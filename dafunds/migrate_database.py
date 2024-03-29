# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from dafunds import app,db

migrate=Migrate(app,db)
manager=Manager(app)

manager.add_command('db',MigrateCommand,render_as_batch=True)

if __name__ == '__main__':
    manager.run()

