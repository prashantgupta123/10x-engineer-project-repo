"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection, PromptVersion


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
        self._prompt_versions: Dict[str, PromptVersion] = {}
    
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
        self._prompt_versions.clear()
    
    # ============== Prompt Version Operations ==============
    
    def create_version(self, version: PromptVersion) -> PromptVersion:
        """Create a new prompt version.
        
        Args:
            version (PromptVersion): The version object to store.
            
        Returns:
            PromptVersion: The stored version object.
        """
        self._prompt_versions[version.id] = version
        return version
    
    def get_version(self, version_id: str) -> Optional[PromptVersion]:
        """Retrieve a version by ID.
        
        Args:
            version_id (str): The unique identifier of the version.
            
        Returns:
            Optional[PromptVersion]: The version object if found, None otherwise.
        """
        return self._prompt_versions.get(version_id)
    
    def get_versions_by_prompt(self, prompt_id: str) -> List[PromptVersion]:
        """Get all versions for a specific prompt.
        
        Args:
            prompt_id (str): The unique identifier of the prompt.
            
        Returns:
            List[PromptVersion]: List of versions for the prompt.
        """
        return [v for v in self._prompt_versions.values() if v.prompt_id == prompt_id]
    
    def get_latest_version_number(self, prompt_id: str) -> int:
        """Get the highest version number for a prompt.
        
        Args:
            prompt_id (str): The unique identifier of the prompt.
            
        Returns:
            int: The highest version number, or 0 if no versions exist.
        """
        versions = self.get_versions_by_prompt(prompt_id)
        return max([v.version_number for v in versions], default=0)


# Global storage instance
storage = Storage()
