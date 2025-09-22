"""
Models Package Initialization for Tailspin Toys Crowd Funding Platform

This module initializes the SQLAlchemy database instance and provides
database configuration utilities. It imports all model classes and
provides the main init_db function for setting up the database.
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Import for type hints only
    from .category import Category
    from .game import Game
    from .publisher import Publisher

db = SQLAlchemy()

# Import models after db is defined to avoid circular imports
from .category import Category
from .game import Game
from .publisher import Publisher

def init_db(app: Flask, testing: bool = False) -> None:
    """
    Initialize the database with the Flask application.
    
    Sets up the SQLAlchemy database instance with the provided Flask app
    and creates all necessary database tables.
    
    Args:
        app: The Flask application instance to initialize
        testing: If True, allows reinitialization for testing purposes
    """
    if testing:
        # For testing, we want to be able to reinitialize
        db.init_app(app)
    else:
        try:
            db.init_app(app)
        except RuntimeError:
            # Database already initialized
            pass
    
    # Create tables when initializing
    with app.app_context():
        db.create_all()