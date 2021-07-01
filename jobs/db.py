import psycopg2
from flask import current_app,g
from flask.cli import with_appcontext
import click

#to get connection with database.
# to avoid new connections eachtime this funciton is called
# g is used

def get_db():
    if "db" not in g:
        dbname=current_app.config['DATABASE']
        g.db=psycopg2.connect(
           f" dbname={dbname}")
        return g.db

def close_db(e=None):
    db=g.pop('db',None)
    if db is not None:
        db.close()

def init_db():
    db=get_db()
    f=current_app.open_resource("sql/create.sql")
    sql_code=f.read().decode("ascii")
    cur=db.cursor()
    cur.execute(sql_code)
    cur.close()
    db.commit()
    close_db()


#click used to add commands to command line interface.
#flask commands dont run seperately , context is needed
#with_appcontext adds the context before running init_db_command
@click.command('initdb',help="initialize the database")
@with_appcontext
def init_db_command():
    init_db()
    click.echo('DB initialized')

#all commands are to be registered in application.
#this funciton is called in __init__.py which will add command to cli

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


