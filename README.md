## View on production
`http://andrew-liang.com/sequence_alignment`


## Setup for local development

Assumes python3, virtualenv, and mysql are all installed.

1. `git clone https://github.com/lianga888/sequence_alignment.git`

2. Create an `env.json` file at the project root with following 
values:

```
{
  "mysql": {
    "user": "root",
    "host": "localhost",
    "password": "",
    "database": <DB_NAME>
  },
  "port": <PORT>
}
```

(this assumes you have a local MySQL with the database `DB_NAME` created)

3. Create your virtualenv and use it: `virtualenv venv && source venv/bin/activate`

4. Install your requirements and template your configs: `./setup`

5. Run alembic to set up your local DB schema: `alembic upgrade head`

6. `PYTHONPATH=. python3 lib/app.py`

7. Visit `http://localhost:<PORT>`  