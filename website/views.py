from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from website.decorators import admin_only
from website.models import Asset, Asset_History, User
from . import db
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    print("🔍 Current user ID:", current_user.id)
    print("🔒 Authenticated:", current_user.is_authenticated)
    
    from sqlalchemy import or_

    # makes the newest asset added appear first
    assets = Asset.query.order_by(Asset.id.desc()).all()
    all_users = User.query.all()

    return render_template('home.html', user=current_user, assets=assets, all_users=all_users)

@views.route('/users')
@login_required
def users():
    from .models import User
    # Fetch all users to render in a table
    all_users = User.query.all()
    
    return render_template('users.html', users=all_users)



@views.route('/assets/add', methods=['GET', 'POST'])
@login_required
def add_asset():
    print("✅ Entered add_asset route")

    import os 
    print("DB path:", os.path.abspath("database.db"))
    print("Can write?", os.access("database.db", os.W_OK))
    if request.method == 'POST':
        # Extract form fields from db model
        asset_name = request.form['asset_name']
        category = request.form['category']
        purchase_date = datetime.strptime(request.form['purchase_date'], '%Y-%m-%d').date()
        condition = request.form['condition']
        status = request.form['status']
        assigned_user_id = request.form.get('assigned_to')  # Could be empty

        # Assign to user only if status is "In Use"
        assigned_id = int(assigned_user_id) if status == 'In Use' and assigned_user_id else None

        # Create and save new asset
        new_asset = Asset(
            asset_name=asset_name,
            category=category,
            purchase_date=purchase_date,
            condition=condition,
            status=status,
            created_by=current_user.id,
            assigned_to=assigned_id
        )

        db.session.add(new_asset)
        db.session.commit()

        # Log history entry for asset creation
        history = Asset_History(
            asset_id=new_asset.id,
            user_id=current_user.id,
            action="Created",
            notes=f"Asset '{new_asset.asset_name}' was added."
        )
        db.session.add(history)
        db.session.commit()
        
        flash('Asset added successfully!', category='success')
        return redirect(url_for('views.home'))
    
    # GET: Render form to add a new asset
    all_users = User.query.all()
    return render_template('add_asset.html', user=current_user, all_users=all_users)

@views.route('/edit-asset/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_asset(id):
    # Get asset or return 404
    asset = Asset.query.get_or_404(id)

    if not asset:
        flash("Asset not found.", category="error")
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        changes = []
        new_assigned_to = request.form.get('assigned_to')

        # Compare and update each field
        new_name = request.form.get('asset_name')
        if asset.asset_name != new_name:
            changes.append(f"Name: '{asset.asset_name}' → '{new_name}'")
            asset.asset_name = new_name

        new_category = request.form.get('category')
        if asset.category != new_category:
            changes.append(f"Category: '{asset.category}' → '{new_category}'")
            asset.category = new_category

        new_condition = request.form.get('condition')
        if asset.condition != new_condition:
            changes.append(f"Condition: '{asset.condition}' → '{new_condition}'")
            asset.condition = new_condition

        new_status = request.form.get('status')
        if asset.status != new_status:
            changes.append(f"Status: '{asset.status}' → '{new_status}'")
            asset.status = new_status

        # When a new assigned user is selected
        if new_assigned_to and (asset.assigned_to != int(new_assigned_to)):
            old_user = User.query.get(asset.assigned_to) if asset.assigned_to else None
            new_user = User.query.get(int(new_assigned_to))

            old_name = f"{old_user.first_name} {old_user.last_name}" if old_user else "None"
            new_name = f"{new_user.first_name} {new_user.last_name}"

            changes.append(f"Assigned to: '{old_name}' → '{new_name}'")
            asset.assigned_to = new_user.id

        # When user is cleared (assigned_to set to None)
        elif new_assigned_to == '':
            if asset.assigned_to is not None:
                old_user = User.query.get(asset.assigned_to)
                old_name = f"{old_user.first_name} {old_user.last_name}" if old_user else "Unknown"
                changes.append(f"Assigned to: '{old_name}' → None")
                asset.assigned_to = None

        # Commit changes if any
        if changes:
            db.session.commit()  # Save the changes first

            # Save update history
            history = Asset_History(
                asset_id=asset.id,
                user_id=current_user.id,
                action="Updated",
                notes="; ".join(changes)
            )
            db.session.add(history)
            db.session.commit()

            flash("Asset updated successfully!", category="success")
        else:
            flash("No changes were made to the asset.", category="info")

        return redirect(url_for('views.home'))

    # GET: Show form pre-filled with asset data
    all_users = User.query.all()
    return render_template('edit_asset.html', asset=asset, user=current_user, all_users=all_users)



@views.route('/delete-asset/<int:id>', methods=['POST'])
@login_required
@admin_only # Only admins can delete assets
def delete_asset(id):
    asset = Asset.query.get_or_404(id)

    # Log the deletion before removing the asset
    history = Asset_History(
        asset_id=asset.id,
        user_id=current_user.id,
        action="Deleted",
        notes=f"Asset '{asset.asset_name}' was deleted."
    )
    db.session.add(history)

    db.session.delete(asset)
    db.session.commit()

    flash("Asset deleted successfully.", category="success")
    return redirect(url_for('views.home'))

@views.route('/dashboard')
@login_required
def dashboard():

    # Show all assets and recent history
    all_assets = Asset.query.all()
    all_history = Asset_History.query.order_by(Asset_History.timestamp.desc()).all()

    return render_template('dashboard.html', user=current_user, assets=all_assets, history=all_history)







