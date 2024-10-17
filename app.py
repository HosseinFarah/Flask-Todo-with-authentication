from app import app, db
from app.models import User, Todo
import sqlalchemy as sa
import sqlalchemy.orm as so

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Todo': Todo, 'sa': sa, 'so': so}