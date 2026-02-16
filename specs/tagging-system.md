# Feature Specification: Tagging System

## Overview and Goals

### Overview
The Tagging System enables users to organize and categorize prompts using flexible, user-defined tags. This feature enhances discoverability, allows for multi-dimensional organization beyond collections, and supports advanced filtering and search capabilities.

### Goals
- Enable flexible categorization of prompts using tags
- Support multiple tags per prompt
- Provide fast tag-based search and filtering
- Allow tag reuse across multiple prompts
- Maintain tag consistency and prevent duplicates

### Success Metrics
- Users can tag prompts with multiple tags
- Tag-based search returns results in <200ms
- Tags can be reused across unlimited prompts
- Zero duplicate tags in the system
- Tag operations complete in <100ms

---

## User Stories with Acceptance Criteria

### User Story 1: Create and Manage Tags
**As a** prompt engineer  
**I want to** create reusable tags with descriptive names  
**So that** I can build a consistent taxonomy for organizing prompts

**Acceptance Criteria:**
- [ ] User can create a tag with name and optional description
- [ ] Tag names are unique (case-insensitive)
- [ ] Tag names are 1-50 characters
- [ ] User can list all available tags
- [ ] Tags show usage count (number of prompts)
- [ ] Empty tag list returns appropriate message

### User Story 2: Add Tags to Prompts
**As a** prompt engineer  
**I want to** attach multiple tags to a prompt  
**So that** I can categorize it across different dimensions

**Acceptance Criteria:**
- [ ] User can add one or more tags to a prompt
- [ ] Same tag cannot be added twice to the same prompt
- [ ] Tag must exist before being added to prompt
- [ ] Adding tag returns confirmation
- [ ] Operation is idempotent (adding existing tag is no-op)

### User Story 3: Remove Tags from Prompts
**As a** prompt engineer  
**I want to** remove tags from prompts  
**So that** I can update categorization as needs change

**Acceptance Criteria:**
- [ ] User can remove any tag from a prompt
- [ ] Removing non-existent tag returns 404
- [ ] Removal doesn't delete the tag itself
- [ ] Operation completes in <100ms

### User Story 4: View Prompt Tags
**As a** prompt engineer  
**I want to** see all tags attached to a prompt  
**So that** I understand how it's categorized

**Acceptance Criteria:**
- [ ] User can list all tags for a specific prompt
- [ ] Tags are returned with full details (id, name, description)
- [ ] Empty tag list returns empty array
- [ ] Response time is under 100ms

### User Story 5: Search Prompts by Tags
**As a** prompt engineer  
**I want to** find prompts by one or more tags  
**So that** I can quickly locate related prompts

**Acceptance Criteria:**
- [ ] User can search prompts by single tag name
- [ ] User can search prompts by multiple tags (AND logic)
- [ ] Search returns prompts with all specified tags
- [ ] Results include full prompt details
- [ ] Search completes in <200ms for 1000+ prompts
- [ ] Non-existent tag returns empty results

### User Story 6: Delete Tags
**As a** prompt engineer  
**I want to** delete unused tags  
**So that** I can keep the tag list clean and relevant

**Acceptance Criteria:**
- [ ] User can delete a tag by ID
- [ ] Deleting tag removes all prompt-tag associations
- [ ] Deletion is permanent and cannot be undone
- [ ] Deleting non-existent tag returns 404
- [ ] Confirmation message is returned

---

## Data Model Changes

### New Model: Tag

```python
class TagBase(BaseModel):
    """Base model for tag data.
    
    Attributes:
        name (str): Tag name, 1-50 characters, unique.
        description (Optional[str]): Optional description, max 200 characters.
    """
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)

class TagCreate(TagBase):
    """Model for creating a new tag.
    
    Inherits all fields from TagBase.
    """
    pass

class Tag(BaseModel):
    """Complete tag model with all fields.
    
    Attributes:
        id (str): Unique identifier, auto-generated.
        name (str): Tag name, 1-50 characters, unique.
        description (Optional[str]): Optional description.
        created_at (datetime): Creation timestamp, auto-generated.
    """
    id: str = Field(default_factory=generate_id)
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    created_at: datetime = Field(default_factory=get_current_time)

    model_config = {
        'from_attributes': True
    }

class TagList(BaseModel):
    """Response model for list of tags.
    
    Attributes:
        tags (List[Tag]): List of tag objects.
        total (int): Total count of tags.
    """
    tags: List[Tag]
    total: int
```

### New Model: PromptTag (Association)

```python
class PromptTag(BaseModel):
    """Association model linking prompts to tags.
    
    Attributes:
        prompt_id (str): ID of the prompt.
        tag_id (str): ID of the tag.
        created_at (datetime): When the tag was added to the prompt.
    """
    prompt_id: str
    tag_id: str
    created_at: datetime = Field(default_factory=get_current_time)

    model_config = {
        'from_attributes': True
    }
```

### Storage Layer Changes

```python
class Storage:
    def __init__(self):
        self._tags: Dict[str, Tag] = {}
        self._prompt_tags: List[PromptTag] = []  # Many-to-many relationship
    
    # Tag operations
    def create_tag(self, tag: Tag) -> Tag:
        """Create a new tag."""
        self._tags[tag.id] = tag
        return tag
    
    def get_tag(self, tag_id: str) -> Optional[Tag]:
        """Retrieve a tag by ID."""
        return self._tags.get(tag_id)
    
    def get_tag_by_name(self, name: str) -> Optional[Tag]:
        """Retrieve a tag by name (case-insensitive)."""
        name_lower = name.lower()
        return next((t for t in self._tags.values() if t.name.lower() == name_lower), None)
    
    def get_all_tags(self) -> List[Tag]:
        """Get all tags."""
        return list(self._tags.values())
    
    def delete_tag(self, tag_id: str) -> bool:
        """Delete a tag and all its associations."""
        if tag_id in self._tags:
            del self._tags[tag_id]
            # Remove all prompt-tag associations
            self._prompt_tags = [pt for pt in self._prompt_tags if pt.tag_id != tag_id]
            return True
        return False
    
    # Prompt-Tag association operations
    def add_tag_to_prompt(self, prompt_id: str, tag_id: str) -> PromptTag:
        """Add a tag to a prompt."""
        # Check if association already exists
        existing = self.get_prompt_tag(prompt_id, tag_id)
        if existing:
            return existing
        
        prompt_tag = PromptTag(prompt_id=prompt_id, tag_id=tag_id)
        self._prompt_tags.append(prompt_tag)
        return prompt_tag
    
    def remove_tag_from_prompt(self, prompt_id: str, tag_id: str) -> bool:
        """Remove a tag from a prompt."""
        initial_length = len(self._prompt_tags)
        self._prompt_tags = [
            pt for pt in self._prompt_tags 
            if not (pt.prompt_id == prompt_id and pt.tag_id == tag_id)
        ]
        return len(self._prompt_tags) < initial_length
    
    def get_prompt_tag(self, prompt_id: str, tag_id: str) -> Optional[PromptTag]:
        """Check if a prompt-tag association exists."""
        return next(
            (pt for pt in self._prompt_tags if pt.prompt_id == prompt_id and pt.tag_id == tag_id),
            None
        )
    
    def get_tags_for_prompt(self, prompt_id: str) -> List[Tag]:
        """Get all tags for a specific prompt."""
        tag_ids = [pt.tag_id for pt in self._prompt_tags if pt.prompt_id == prompt_id]
        return [self._tags[tid] for tid in tag_ids if tid in self._tags]
    
    def get_prompts_by_tag(self, tag_id: str) -> List[Prompt]:
        """Get all prompts with a specific tag."""
        prompt_ids = [pt.prompt_id for pt in self._prompt_tags if pt.tag_id == tag_id]
        return [self._prompts[pid] for pid in prompt_ids if pid in self._prompts]
    
    def get_prompts_by_tags(self, tag_ids: List[str]) -> List[Prompt]:
        """Get prompts that have ALL specified tags (AND logic)."""
        if not tag_ids:
            return []
        
        # Get prompts for first tag
        prompt_ids = set(pt.prompt_id for pt in self._prompt_tags if pt.tag_id == tag_ids[0])
        
        # Intersect with prompts for remaining tags
        for tag_id in tag_ids[1:]:
            tag_prompt_ids = set(pt.prompt_id for pt in self._prompt_tags if pt.tag_id == tag_id)
            prompt_ids = prompt_ids.intersection(tag_prompt_ids)
        
        return [self._prompts[pid] for pid in prompt_ids if pid in self._prompts]
```

---

## API Endpoints with Request/Response

### 1. List All Tags

**Endpoint:** `GET /tags`

**Description:** Retrieve all available tags in the system.

**Request Example:**
```bash
curl http://localhost:8000/tags
```

**Response (200 OK):**
```json
{
  "tags": [
    {
      "id": "tag-001",
      "name": "customer-support",
      "description": "Prompts for customer service interactions",
      "created_at": "2024-01-15T10:00:00.000Z"
    },
    {
      "id": "tag-002",
      "name": "email",
      "description": "Email-related prompts",
      "created_at": "2024-01-15T10:05:00.000Z"
    }
  ],
  "total": 2
}
```

---

### 2. Create Tag

**Endpoint:** `POST /tags`

**Description:** Create a new tag. Tag names must be unique (case-insensitive).

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Tag name (1-50 chars, unique) |
| description | string | No | Optional description (max 200 chars) |

**Request Example:**
```bash
curl -X POST http://localhost:8000/tags \
  -H "Content-Type: application/json" \
  -d '{
    "name": "marketing",
    "description": "Marketing and content generation prompts"
  }'
```

**Response (201 Created):**
```json
{
  "id": "tag-003",
  "name": "marketing",
  "description": "Marketing and content generation prompts",
  "created_at": "2024-01-15T11:00:00.000Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Tag with name 'marketing' already exists"
}
```

---

### 3. Get Tag

**Endpoint:** `GET /tags/{tag_id}`

**Description:** Retrieve a specific tag by its ID.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tag_id | string | Yes | Unique tag identifier |

**Request Example:**
```bash
curl http://localhost:8000/tags/tag-001
```

**Response (200 OK):**
```json
{
  "id": "tag-001",
  "name": "customer-support",
  "description": "Prompts for customer service interactions",
  "created_at": "2024-01-15T10:00:00.000Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Tag not found"
}
```

---

### 4. Delete Tag

**Endpoint:** `DELETE /tags/{tag_id}`

**Description:** Delete a tag and remove it from all prompts.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tag_id | string | Yes | Unique tag identifier |

**Request Example:**
```bash
curl -X DELETE http://localhost:8000/tags/tag-003
```

**Response (204 No Content):**
```
No response body
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Tag not found"
}
```

---

### 5. Add Tag to Prompt

**Endpoint:** `POST /prompts/{prompt_id}/tags/{tag_id}`

**Description:** Attach a tag to a prompt. Operation is idempotent.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |
| tag_id | string | Yes | Unique tag identifier |

**Request Example:**
```bash
curl -X POST http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/tags/tag-001
```

**Response (201 Created):**
```json
{
  "message": "Tag added to prompt successfully",
  "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
  "tag_id": "tag-001"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Prompt not found"
}
```
```json
{
  "detail": "Tag not found"
}
```

---

### 6. Remove Tag from Prompt

**Endpoint:** `DELETE /prompts/{prompt_id}/tags/{tag_id}`

**Description:** Remove a tag from a prompt.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |
| tag_id | string | Yes | Unique tag identifier |

**Request Example:**
```bash
curl -X DELETE http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/tags/tag-001
```

**Response (204 No Content):**
```
No response body
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Tag association not found"
}
```

---

### 7. List Tags for Prompt

**Endpoint:** `GET /prompts/{prompt_id}/tags`

**Description:** Retrieve all tags attached to a specific prompt.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |

**Request Example:**
```bash
curl http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/tags
```

**Response (200 OK):**
```json
{
  "tags": [
    {
      "id": "tag-001",
      "name": "customer-support",
      "description": "Prompts for customer service interactions",
      "created_at": "2024-01-15T10:00:00.000Z"
    },
    {
      "id": "tag-002",
      "name": "email",
      "description": "Email-related prompts",
      "created_at": "2024-01-15T10:05:00.000Z"
    }
  ],
  "total": 2
}
```

---

### 8. Search Prompts by Tags

**Endpoint:** `GET /prompts?tags={tag_names}`

**Description:** Find prompts that have all specified tags (AND logic). Extends existing /prompts endpoint.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tags | string | No | Comma-separated tag names |
| collection_id | string | No | Filter by collection (existing) |
| search | string | No | Search query (existing) |

**Request Example:**
```bash
# Single tag
curl "http://localhost:8000/prompts?tags=customer-support"

# Multiple tags (AND logic)
curl "http://localhost:8000/prompts?tags=customer-support,email"

# Combine with other filters
curl "http://localhost:8000/prompts?tags=email&collection_id=abc-123&search=template"
```

**Response (200 OK):**
```json
{
  "prompts": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Email Response Template",
      "content": "You are a helpful customer support agent...",
      "description": "Template for generating email responses",
      "collection_id": "abc-123",
      "created_at": "2024-01-15T10:30:00.000Z",
      "updated_at": "2024-01-15T10:30:00.000Z"
    }
  ],
  "total": 1
}
```

---

## Edge Cases Considered

### 1. Duplicate Tag Names
**Scenario:** User tries to create tag with existing name (case-insensitive)  
**Handling:** Return 400 with message "Tag with name 'X' already exists"  
**Test:** Create tag "Email", then try "email" or "EMAIL"

### 2. Tag Doesn't Exist
**Scenario:** User tries to add non-existent tag to prompt  
**Handling:** Return 404 with message "Tag not found"  
**Test:** POST /prompts/{id}/tags/invalid-tag-id

### 3. Prompt Doesn't Exist
**Scenario:** User tries to add tag to non-existent prompt  
**Handling:** Return 404 with message "Prompt not found"  
**Test:** POST /prompts/invalid-id/tags/{tag_id}

### 4. Adding Same Tag Twice
**Scenario:** User adds tag that's already on the prompt  
**Handling:** Idempotent operation, return 201 (no error)  
**Test:** Add same tag twice, verify only one association exists

### 5. Removing Non-Existent Association
**Scenario:** User removes tag that's not on the prompt  
**Handling:** Return 404 with message "Tag association not found"  
**Test:** DELETE tag that was never added

### 6. Deleting Tag in Use
**Scenario:** User deletes tag that's attached to prompts  
**Handling:** Delete tag and remove all associations (cascade)  
**Test:** Delete tag, verify it's removed from all prompts

### 7. Empty Tag Name
**Scenario:** User creates tag with empty or whitespace-only name  
**Handling:** Pydantic validation returns 422  
**Test:** POST with name="" or name="   "

### 8. Tag Name Too Long
**Scenario:** User creates tag with name >50 characters  
**Handling:** Pydantic validation returns 422  
**Test:** POST with 51-character name

### 9. Search with Non-Existent Tag
**Scenario:** User searches prompts by tag that doesn't exist  
**Handling:** Return empty results (not an error)  
**Test:** GET /prompts?tags=nonexistent

### 10. Multiple Tags Search (AND Logic)
**Scenario:** User searches with multiple tags  
**Handling:** Return only prompts that have ALL specified tags  
**Test:** Search with tags=A,B, verify results have both tags

### 11. Special Characters in Tag Names
**Scenario:** Tag name contains special characters, spaces, unicode  
**Handling:** Accept all valid characters (allow spaces, hyphens, underscores)  
**Test:** Create tag "customer-support", "AI/ML", "email 📧"

### 12. Prompt Deletion with Tags
**Scenario:** Prompt is deleted but has tags  
**Handling:** Cascade delete all prompt-tag associations  
**Test:** Delete prompt, verify associations are removed

---

## Implementation Notes

### Phase 1: Core Functionality
- Implement tag CRUD operations
- Implement prompt-tag associations
- Add tag-based filtering to existing /prompts endpoint

### Phase 2: Enhancements
- Add tag usage statistics (count of prompts per tag)
- Add tag autocomplete/suggestions
- Add bulk tag operations

### Phase 3: Advanced Features
- Add tag hierarchies (parent-child relationships)
- Add tag synonyms
- Add tag-based analytics

### Database Considerations
- Index on tag name for uniqueness check
- Index on prompt_id and tag_id for fast lookups
- Consider separate junction table for many-to-many relationship

### Performance Targets
- List tags: <100ms
- Create tag: <100ms
- Add tag to prompt: <100ms
- Search by tags: <200ms for 1000+ prompts

---

## Testing Checklist

- [ ] Unit tests for all storage methods
- [ ] Integration tests for all endpoints
- [ ] Test tag name uniqueness (case-insensitive)
- [ ] Test idempotent tag addition
- [ ] Test cascade delete on tag deletion
- [ ] Test AND logic for multiple tag search
- [ ] Test all error scenarios (404, 400, 422)
- [ ] Test with special characters in tag names
- [ ] Test with empty tag list
- [ ] Performance test with 100+ tags and 1000+ prompts