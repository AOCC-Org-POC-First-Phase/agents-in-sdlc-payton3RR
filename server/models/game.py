"""
Game Model for Tailspin Toys Crowd Funding Platform

This module defines the Game model which represents individual games
available for crowdfunding. Games are linked to publishers and categories
and include rating information.
"""

from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship
from typing import Dict, Any, Optional

class Game(BaseModel):
    """
    Represents a game available for crowdfunding on the platform.
    
    Each game belongs to a publisher and category, and includes
    descriptive information and user ratings.
    """
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    star_rating = db.Column(db.Float, nullable=True)
    
    # Foreign keys for one-to-many relationships
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'), nullable=False)
    
    # One-to-many relationships (many games belong to one category/publisher)
    category = relationship("Category", back_populates="games")
    publisher = relationship("Publisher", back_populates="games")
    
    @validates('title')
    def validate_name(self, key: str, name: str) -> str:
        """
        Validates the game title meets minimum length requirements.
        
        Args:
            key: The field name being validated
            name: The title value to validate
            
        Returns:
            The validated title
        """
        return self.validate_string_length('Game title', name, min_length=2)
    
    @validates('description')
    def validate_description(self, key: str, description: Optional[str]) -> Optional[str]:
        """
        Validates the game description meets minimum length requirements.
        
        Args:
            key: The field name being validated
            description: The description value to validate
            
        Returns:
            The validated description or None
        """
        if description is not None:
            return self.validate_string_length('Description', description, min_length=10, allow_none=True)
        return description
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the Game instance.
        
        Returns:
            A formatted string with game title and ID
        """
        return f'<Game {self.title}, ID: {self.id}>'

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Game instance to a dictionary for JSON serialization.
        
        Returns:
            Dictionary containing game data with related publisher and category info
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'publisher': {'id': self.publisher.id, 'name': self.publisher.name} if self.publisher else None,
            'category': {'id': self.category.id, 'name': self.category.name} if self.category else None,
            'starRating': self.star_rating  # Changed from star_rating to starRating
        }