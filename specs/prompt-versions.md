# Feature Specification: Prompt Versions

## Overview and Goals

### Overview
The Prompt Versions feature enables version control for AI prompts, allowing users to track changes, maintain history, and revert to previous versions. This feature is essential for iterative prompt engineering where teams need to experiment with different variations while preserving the ability to rollback changes.

### Goals
- Enable tracking of all prompt modifications over time
- Allow users to compare different versions side-by-side
- Provide rollback capability to any previous version
- Maintain complete audit trail of prompt evolution
- Support collaborative prompt engineering workflows

### Success Metrics
- Users can create and manage multiple versions per prompt
- Version history is preserved indefinitely
- Revert operations complete in <100ms
- Zero data loss during version operations

---

## User Stories with Acceptance Criteria

### User Story 1: View Version History
**As a** prompt engineer  
**I want to** view all versions of a prompt with their metadata  
**So that** I can understand how the prompt has evolved over time

**Acceptance Criteria:**
- [ ] User can list all versions for a specific prompt
- [ ] Each version shows: version number, title, content preview, created timestamp
- [ ] Versions are sorted by creation date (newest first)
- [ ] API returns versions in under 200ms for prompts with <100 versions
- [ ] Empty version list returns appropriate message

### User Story 2: Create New Version
**As a** prompt engineer  
**I want to** create a new version when updating a prompt  
**So that** I can preserve the previous version while making changes

**Acceptance Criteria:**
- [ ] User can create a new version with title, content, and description
- [ ] Version number auto-increments from the last version
- [ ] Original prompt remains unchanged
- [ ] New version is immediately available in version list
- [ ] Creation timestamp is automatically set
- [ ] Validation ensures required fields are present

### User Story 3: View Specific Version
**As a** prompt engineer  
**I want to** view the complete details of a specific version  
**So that** I can review its exact content and metadata

**Acceptance Criteria:**
- [ ] User can retrieve any version by its ID
- [ ] Response includes all version fields (id, prompt_id, title, content, description, version_number, created_at)
- [ ] Non-existent version returns 404 error
- [ ] Response time is under 100ms

### User Story 4: Revert to Previous Version
**As a** prompt engineer  
**I want to** revert a prompt to a previous version  
**So that** I can undo unwanted changes quickly

**Acceptance Criteria:**
- [ ] User can revert to any previous version by version ID
- [ ] Revert creates a new version (doesn't delete history)
- [ ] New version contains content from the selected previous version
- [ ] Version number increments (e.g., v5 reverted to v2 creates v6 with v2's content)
- [ ] Revert operation is atomic (all-or-nothing)
- [ ] User receives confirmation of successful revert

---

## Data Model Changes

### New Model: PromptVersion

```python
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
```

### Storage Layer Changes

```python
class Storage:
    def __init__(self):
        self._prompt_versions: Dict[str, PromptVersion] = {}
    
    def create_version(self, version: PromptVersion) -> PromptVersion:
        """Create a new prompt version."""
        self._prompt_versions[version.id] = version
        return version
    
    def get_version(self, version_id: str) -> Optional[PromptVersion]:
        """Retrieve a version by ID."""
        return self._prompt_versions.get(version_id)
    
    def get_versions_by_prompt(self, prompt_id: str) -> List[PromptVersion]:
        """Get all versions for a specific prompt."""
        return [v for v in self._prompt_versions.values() if v.prompt_id == prompt_id]
    
    def get_latest_version_number(self, prompt_id: str) -> int:
        """Get the highest version number for a prompt."""
        versions = self.get_versions_by_prompt(prompt_id)
        return max([v.version_number for v in versions], default=0)
```

---

## API Endpoints with Request/Response

### 1. List Prompt Versions

**Endpoint:** `GET /prompts/{prompt_id}/versions`

**Description:** Retrieve all versions of a specific prompt, sorted by version number (newest first).

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |

**Request Example:**
```bash
curl http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/versions
```

**Response (200 OK):**
```json
{
  "versions": [
    {
      "id": "ver-123",
      "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Email Template v3",
      "content": "You are a helpful assistant...",
      "description": "Added personalization tokens",
      "version_number": 3,
      "created_at": "2024-01-15T14:30:00.000Z"
    },
    {
      "id": "ver-122",
      "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Email Template v2",
      "content": "You are a helpful assistant...",
      "description": "Improved tone",
      "version_number": 2,
      "created_at": "2024-01-15T12:00:00.000Z"
    }
  ],
  "total": 2
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Prompt not found"
}
```

---

### 2. Get Specific Prompt Version

**Endpoint:** `GET /prompts/{prompt_id}/versions/{version_id}`

**Description:** Retrieve a specific version of a prompt by its ID.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |
| version_id | string | Yes | Unique version identifier |

**Request Example:**
```bash
curl http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/versions/ver-123
```

**Response (200 OK):**
```json
{
  "id": "ver-123",
  "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Email Template v3",
  "content": "You are a helpful assistant. Respond professionally to: {{email_content}}",
  "description": "Added personalization tokens",
  "version_number": 3,
  "created_at": "2024-01-15T14:30:00.000Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Version not found"
}
```

---

### 3. Create New Version

**Endpoint:** `POST /prompts/{prompt_id}/versions`

**Description:** Create a new version for a specified prompt. Version number auto-increments.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Version title (1-200 chars) |
| content | string | Yes | Version content (min 1 char) |
| description | string | No | Description of changes (max 500 chars) |

**Request Example:**
```bash
curl -X POST http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/versions \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Email Template v4",
    "content": "You are a helpful assistant. Respond professionally and empathetically to: {{email_content}}",
    "description": "Added empathy instruction"
  }'
```

**Response (201 Created):**
```json
{
  "id": "ver-124",
  "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Email Template v4",
  "content": "You are a helpful assistant. Respond professionally and empathetically to: {{email_content}}",
  "description": "Added empathy instruction",
  "version_number": 4,
  "created_at": "2024-01-15T15:00:00.000Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Prompt not found"
}
```

**Error Response (422 Validation Error):**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### 4. Revert to Previous Version

**Endpoint:** `POST /prompts/{prompt_id}/versions/{version_id}/revert`

**Description:** Revert the prompt to a specified version by creating a new version with the old content.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |
| version_id | string | Yes | Version ID to revert to |

**Request Example:**
```bash
curl -X POST http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000/versions/ver-122/revert
```

**Response (201 Created):**
```json
{
  "id": "ver-125",
  "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Email Template v2",
  "content": "You are a helpful assistant...",
  "description": "Reverted to version 2",
  "version_number": 5,
  "created_at": "2024-01-15T16:00:00.000Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Version not found"
}
```

---

## Edge Cases Considered

### 1. Prompt Doesn't Exist
**Scenario:** User tries to create version for non-existent prompt  
**Handling:** Return 404 with message "Prompt not found"  
**Test:** Attempt to create version with invalid prompt_id

### 2. Version Doesn't Exist
**Scenario:** User tries to retrieve or revert to non-existent version  
**Handling:** Return 404 with message "Version not found"  
**Test:** Request version with invalid version_id

### 3. No Versions Exist
**Scenario:** User lists versions for prompt with no versions  
**Handling:** Return empty list with total=0  
**Test:** List versions for newly created prompt

### 4. Concurrent Version Creation
**Scenario:** Two users create versions simultaneously  
**Handling:** Both succeed with sequential version numbers (use atomic increment)  
**Test:** Simulate concurrent POST requests

### 5. Large Content
**Scenario:** User creates version with very large content (>1MB)  
**Handling:** Accept but consider adding max length validation in future  
**Test:** Create version with 1MB+ content

### 6. Revert to Current Version
**Scenario:** User reverts to the latest version  
**Handling:** Allow operation, creates duplicate version  
**Test:** Revert to version_number = max(version_number)

### 7. Version Number Gaps
**Scenario:** Versions deleted (future feature) causing gaps  
**Handling:** Version numbers continue incrementing, gaps are acceptable  
**Test:** Verify version_number increments correctly

### 8. Empty Description
**Scenario:** User creates version without description  
**Handling:** Accept, description is optional (null)  
**Test:** Create version with description=null

### 9. Special Characters in Content
**Scenario:** Content contains special characters, emojis, unicode  
**Handling:** Accept all valid UTF-8 characters  
**Test:** Create version with emojis and special characters

### 10. Prompt Deletion
**Scenario:** Prompt is deleted but versions exist  
**Handling:** Cascade delete all versions OR keep versions orphaned (design decision)  
**Test:** Delete prompt and verify version behavior

---

## Implementation Notes

### Phase 1: Core Functionality
- Implement basic CRUD operations for versions
- Add version number auto-increment logic
- Implement revert functionality

### Phase 2: Enhancements
- Add version comparison (diff view)
- Add version search/filter
- Add version tags/labels

### Phase 3: Advanced Features
- Add version branching
- Add merge capabilities
- Add collaborative editing with conflict resolution

### Database Considerations
- Index on `prompt_id` for fast version lookups
- Index on `version_number` for sorting
- Consider partitioning by prompt_id for large datasets

### Performance Targets
- List versions: <200ms for 100 versions
- Get version: <100ms
- Create version: <150ms
- Revert: <200ms

---

## Testing Checklist

- [ ] Unit tests for all storage methods
- [ ] Integration tests for all endpoints
- [ ] Test version number auto-increment
- [ ] Test revert creates new version
- [ ] Test concurrent version creation
- [ ] Test all error scenarios (404, 422)
- [ ] Test with empty version list
- [ ] Test with large content
- [ ] Performance test with 100+ versions
- [ ] Test cascade delete behavior