import configparser
import json
import os
import time
import re
import threading
import random
import copy

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import generic_protein
from flask import Flask, request, render_template, Response

import mysql.connector as mysql

config = configparser.ConfigParser()
config.read("config.ini")

root_dir = config["DEFAULT"]["ROOT_DIR"]

app = Flask(
    __name__,
    template_folder=os.path.join(root_dir, "templates"),
    root_path=root_dir,
)

mysql_config = config["mysql"]


def get_mysql_conn():
    return mysql.connect(
        host=mysql_config["DB_HOST"],
        user=mysql_config["DB_USER"],
        passwd=mysql_config["DB_PASSWORD"],
        db=mysql_config["DB_NAME"],
    )


GENOME_NAMES = [
    "NC_000852",
    "NC_007346",
    "NC_008724",
    "NC_009899",
    "NC_014637",
    "NC_020104",
    "NC_023423",
    "NC_023640",
    "NC_023719",
    "NC_027867",
]


@app.route('/')
def index():
    return render_template("index.html")


def compute_match(search_sequence, search_sequence_name, delay_s):
    shuffled = copy.copy(GENOME_NAMES)
    random.shuffle(shuffled)
    matched_name = None
    matched_index = None

    for genome_name in shuffled:
        gb_record = SeqIO.read(
            open("genomes/{}.gb".format(genome_name), "r"), "genbank"
        )
        full_seq = gb_record.seq

        for feature in gb_record.features:
            if feature.type == "CDS":
                protein_seq = feature.extract(full_seq)

                # Find exact match within given sequence
                if protein_seq == search_sequence:
                    try:
                        matched_name = feature.qualifiers["protein_id"][0]
                    except (KeyError, IndexError):
                        matched_name = "Not Available"

                    # Index within the original genome
                    # Note that the index starts at 1 instead of 0
                    matched_index = int(feature.location.start)
                    break

    time.sleep(delay_s)
    db = get_mysql_conn()
    cursor = db.cursor(buffered=True)
    cursor.execute(
        "INSERT INTO results "
        "(search_sequence_name, search_sequence, matched_name, matched_index) "
        "VALUES (%s, %s, %s, %s)",
        (search_sequence_name, search_sequence, matched_name, matched_index)
    )
    db.commit()
    cursor.close()


@app.route("/find_dna_sequence", methods=["POST"])
def find_dna_sequence():
    payload = request.get_json()

    search_sequence = payload.get("dna_sequence")
    search_sequence_name = payload.get("dna_sequence_name")
    delay_s = payload.get("delay_s") or 0

    try:
        delay_s = int(delay_s)
    except ValueError:
        return Response(
            response=json.dumps({
                "err": "Delay must be a number"
            }),
            status=400,
        )

    if not search_sequence or not search_sequence_name:
        return Response(
            response=json.dumps({
                "err": "Must provide a sequence and sequence name"
            }),
            status=400,
        )

    search_sequence = re.sub(r'[\n\s]', '', search_sequence).upper()
    search_sequence_name = search_sequence_name.strip()

    t = threading.Thread(
        target=compute_match,
        args=(search_sequence, search_sequence_name, delay_s)
    )
    t.start()

    return Response(status=200)


@app.route("/get_latest_results", methods=["POST"])
def get_latest_results():
    db = get_mysql_conn()
    cursor = db.cursor(buffered=True)
    cursor.execute(
        "SELECT id, search_sequence_name, matched_name, matched_index "
        "FROM results ORDER BY id DESC LIMIT 10",
    )
    result = cursor.fetchall()
    cursor.close()
    return Response(json.dumps(result))


@app.route("/get_searched_by_id/<int:searched>")
def get_searched_by_id(searched):
    db = get_mysql_conn()
    cursor = db.cursor(buffered=True)
    query = "SELECT search_sequence FROM results WHERE id = {}".format(searched)
    cursor.execute(query)

    search_sequence = cursor.fetchone()
    cursor.close()

    if search_sequence is None:
        return Response(
            response=json.dumps({
                "err": "id not found"
            }),
            status=400,
        )

    return Response(json.dumps({"search_sequence": search_sequence[0]}))


if __name__ == '__main__':
    app.run(port=config["DEFAULT"]["PORT"])
