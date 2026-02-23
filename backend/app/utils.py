"""Utility functions for PromptLab"""

from typing import List
from fastapi import HTTPException
from app.models import Prompt, Collection


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by creation date.
    
    Args:
        prompts (List[Prompt]): List of prompts to sort.
        descending (bool): If True, newest prompts first. Defaults to True.
        
    Returns:
        List[Prompt]: Sorted list of prompts.
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by collection ID.
    
    Args:
        prompts (List[Prompt]): List of prompts to filter.
        collection_id (str): The collection ID to filter by.
        
    Returns:
        List[Prompt]: Prompts belonging to the specified collection.
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by query string in title and description.
    
    Args:
        prompts (List[Prompt]): List of prompts to search.
        query (str): Search query string (case-insensitive).
        
    Returns:
        List[Prompt]: Prompts matching the search query.
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Validate prompt content meets minimum requirements.
    
    Args:
        content (str): The prompt content to validate.
        
    Returns:
        bool: True if content is valid, False otherwise.
        
    Note:
        Valid content must be:
        - Not empty
        - Not just whitespace
        - At least 10 characters long
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    Args:
        content (str): The prompt content to parse.
        
    Returns:
        List[str]: List of variable names found in the content.
        
    Note:
        Variables must be in the format {{variable_name}}.
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)


def get_prompt_or_404(prompt_id: str) -> Prompt:
    """Retrieve prompt by ID or raise 404 error if not found."""
    from app.storage import storage
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


def get_collection_or_404(collection_id: str) -> Collection:
    """Retrieve collection by ID or raise 404 error if not found."""
    from app.storage import storage
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

