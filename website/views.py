from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from website.models import Asset
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    print("🔍 Current user ID:", current_user.id)
    print("🔒 Is authenticated:", current_user.is_authenticated)
    assets = Asset.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, assets=assets)


@views.route('/assets/add', methods=['GET', 'POST'])
@login_required
def add_asset():
    print("✅ Entered add_asset route")

    import os 
    print("DB path:", os.path.abspath("database.db"))
    print("Can write?", os.access("database.db", os.W_OK))
    if request.method == 'POST':
        asset_name = request.form['asset_name']
        category = request.form['category']
        purchase_date = float(request.form['purchase_date'])  # or validate/parse better
        condition = request.form['condition']
        status = request.form['status']

        new_asset = Asset(
            asset_name=asset_name,
            category=category,
            purchase_date=purchase_date,
            condition=condition,
            status=status,
            user_id=current_user.id
        )

        db.session.add(new_asset)
        db.session.commit()
        flash('Asset added successfully!', category='success')
        return redirect(url_for('views.home'))

    return render_template('add_asset.html', user=current_user)


@views.route('/edit-asset/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_asset(id):
    asset = Asset.query.filter_by(id=id, user_id=current_user.id).first()

    if not asset:
        flash("Asset not found or you don't have permission to edit it.", category="error")
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        asset.asset_name = request.form.get('asset_name')
        asset.category = request.form.get('category')
        asset.purchase_date = request.form.get('purchase_date')
        asset.condition = request.form.get('condition')
        asset.status = request.form.get('status')

        db.session.commit()
        flash("Asset updated successfully!", category="success")
        return redirect(url_for('views.home'))

    return render_template('edit_asset.html', asset=asset, user=current_user)





