import pytest
from flask_app import create_app
from db_instance import db
from models import Fighter

@pytest.fixture(scope='module')
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ufc_test.db'  # Use a test database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture(scope='module')
def init_db(app):
    """Initialize the database."""
    db.create_all()  # Create tables
    yield db  # Provide the db instance for tests
    db.drop_all()  # Cleanup after tests

@pytest.fixture
def new_fighter(init_db):
    """Fixture to create a new fighter for testing."""
    fighter = Fighter(name="Conor McGregor", nickname="The Notorious", weight_class="Lightweight")
    db.session.add(fighter)
    db.session.commit()
    return fighter

def test_add_fighter(init_db, new_fighter):
    """Test that a fighter can be added to the database."""
    fighter = Fighter.query.filter_by(name="Conor McGregor").first()
    assert fighter is not None
    assert fighter.nickname == "The Notorious"
    assert fighter.weight_class == "Lightweight"

def test_query_fighter(init_db, new_fighter):
    """Test querying a fighter by name."""
    fighter = Fighter.query.filter_by(name="Conor McGregor").first()
    assert fighter is not None
    assert fighter.name == "Conor McGregor"

def test_fighter_not_in_db():
    """Test that a fighter not in the DB returns None."""
    fighter = Fighter.query.filter_by(name="Nonexistent Fighter").first()
    assert fighter is None

def test_update_fighter(init_db, new_fighter):
    """Test that a fighter's details can be updated."""
    fighter = Fighter.query.filter_by(name="Conor McGregor").first()
    fighter.nickname = "The Mystic"
    db.session.commit()

    updated_fighter = Fighter.query.filter_by(name="Conor McGregor").first()
    assert updated_fighter.nickname == "The Mystic"

