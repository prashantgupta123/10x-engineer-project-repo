# GitHub Copilot Instructions for PromptLab

This guide helps AI agents generate high-quality, consistent code for the PromptLab AI Prompt Engineering Platform.

## Project Architecture

**Tech Stack:** FastAPI + Pydantic + Python 3.10+

**Structure:**
```
backend/app/
├── api.py       # FastAPI routes and endpoints
├── models.py    # Pydantic data models
├── storage.py   # Data access layer (in-memory)
├── utils.py     # Business logic utilities
```

## Coding Standards

### Python Style Guide

**1. Follow PEP 8**
- Line length: 100 characters max
- Indentation: 4 spaces
- Imports: Standard library → Third-party → Local

**2. Type Hints (Required)**
```python
def filter_prompts_by_collection(
    prompts: List[Prompt], 
    collection_id: str
) -> List[Prompt]:
    return [p for p in prompts if p.collection_id == collection_id]
```

**3. Google-Style Docstrings (Required)**
```python
def create_prompt(prompt: Prompt) -> Prompt:
    """Create a new prompt in storage.
    
    Args:
        prompt (Prompt): The prompt object to store.
        
    Returns:
        Prompt: The stored prompt object.
    """
    self._prompts[prompt.id] = prompt
    return prompt
```

### FastAPI Patterns

**1. Endpoint Structure**
```python
@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.
    
    Args:
        prompt_data (PromptCreate): Data for the new prompt.
        
    Returns:
        Prompt: The created prompt object.
        
    Raises:
        HTTPException: If validation fails.
    """
    # Validate foreign keys
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Create and return
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)
```

**2. Status Codes**
- `200`: GET, PUT, PATCH success
- `201`: POST success (resource created)
- `204`: DELETE success (no content)
- `400`: Bad request (validation, foreign key)
- `404`: Resource not found
- `422`: Pydantic validation error

**3. Error Handling**
```python
if not resource:
    raise HTTPException(status_code=404, detail="Resource not found")
```

### Pydantic Model Patterns

**1. Separate Models for Different Operations**
```python
class PromptBase(BaseModel):
    """Base model with common fields."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)

class PromptCreate(PromptBase):
    """Model for creating prompts (no id/timestamps)."""
    pass

class Prompt(BaseModel):
    """Complete model with all fields."""
    title: str
    content: str
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
```

**2. Field Validation**
```python
title: str = Field(..., min_length=1, max_length=200)
description: Optional[str] = Field(None, max_length=500)
```

### Testing Patterns

**1. Test Structure**
```python
class TestPrompts:
    """Tests for prompt endpoints."""
    
    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert "id" in data
```

**2. Use Fixtures**
```python
@pytest.fixture
def sample_prompt_data():
    return {
        "title": "Test Prompt",
        "content": "Test content",
        "description": "Test description"
    }
```

## Useful Patterns for AI Code Generation

### Pattern 1: CRUD Endpoint Template
```python
# CREATE
@app.post("/resources", response_model=Resource, status_code=201)
def create_resource(data: ResourceCreate):
    resource = Resource(**data.model_dump())
    return storage.create_resource(resource)

# READ (List)
@app.get("/resources", response_model=ResourceList)
def list_resources():
    resources = storage.get_all_resources()
    return ResourceList(resources=resources, total=len(resources))

# READ (Single)
@app.get("/resources/{resource_id}", response_model=Resource)
def get_resource(resource_id: str):
    resource = storage.get_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

# UPDATE
@app.put("/resources/{resource_id}", response_model=Resource)
def update_resource(resource_id: str, data: ResourceUpdate):
    existing = storage.get_resource(resource_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    updated = Resource(
        id=existing.id,
        **data.model_dump(),
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    return storage.update_resource(resource_id, updated)

# DELETE
@app.delete("/resources/{resource_id}", status_code=204)
def delete_resource(resource_id: str):
    if not storage.delete_resource(resource_id):
        raise HTTPException(status_code=404, detail="Resource not found")
    return None
```

### Pattern 2: Filtering and Searching
```python
@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    prompts = storage.get_all_prompts()
    
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    if search:
        prompts = search_prompts(prompts, search)
    
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))
```

### Pattern 3: Foreign Key Validation
```python
if prompt_data.collection_id:
    collection = storage.get_collection(prompt_data.collection_id)
    if not collection:
        raise HTTPException(status_code=400, detail="Collection not found")
```

### Pattern 4: Utility Functions
```python
def filter_by_field(items: List[T], field: str, value: Any) -> List[T]:
    """Generic filter function.
    
    Args:
        items (List[T]): Items to filter.
        field (str): Field name to filter by.
        value (Any): Value to match.
        
    Returns:
        List[T]: Filtered items.
    """
    return [item for item in items if getattr(item, field) == value]
```

## Common Tasks

### Adding a New Endpoint

1. **Define Pydantic models** in `models.py`
2. **Add storage methods** in `storage.py`
3. **Create endpoint** in `api.py` with proper:
   - HTTP method and path
   - Response model and status code
   - Google-style docstring
   - Error handling
4. **Write tests** in `tests/test_api.py`
5. **Document in** `docs/API_REFERENCE.md`

### Adding a New Model

1. Create Base, Create, and full model classes
2. Add field validation with Pydantic Field
3. Include Google-style docstring with Attributes
4. Add to response models if needed

### Adding Business Logic

1. Add function to `utils.py`
2. Include type hints and Google-style docstring
3. Keep functions pure (no side effects)
4. Write unit tests

## What NOT to Do

❌ **Don't** skip type hints
❌ **Don't** skip docstrings
❌ **Don't** use generic variable names (x, data, temp)
❌ **Don't** mix business logic in API endpoints
❌ **Don't** forget error handling
❌ **Don't** hardcode values (use constants)
❌ **Don't** skip tests for new features

## Quick Reference

**Import Order:**
```python
# Standard library
from datetime import datetime
from typing import Optional, List

# Third-party
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Local
from app.models import Prompt, PromptCreate
from app.storage import storage
```

**File Locations:**
- API endpoints → `backend/app/api.py`
- Data models → `backend/app/models.py`
- Storage layer → `backend/app/storage.py`
- Utilities → `backend/app/utils.py`
- Tests → `backend/tests/test_api.py`
- API docs → `docs/API_REFERENCE.md`