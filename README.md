# WaaT

Python version 3.11.8
install required packages with requirements.txt

when working locally, you need an env.development file.
when developing in docker or deploying ensure the docker file has ENVIRONMENT=DOCKER var.

The web server can be run or not by setting the 'START_WEBSERVER' variable to true.

The DATABASE_URL should follow the format recognized by SQLAlchemy, which generally looks like:

`dialect+driver://username:password@host/dbname`

### Example variables for the supported Database providers:
- SQLite: sqlite:///./test.db (note the three slashes, indicating a relative file path)
- PostgreSQL: postgresql://user:password@localhost/dbname
- MySQL/MariaDB: mysql+pymysql://user:password@localhost/dbname (using pymysql as the driver)
- SQL Server: mssql+pyodbc://user:password@servername/dbname?driver=SQL+Server (using pyodbc and have the SQL Server ODBC driver installed)


I can't promise efficacy of the db providers outside of psql and sqlite, since those are the only ones I use. I am using SQLAlchemy so they should work.

#### example .env.development file:
``` DEBUG=true 
CHANNEL_NAME=Test
META_CHANNEL_NAME=Test-Meta
GUILD_ID=54564645646464
DATABASE_URL=test.db
BOT_COMMAND_PREFIX=!
DISCORD_API_KEY=APIKEY
DATABASE=sqlite
DATABASE_URL=sqlite:///./test.db
WEBSERVER_URL=localhost
WEBSERVER_PORT=8080 ```
