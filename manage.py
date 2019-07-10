from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from app.db_loader import populate_db

# Initializing the manager
manager = Manager(app)

# Initialize Flask Migrate
migrate = Migrate(app, db)

# Add the flask migrate
manager.add_command('db', MigrateCommand)

@manager.command
def populate():
    """
        Loading data to database if not loaded
    """
    populate_db()

# Run the manager
if __name__ == '__main__':
    manager.run()