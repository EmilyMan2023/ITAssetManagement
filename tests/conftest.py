import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from website import create_app, db
from flask import template_rendered



@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'testsecret'


    with app.app_context():
        db.create_all()
        yield app  # this provides the app to other fixtures/tests

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def register_and_login_admin(client, app):
    def do_login():
        client.post('/sign-up', data={
            'email': 'admin@example.com',
            'firstName': 'Admin',
            'lastName': 'Tester',
            'password1': 'adminpass',
            'password2': 'adminpass',
            'department': 'IT',  # ✅ add this
            'role': 'admin'
        }, follow_redirects=True)
        client.post('/login', data={
            'email': 'admin@example.com',
            'password': 'adminpass'
        }, follow_redirects=True)
    return do_login


