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

    # Relationships - this user has created these assets
    created_assets = db.relationship('Asset', foreign_keys='Asset.created_by', backref='creator_user')
    # this user has been assigned these assets
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
    
    # this asset has many history records
    asset_history = db.relationship('Asset_History', back_populates='asset', passive_deletes=True)
    # user who added the asset
    creator = db.relationship('User', foreign_keys=[created_by])
    # user currently using the asset
    assignee = db.relationship('User', foreign_keys=[assigned_to])

class Asset_History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # which asset this history log belongs to
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id', ondelete='SET NULL'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # e.g. 'Created', 'Updated', 'Assigned', 'Deleted'
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    notes = db.Column(db.Text, nullable=True)

    # relationship back to the associated asset
    asset = db.relationship('Asset', back_populates='asset_history', passive_deletes=True)
    # who performed the action
    user = db.relationship('User')
