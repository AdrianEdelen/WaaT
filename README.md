# WaaT
To get started with development:
1. Install Python version 3.11.8 
   -  it may work with other versions but I haven't tested them
2. clone the repo into your desired working directory: git clone https://github.com/AdrianEdelen/WaaT/
3. Install required packages by running `pip install -r requirements.txt`
4. Create a .env.development file in the repo's main directory.
   - See below for a template of the .env file.
   - when working locally, you need an env.development file.
   - when developing in docker or deploying ensure the docker file has ENVIRONMENT=DOCKER var.
   - you can use the following DB providers:
     - SQLite - So far only SQLite is tested and this is recommended for development
     - PostgresSQL
     - MySQL/MariaDB
     - SQL Server
5. execute the program in your preferred way

Here is an example of a launch.json (for vscode):
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Run main.py",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal"
        }
    ]
}
```



The DATABASE_URL should follow the format recognized by SQLAlchemy, which generally looks like:

`dialect+driver://username:password@host/dbname`

#### Example variables for the supported Database providers:
```
- SQLite: sqlite:///./test.db (note the three slashes, indicating a relative file path)
- PostgreSQL: postgresql://user:password@localhost/dbname
- MySQL/MariaDB: mysql+pymysql://user:password@localhost/dbname (using pymysql as the driver)
- SQL Server: mssql+pyodbc://user:password@servername/dbname?driver=SQL+Server (using pyodbc and have the SQL Server ODBC driver installed)
```

I can't promise efficacy of the db providers outside of psql and sqlite, since those are the only ones I use. I am using SQLAlchemy so they should work.

#### example .env.development file:
```
DEBUG=true 
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
