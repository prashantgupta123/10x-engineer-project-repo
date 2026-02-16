"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """In-memory storage for prompts and collections.
    
    This class provides CRUD operations for prompts and collections using
    in-memory dictionaries. In production, this should be replaced with a
    database implementation.
    
    Attributes:
        _prompts (Dict[str, Prompt]): Dictionary storing prompts by ID.
        _collections (Dict[str, Collection]): Dictionary storing collections by ID.
    """
    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Create a new prompt in storage.
        
        Args:
            prompt (Prompt): The prompt object to store.
            
        Returns:
            Prompt: The stored prompt object.
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its ID.
        
        Args:
            prompt_id (str): The unique identifier of the prompt.
            
        Returns:
            Optional[Prompt]: The prompt object if found, None otherwise.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all prompts from storage.
        
        Returns:
            List[Prompt]: List of all stored prompts.
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt.
        
        Args:
            prompt_id (str): The unique identifier of the prompt to update.
            prompt (Prompt): The updated prompt object.
            
        Returns:
            Optional[Prompt]: The updated prompt if found, None otherwise.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt from storage.
        
        Args:
            prompt_id (str): The unique identifier of the prompt to delete.
            
        Returns:
            bool: True if prompt was deleted, False if not found.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Create a new collection in storage.
        
        Args:
            collection (Collection): The collection object to store.
            
        Returns:
            Collection: The stored collection object.
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its ID.
        
        Args:
            collection_id (str): The unique identifier of the collection.
            
        Returns:
            Optional[Collection]: The collection object if found, None otherwise.
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieve all collections from storage.
        
        Returns:
            List[Collection]: List of all stored collections.
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection from storage.
        
        Args:
            collection_id (str): The unique identifier of the collection to delete.
            
        Returns:
            bool: True if collection was deleted, False if not found.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve all prompts belonging to a specific collection.
        
        Args:
            collection_id (str): The unique identifier of the collection.
            
        Returns:
            List[Prompt]: List of prompts in the specified collection.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Clear all data from storage.
        
        Removes all prompts and collections. Primarily used for testing.
        """
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()
