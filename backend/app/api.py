"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Checks the health of the API.

    Returns:
        HealthResponse: The current status and version of the API.
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """Lists all prompts, with optional filtering by collection or search query.

    Args:
        collection_id (Optional[str]): The ID of the collection to filter prompts by.
        search (Optional[str]): A search query string to filter prompts.

    Returns:
        PromptList: A list of prompts, potentially filtered and sorted by date.
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieves a specific prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to retrieve.

    Returns:
        Prompt: The prompt object if found.

    Raises:
        HTTPException: If the prompt is not found, a 404 error is raised.
    """
    # Retrieve prompt
    prompt = storage.get_prompt(prompt_id)
    
    # Check if prompt exists. If not, raise 404 error.
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    else:
        return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Creates a new prompt.

    Args:
        prompt_data (PromptCreate): Data for the new prompt.

    Returns:
        Prompt: The created prompt object.

    Raises:
        HTTPException: If the specified collection does not exist, a 400 error is raised.
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Updates an existing prompt with new data.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptUpdate): The new data for the prompt.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt or collection does not exist, appropriate errors are raised.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def partial_update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Partially updates an existing prompt with the provided data fields.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptUpdate): The fields to update in the prompt.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt or collection does not exist, appropriate errors are raised.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Update only the fields provided in the request
    updated_data = existing.model_dump()
    update_fields = prompt_data.model_dump(exclude_unset=True)
    updated_data.update(update_fields)
    updated_data['id'] = existing.id
    updated_data['created_at'] = existing.created_at
    updated_data['updated_at'] = get_current_time()
    updated_prompt = Prompt(**updated_data)
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Deletes a prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to delete.

    Returns:
        None: No content is returned upon successful deletion.

    Raises:
        HTTPException: If the prompt is not found, a 404 error is raised.
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """Lists all collections.

    Returns:
        CollectionList: A list of all collections.
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieves a specific collection by its ID.

    Args:
        collection_id (str): The ID of the collection to retrieve.

    Returns:
        Collection: The collection object if found.

    Raises:
        HTTPException: If the collection is not found, a 404 error is raised.
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Creates a new collection.

    Args:
        collection_data (CollectionCreate): Data for the new collection.

    Returns:
        Collection: The created collection object.
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)

@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Deletes a collection by its ID and all associated prompts.

    Args:
        collection_id (str): The ID of the collection to delete.

    Returns:
        None: No content is returned upon successful deletion.

    Raises:
        HTTPException: If the collection is not found, a 404 error is raised.
    """
    # Attempt to delete the collection
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")

    # Retrieve prompts associated with the collection
    prompts = storage.get_prompts_by_collection(collection_id)

    # Delete each prompt associated with the collection
    for prompt in prompts:
        storage.delete_prompt(prompt.id)

    # No return needed for HTTP 204 No Content
    return None
