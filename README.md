# My Candidate flask template

## Technical Specs for QA
* Python 3.10.8
* postgresql 12.6.* or later


## Website Environments
- [Production Environment](https://southafrica.mycandidate.africa/)

## Backend Setup
### Setting up a virtual environment with Python and pip
* clone the repo
* install a virtual env and activate it: `python -m venv env; env/Scripts/activate`[Windows]
* install a virtual env and activate it: `virtualenv --no-site-packages env; source env/bin/activate`[Linux/iOS]
* install requirements: `pip install -r requirements.txt`
* copy the configuration file: `cp dexter/config/example.development.cfg dexter/config/development.cfg`.

### Setting up a virtual anaconda environment with Python and pip
* clone the repo
* install a virtual conda env: `conda create -n mycandidate`
* activate the conda env: `source activate mycandidate`  
_for the VS Code IDE, make sure the new environment is set as the python interpreter_
* install requirements: `pip install -r requirements.txt`  
  _If errors are thrown, comment out the package in package.json, and handle afterwards individually. Uncomment package when committing back into repo_

### Setting up the Database with PostgreSQL
Setup the PostgreSQL database (minimum version 12.*)
```
psql -U postgres
=# CREATE USER mycandidate WITH PASSWORD 'mycandidate_<country_code>';
=# CREATE DATABASE mycandidate_<country_code>;
=# GRANT ALL PRIVILEGES ON DATABASE mycandidate_<country_code> TO mycandidate;
=# \q
```
- i.e mycandidate_<country_code> = mycandidate_za
Construct your db app-side:
```
from main.models import db
from main.models.seeds import seed_db
run 'python rebuild_db.py'
```

### Deploying database changes
* mycandidate App uses Flask-Migrate (which uses Alembic) to handle database migrations.
* To add a new model or make changes, update the SQLAlchemy definitions in `main/models/`. Then run
`alembic revision -m "create account table"`
* This will autogenerate a change. Double check that it make sense. To apply it on your machine, run
`alembic upgrade head`
* To downgrade all versions, this ultimately delete all tables
`alembic downgrade base`
  

### Pytest
- Powershell Run: `$ENV:PYTHONPATH = "<name-of-project>"`
- Linux/Mac to set the environment path `export PYTOHNPATH=<name-of-project>`

Then run `pytest` for simple test summary or `pytest -vv` for detailed test summary

### Redis Setup
Redis is required for caching and background task management.

Install Redis:

1. On Mac OS X: `brew install redis`
2. On Windows: Use the Redis [MSI installer](https://github.com/microsoftarchive/redis/releases)
3. On Ubuntu: `sudo apt-get update && sudo apt-get install redis-server`
4. Update your `development.cfg` to include Redis configuration: `REDIS_URL = "redis://<redis-host>"`