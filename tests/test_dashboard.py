def test_deleted_asset_still_in_history(client, register_and_login_admin, app):
    register_and_login_admin()

    # Create and delete an asset
    with app.app_context():
        from website import db
        from website.models import Asset, Asset_History
        asset = Asset(asset_name='GhostAsset', category='Archived')
        db.session.add(asset)
        db.session.commit()

        history = Asset_History(asset_id=asset.id, user_id=1, action='Deleted', notes='Deleted via test')
        db.session.add(history)
        db.session.delete(asset)
        db.session.commit()

    # Visit dashboard
    response = client.get('/dashboard', follow_redirects=True)

    assert b'GhostAsset' not in response.data  # asset is gone
    assert b'Deleted' in response.data         # history entry still visible
    assert b'[Deleted Asset]' in response.data  # rendered safely
