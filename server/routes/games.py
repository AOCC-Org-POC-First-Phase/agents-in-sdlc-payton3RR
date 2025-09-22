"""
Games API Routes for Tailspin Toys Crowd Funding Platform

This module provides REST API endpoints for managing and retrieving
game information. It includes endpoints for listing all games and
retrieving individual game details with publisher and category data.
"""

from flask import jsonify, Response, Blueprint
from models import db, Game, Publisher, Category
from sqlalchemy.orm import Query
from typing import Union, Tuple

# Create a Blueprint for games routes
games_bp = Blueprint('games', __name__)

def get_games_base_query() -> Query:
    """
    Creates a base SQLAlchemy query for games with joined publisher and category data.
    
    This query includes left outer joins to ensure games are returned even if
    publisher or category relationships are missing.
    
    Returns:
        A SQLAlchemy Query object ready for further filtering or execution
    """
    return db.session.query(Game).join(
        Publisher, 
        Game.publisher_id == Publisher.id, 
        isouter=True
    ).join(
        Category, 
        Game.category_id == Category.id, 
        isouter=True
    )

@games_bp.route('/api/games', methods=['GET'])
def get_games() -> Response:
    """
    Retrieves a list of all games available on the crowdfunding platform.
    
    Returns a JSON array of game objects, each containing the game's
    basic information along with associated publisher and category details.
    
    Returns:
        JSON response containing an array of game objects
    """
    # Use the base query for all games
    games_query = get_games_base_query().all()
    
    # Convert the results using the model's to_dict method
    games_list = [game.to_dict() for game in games_query]
    
    return jsonify(games_list)

@games_bp.route('/api/games/<int:id>', methods=['GET'])
def get_game(id: int) -> Union[Tuple[Response, int], Response]:
    """
    Retrieves a specific game by its ID.
    
    Returns detailed information about a single game including its
    associated publisher and category information.
    
    Args:
        id: The unique identifier of the game to retrieve
        
    Returns:
        JSON response containing the game object, or 404 error if not found
    """
    # Use the base query and add filter for specific game
    game_query = get_games_base_query().filter(Game.id == id).first()
    
    # Return 404 if game not found
    if not game_query: 
        return jsonify({"error": "Game not found"}), 404
    
    # Convert the result using the model's to_dict method
    game = game_query.to_dict()
    
    return jsonify(game)
