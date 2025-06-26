def test_known_user_shown_in_user_table(client, register_and_login_admin, app):
    register_and_login_admin()

    with app.app_context():
        from website.models import User
        from website import db
        user = User(email='unit@test.com', first_name='Unit', last_name='Testy', role='user', password='dummy')
        db.session.add(user)
        db.session.commit()

    response = client.get('/users', follow_redirects=True)

    User.query.filter_by(email='unit@test.com').delete()
    db.session.commit()

    assert b'unit@test.com' in response.data
    assert b'Testy' in response.data
