import json
import os

from jinja2 import Template

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

with open("env.json") as f:
    config = json.load(f)
    config["root_dir"] = ROOT_DIR

with open("alembic.ini", "w") as f:
    f.write(Template(open("alembic.ini.j2").read()).render(config))

with open("config.ini", "w") as f:
    f.write(Template(open("config.ini.j2").read()).render(config))



