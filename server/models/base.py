"""
Base Model Module for Tailspin Toys Crowd Funding Platform

This module provides the base SQLAlchemy model class that all other models
inherit from. It includes common validation utilities and database
configuration for the crowdfunding platform.
"""

# filepath: server/models/base.py
from . import db

class BaseModel(db.Model):
    """
    Abstract base model class for all database models in the application.
    
    Provides common functionality including string validation utilities
    that can be used by all model classes.
    """
    __abstract__ = True
    
    @staticmethod
    def validate_string_length(field_name: str, value: str, min_length: int = 2, allow_none: bool = False) -> str:
        """
        Validates that a string field meets minimum length requirements.
        
        Args:
            field_name: The name of the field being validated (for error messages)
            value: The string value to validate
            min_length: The minimum required length (default: 2)
            allow_none: Whether None values are allowed (default: False)
            
        Returns:
            The validated string value
            
        Raises:
            ValueError: If validation fails
        """
        if value is None:
            if allow_none:
                return value
            else:
                raise ValueError(f"{field_name} cannot be empty")
        
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
            
        if len(value.strip()) < min_length:
            raise ValueError(f"{field_name} must be at least {min_length} characters")
            
        return value