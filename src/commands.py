from flask.cli import with_appcontext
import click
from click import command
import os
from src.ext import db
from src.models.product import Category
from src.models.user import User


def init_db():
    click.echo('Initializing database')
    db.drop_all()
    db.create_all()
    click.echo('Done')

def populate_db():
    click.echo('Populating database')
    admin=User.query.filter_by(name='admin').first()
   
    admin = User(name = 'admin', role='admin', password=os.getenv('ADMIN_PASSWORD','admin123'))
    admin.create()
    category1=Category(name='Woman')
    category2=Category(name='Man')
    category3=Category(name='Child')

    categories = [category1,category2,category3]
    for category in categories:
        category.create()

    ipeks=[]
    for ipek in ipeks:
        ipek.create()

    click.echo('Done')

@command('init_db')
@with_appcontext
def init_db_command():
    init_db()


@command('populate_db')
@with_appcontext
def populate_db_command():
    populate_db()






