from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    department = db.Column(db.String(150))
    role = db.Column(db.String(10), nullable=False, default='user')

    # Relationship fixes:
    created_assets = db.relationship('Asset', foreign_keys='Asset.created_by', backref='creator_user')
    assigned_assets = db.relationship('Asset', foreign_keys='Asset.assigned_to', backref='assignee_user')


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(150))
    category = db.Column(db.String(150))
    purchase_date = db.Column(db.Date)
    condition = db.Column(db.String(150))
    status = db.Column(db.String(150))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    asset_history = db.relationship('Asset_History', back_populates='asset', passive_deletes=True)
    creator = db.relationship('User', foreign_keys=[created_by])
    assignee = db.relationship('User', foreign_keys=[assigned_to])

class Asset_History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id', ondelete='SET NULL'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # e.g. 'Created', 'Updated', 'Assigned', 'Deleted'
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    notes = db.Column(db.Text, nullable=True)

    # Relationships
    asset = db.relationship('Asset', back_populates='asset_history', passive_deletes=True)
    user = db.relationship('User')
