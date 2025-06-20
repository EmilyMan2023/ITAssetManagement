from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from website.models import Asset
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/assets')
def list_assets():
    assets = Asset.query.all()
    return render_template('home.html', assets=assets, user=current_user)


@views.route('/assets/add', methods=['GET', 'POST'])
@login_required
def add_asset():
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
        return redirect(url_for('views.list_assets'))

    return render_template('add_asset.html', user=current_user)


@views.route('/assets/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_asset(id):
    asset = Asset.query.get_or_404(id)

    if request.method == 'POST':
        asset.name = request.form.get('name')
        asset.description = request.form.get('description')
        db.session.commit()
        flash('Asset updated!', category='success')
        return redirect(url_for('views.list_assets'))

    return render_template('edit_asset.html', asset=asset, user=current_user)




