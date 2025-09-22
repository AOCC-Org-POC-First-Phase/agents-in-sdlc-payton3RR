"""
Publisher Model for Tailspin Toys Crowd Funding Platform

This module defines the Publisher model which represents game publishers
on the crowdfunding platform. Publishers can have multiple games
associated with their account.
"""

from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship
from typing import Dict, Any, Optional

class Publisher(BaseModel):
    """
    Represents a game publisher on the crowdfunding platform.
    
    Publishers create and manage games available for funding.
    Each publisher can have multiple games associated with them.
    """
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one publisher has many games
    games = relationship("Game", back_populates="publisher")

    @validates('name')
    def validate_name(self, key: str, name: str) -> str:
        """
        Validates the publisher name meets minimum length requirements.
        
        Args:
            key: The field name being validated
            name: The publisher name to validate
            
        Returns:
            The validated publisher name
        """
        return self.validate_string_length('Publisher name', name, min_length=2)

    @validates('description')
    def validate_description(self, key: str, description: Optional[str]) -> Optional[str]:
        """
        Validates the publisher description meets minimum length requirements.
        
        Args:
            key: The field name being validated
            description: The description to validate
            
        Returns:
            The validated description or None if not provided
        """
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Publisher instance.
        
        Returns:
            A formatted string with publisher name
        """
        return f'<Publisher {self.name}>'

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Publisher instance to a dictionary for JSON serialization.
        
        Returns:
            Dictionary containing publisher data including game count
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'game_count': len(self.games) if self.games else 0
        }