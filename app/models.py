"""Models to interact with 'recipes.db' """
from .extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Alias common SQLAlchemy names
Integer = db.Integer
Column = db.Column
String = db.String

# TODO: Change 'Recipe' db column names to be more descriptive:
# The column names and types were imported from an old 'Lotus Approach' db...
# they need renaming/restructuring.
# desc -> category
# type -> cuisine
# note -> instructions
# ingred -> ingredients


class Recipe(db.Model):
    """Model for interacting with 'recipe' table in database."""
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    desc = Column(String)
    prep_time = Column(String)
    servings = Column(String)
    cal_p_serving = Column(String)
    ingred = Column(String)
    source = Column(String)
    note = Column(String)
    type = Column(String)
    date = Column(String)
    main_ingredient = Column(String)
    category = Column(String)

    def __repr__(self):
        return f"< {self.id} | {self.name} | {self.category} >"


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password_hash = Column(String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
