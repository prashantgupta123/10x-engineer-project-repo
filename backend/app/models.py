"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier using UUID4.
    
    Returns:
        str: A unique identifier string.
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Get the current UTC timestamp.
    
    Returns:
        datetime: Current UTC datetime.
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for prompt data.
    
    Attributes:
        title (str): Prompt title, 1-200 characters.
        content (str): Prompt content, minimum 1 character.
        description (Optional[str]): Optional description, max 500 characters.
        collection_id (Optional[str]): Optional ID of parent collection.
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Model for creating a new prompt.
    
    Inherits all fields from PromptBase.
    """
    pass


class PromptUpdate(PromptBase):
    """Model for updating an existing prompt.
    
    Inherits all fields from PromptBase.
    """
    pass


class Prompt(BaseModel):
    """Complete prompt model with all fields.
    
    Attributes:
        title (str): Prompt title, 1-200 characters.
        content (str): Prompt content, minimum 1 character.
        description (Optional[str]): Optional description, max 500 characters.
        collection_id (Optional[str]): Optional ID of parent collection.
        id (str): Unique identifier, auto-generated.
        created_at (datetime): Creation timestamp, auto-generated.
        updated_at (datetime): Last update timestamp, auto-generated.
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    model_config = {
        'from_attributes': True
    }


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for collection data.
    
    Attributes:
        name (str): Collection name, 1-100 characters.
        description (Optional[str]): Optional description, max 500 characters.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model for creating a new collection.
    
    Inherits all fields from CollectionBase.
    """
    pass

class Collection(BaseModel):
    """Complete collection model with all fields.
    
    Attributes:
        name (str): Collection name, 1-100 characters.
        description (Optional[str]): Optional description, max 500 characters.
        id (str): Unique identifier, auto-generated.
        created_at (datetime): Creation timestamp, auto-generated.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    model_config = {
        'from_attributes': True
    }


# ============== Response Models ==============

class PromptList(BaseModel):
    """Response model for list of prompts.
    
    Attributes:
        prompts (List[Prompt]): List of prompt objects.
        total (int): Total count of prompts.
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Response model for list of collections.
    
    Attributes:
        collections (List[Collection]): List of collection objects.
        total (int): Total count of collections.
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Response model for health check endpoint.
    
    Attributes:
        status (str): Health status of the API.
        version (str): Current API version.
    """
    status: str
    version: str


# ============== Prompt Version Models ==============

class PromptVersionBase(BaseModel):
    """Base model for prompt version data.
    
    Attributes:
        title (str): Version title, 1-200 characters.
        content (str): Version content, minimum 1 character.
        description (Optional[str]): Optional description of changes, max 500 characters.
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)


class PromptVersionCreate(PromptVersionBase):
    """Model for creating a new prompt version.
    
    Inherits all fields from PromptVersionBase.
    """
    pass


class PromptVersion(BaseModel):
    """Complete prompt version model with all fields.
    
    Attributes:
        id (str): Unique identifier, auto-generated.
        prompt_id (str): ID of the parent prompt.
        title (str): Version title, 1-200 characters.
        content (str): Version content, minimum 1 character.
        description (Optional[str]): Optional description of changes.
        version_number (int): Sequential version number (1, 2, 3...).
        created_at (datetime): Creation timestamp, auto-generated.
    """
    id: str = Field(default_factory=generate_id)
    prompt_id: str
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    version_number: int = Field(..., ge=1)
    created_at: datetime = Field(default_factory=get_current_time)

    model_config = {
        'from_attributes': True
    }


class PromptVersionList(BaseModel):
    """Response model for list of prompt versions.
    
    Attributes:
        versions (List[PromptVersion]): List of version objects.
        total (int): Total count of versions.
    """
    versions: List[PromptVersion]
    total: int

