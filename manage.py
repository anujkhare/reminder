from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from MsgApp import app, db


print('Manage 1')
app.config.from_object('MsgApp.appconfig')

migrate = Migrate(app, db)
manager = Manager(app)
print('Manage 2')

manager.add_command('db', MigrateCommand)

print('Manage 3')

if __name__ == '__main__':
    manager.run()
    print('Manage 5')
