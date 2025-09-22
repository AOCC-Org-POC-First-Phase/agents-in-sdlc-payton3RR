"""
Category Model for Tailspin Toys Crowd Funding Platform

This module defines the Category model which represents game categories
used to organize games on the crowdfunding platform. Categories help
users discover games by type or theme.
"""

from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship
from typing import Dict, Any, Optional

class Category(BaseModel):
    """
    Represents a game category on the crowdfunding platform.
    
    Categories are used to organize and classify games, making it easier
    for users to discover games that match their interests.
    """
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one category has many games
    games = relationship("Game", back_populates="category")
    
    @validates('name')
    def validate_name(self, key: str, name: str) -> str:
        """
        Validates the category name meets minimum length requirements.
        
        Args:
            key: The field name being validated
            name: The category name to validate
            
        Returns:
            The validated category name
        """
        return self.validate_string_length('Category name', name, min_length=2)
        
    @validates('description')
    def validate_description(self, key: str, description: Optional[str]) -> Optional[str]:
        """
        Validates the category description meets minimum length requirements.
        
        Args:
            key: The field name being validated
            description: The description to validate
            
        Returns:
            The validated description or None if not provided
        """
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the Category instance.
        
        Returns:
            A formatted string with category name
        """
        return f'<Category {self.name}>'
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Category instance to a dictionary for JSON serialization.
        
        Returns:
            Dictionary containing category data including game count
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'game_count': len(self.games) if self.games else 0
        }