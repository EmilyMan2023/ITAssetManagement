def test_add_asset(client, register_and_login_admin):
    register_and_login_admin()
    response = client.post('/assets/add', data={
        'asset_name': 'Test Laptop',
        'category': 'Electronics',
        'purchase_date': '2024-01-01',
        'condition': 'New',
        'status': 'Available'
    }, follow_redirects=True)

    assert b'Test Laptop' in response.data

def test_edit_asset(client, register_and_login_admin, app):
    register_and_login_admin()

    # Add the asset
    client.post('/assets/add', data={
        'asset_name': 'EditTest',
        'category': 'Furniture',
        'purchase_date': '2023-01-01',
        'condition': 'Used',
        'status': 'Available'
    }, follow_redirects=True)

    # Get the asset's ID (assuming ID 1 since test DB is fresh)
    with app.app_context():
        from website.models import Asset
        asset = Asset.query.filter_by(asset_name='EditTest').first()
        assert asset is not None

    # Edit the asset
    response = client.post(f'/edit-asset/{asset.id}', data={
        'asset_name': 'UpdatedTest',
        'category': 'Electronics',
        'purchase_date': '2023-01-01',
        'condition': 'Refurbished',
        'status': 'Assigned'
    }, follow_redirects=True)

    assert b'UpdatedTest' in response.data
    assert b'EditTest' not in response.data

def test_delete_asset(client, register_and_login_admin, app):
    register_and_login_admin()

    # Add the asset
    client.post('/assets/add', data={
        'asset_name': 'DeleteMe',
        'category': 'Misc',
        'purchase_date': '2022-06-15',
        'condition': 'New',
        'status': 'Available'
    }, follow_redirects=True)

    # Get the asset's ID
    with app.app_context():
        from website.models import Asset
        asset = Asset.query.filter_by(asset_name='DeleteMe').first()
        asset_id = asset.id

    # Delete the asset
    response = client.post(f'/delete-asset/{asset_id}', follow_redirects=True)

    assert b'DeleteMe' not in response.data

def test_delete_button_hidden_from_regular_user(client, app):
    # Register and log in as a regular user
    client.post('/sign-up', data={
        'email': 'viewer@example.com',
        'firstName': 'ReadOnly',
        'lastName': 'User',
        'password1': 'viewpass',
        'password2': 'viewpass',
        'role': 'user'
    }, follow_redirects=True)

    client.post('/login', data={
        'email': 'viewer@example.com',
        'password': 'viewpass'
    }, follow_redirects=True)

    # Add an asset (directly via app context, since regular user can't access the form)
    with app.app_context():
        from website.models import Asset
        from website import db
        asset = Asset(asset_name='InvisibleDelete', category='Test')
        db.session.add(asset)
        db.session.commit()

    # Visit dashboard
    response = client.get('/dashboard', follow_redirects=True)

    # Assert "Delete" button not shown
    assert b'delete-asset' not in response.data




