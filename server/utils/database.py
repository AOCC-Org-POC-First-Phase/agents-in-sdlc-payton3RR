"""
Database Utilities for Tailspin Toys Crowd Funding Platform

This module provides database initialization and configuration utilities
for the Flask application. It handles SQLite database setup and
connection management for the crowdfunding platform.
"""

import os
from models import init_db as models_init_db
from flask import Flask
from typing import Optional

def init_db(app: Flask, connection_string: Optional[str] = None, testing: bool = False) -> None:
    """
    Initializes the database with the given Flask app and connection string.
    
    If no connection string is provided, a default SQLite connection string is used
    pointing to the project's data directory.
    
    Args:
        app: The Flask application instance to configure
        connection_string: Optional database connection string. If None, uses default SQLite
        testing: If True, allows reinitialization for testing purposes
    """
    if connection_string is None:
        connection_string = __get_connection_string()
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    models_init_db(app, testing=testing)

def __get_connection_string() -> str:
    """
    Returns the default SQLite connection string for the application.
    
    Creates the data directory if it doesn't exist and returns a connection
    string pointing to the tailspin-toys.db file in the project's data folder.
    
    Returns:
        SQLite connection string for the application database
    """
    # Get the server directory
    server_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Go up one level to project root, then into data folder
    project_root = os.path.dirname(server_dir)
    data_dir = os.path.join(project_root, "data")
    
    # Create the data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
    return f'sqlite:///{os.path.join(data_dir, "tailspin-toys.db")}'