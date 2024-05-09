# shoal
System that allows you to view telephone numbers taken from LDAP People. In a version of https://github.com/efornal/cardumen in python.

### Docker
* Volume Creation
```bash
docker volume create mollys_app
docker volume create mollys_pgdata
```
* Application settings
```bash
Copy .env.tpl to .env.dev and configure with custom values
```
configuration details in /mollys/settings.py
* Environment creation with docker-compose 
```bash
docker-compose up
```
* Volume creation
```bash
docker volume create shoal_pgdata
```
* Database initialization
To initialize the database (creation of connection users, etc) or import the database from a dump, the file must be added to the db directory, which will then be mounted where the postgresql image requires it.
```bash
$ ls db/
init_db_or_dump.sql
```
* Health ckeck
For the health check, the middelware proposed at https://www.ianlewis.org/en/kubernetes-health-checks-django is used