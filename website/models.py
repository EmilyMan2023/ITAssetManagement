from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    department = db.Column(db.String(150))
    assets = db.relationship('Asset')
    role = db.Column(db.String(10), nullable=False, default='user')

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    asset_name = db.Column(db.String(150))
    category = db.Column(db.String(150))
    purchase_date = db.Column(db.Float)
    condition = db.Column(db.String(150))
    status = db.Column(db.String(150))