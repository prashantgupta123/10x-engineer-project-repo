# API Reference

Complete API documentation for PromptLab - AI Prompt Engineering Platform.

**Base URL:** `http://localhost:8000`

**Version:** 0.1.0

---

## Table of Contents

- [Authentication](#authentication)
- [Health Check](#health-check)
- [Prompts](#prompts)
  - [List Prompts](#list-prompts)
  - [Get Prompt](#get-prompt)
  - [Create Prompt](#create-prompt)
  - [Update Prompt (PUT)](#update-prompt-put)
  - [Update Prompt (PATCH)](#update-prompt-patch)
  - [Delete Prompt](#delete-prompt)
- [Collections](#collections)
  - [List Collections](#list-collections)
  - [Get Collection](#get-collection)
  - [Create Collection](#create-collection)
  - [Delete Collection](#delete-collection)
- [Error Responses](#error-responses)

---

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

**Note:** Authentication will be added in future versions using JWT tokens.

---

## Health Check

### Check API Health

Check the health status and version of the API.

**Endpoint:** `GET /health`

**Request Example (curl):**
```bash
curl http://localhost:8000/health
```

**Request Example (fetch):**
```javascript
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log(data));
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

---

## Prompts

### List Prompts

Retrieve all prompts with optional filtering and searching.

**Endpoint:** `GET /prompts`

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| collection_id | string | No | Filter prompts by collection ID |
| search | string | No | Search in title and description |

**Request Example (curl):**
```bash
# Get all prompts
curl http://localhost:8000/prompts

# Filter by collection
curl "http://localhost:8000/prompts?collection_id=abc-123"

# Search prompts
curl "http://localhost:8000/prompts?search=email"

# Combine filters
curl "http://localhost:8000/prompts?collection_id=abc-123&search=template"
```

**Request Example (fetch):**
```javascript
// Get all prompts
fetch('http://localhost:8000/prompts')
  .then(response => response.json())
  .then(data => console.log(data));

// With filters
fetch('http://localhost:8000/prompts?collection_id=abc-123&search=email')
  .then(response => response.json())
  .then(data => console.log(data));
```

**Response (200 OK):**
```json
{
  "prompts": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Email Response Template",
      "content": "You are a helpful customer support agent. Respond to this email professionally: {{email_content}}",
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

### Get Prompt

Retrieve a specific prompt by ID.

**Endpoint:** `GET /prompts/{prompt_id}`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |

**Request Example (curl):**
```bash
curl http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000
```

**Request Example (fetch):**
```javascript
fetch('http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000')
  .then(response => response.json())
  .then(data => console.log(data));
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Email Response Template",
  "content": "You are a helpful customer support agent. Respond to this email professionally: {{email_content}}",
  "description": "Template for generating email responses",
  "collection_id": "abc-123",
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T10:30:00.000Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Prompt not found"
}
```

---

### Create Prompt

Create a new prompt.

**Endpoint:** `POST /prompts`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Prompt title (1-200 chars) |
| content | string | Yes | Prompt content (min 1 char) |
| description | string | No | Optional description (max 500 chars) |
| collection_id | string | No | Optional collection ID |

**Request Example (curl):**
```bash
curl -X POST http://localhost:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Email Response Template",
    "content": "You are a helpful customer support agent. Respond to this email professionally: {{email_content}}",
    "description": "Template for generating email responses",
    "collection_id": "abc-123"
  }'
```

**Request Example (fetch):**
```javascript
fetch('http://localhost:8000/prompts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'Email Response Template',
    content: 'You are a helpful customer support agent. Respond to this email professionally: {{email_content}}',
    description: 'Template for generating email responses',
    collection_id: 'abc-123'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Email Response Template",
  "content": "You are a helpful customer support agent. Respond to this email professionally: {{email_content}}",
  "description": "Template for generating email responses",
  "collection_id": "abc-123",
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T10:30:00.000Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Collection not found"
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

### Update Prompt (PUT)

Fully update an existing prompt. All fields must be provided.

**Endpoint:** `PUT /prompts/{prompt_id}`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Prompt title (1-200 chars) |
| content | string | Yes | Prompt content (min 1 char) |
| description | string | No | Optional description (max 500 chars) |
| collection_id | string | No | Optional collection ID |

**Request Example (curl):**
```bash
curl -X PUT http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Email Template",
    "content": "Updated content for the prompt",
    "description": "Updated description",
    "collection_id": "abc-123"
  }'
```

**Request Example (fetch):**
```javascript
fetch('http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'Updated Email Template',
    content: 'Updated content for the prompt',
    description: 'Updated description',
    collection_id: 'abc-123'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated Email Template",
  "content": "Updated content for the prompt",
  "description": "Updated description",
  "collection_id": "abc-123",
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T11:45:00.000Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Prompt not found"
}
```

---

### Update Prompt (PATCH)

Partially update an existing prompt. Only provided fields will be updated.

**Endpoint:** `PATCH /prompts/{prompt_id}`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | No | Prompt title (1-200 chars) |
| content | string | No | Prompt content (min 1 char) |
| description | string | No | Optional description (max 500 chars) |
| collection_id | string | No | Optional collection ID |

**Request Example (curl):**
```bash
curl -X PATCH http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Only Update Title"
  }'
```

**Request Example (fetch):**
```javascript
fetch('http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'Only Update Title'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Only Update Title",
  "content": "Original content remains unchanged",
  "description": "Original description remains unchanged",
  "collection_id": "abc-123",
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T12:00:00.000Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Prompt not found"
}
```

---

### Delete Prompt

Delete a prompt by ID.

**Endpoint:** `DELETE /prompts/{prompt_id}`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt_id | string | Yes | Unique prompt identifier |

**Request Example (curl):**
```bash
curl -X DELETE http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000
```

**Request Example (fetch):**
```javascript
fetch('http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000', {
  method: 'DELETE'
})
  .then(response => {
    if (response.status === 204) {
      console.log('Prompt deleted successfully');
    }
  });
```

**Response (204 No Content):**
```
No response body
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Prompt not found"
}
```

---

## Collections

### List Collections

Retrieve all collections.

**Endpoint:** `GET /collections`

**Request Example (curl):**
```bash
curl http://localhost:8000/collections
```

**Request Example (fetch):**
```javascript
fetch('http://localhost:8000/collections')
  .then(response => response.json())
  .then(data => console.log(data));
```

**Response (200 OK):**
```json
{
  "collections": [
    {
      "id": "abc-123",
      "name": "Customer Support",
      "description": "Prompts for customer service automation",
      "created_at": "2024-01-15T09:00:00.000Z"
    },
    {
      "id": "def-456",
      "name": "Marketing",
      "description": "Marketing and content generation prompts",
      "created_at": "2024-01-15T09:15:00.000Z"
    }
  ],
  "total": 2
}
```

---

### Get Collection

Retrieve a specific collection by ID.

**Endpoint:** `GET /collections/{collection_id}`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| collection_id | string | Yes | Unique collection identifier |

**Request Example (curl):**
```bash
curl http://localhost:8000/collections/abc-123
```

**Request Example (fetch):**
```javascript
fetch('http://localhost:8000/collections/abc-123')
  .then(response => response.json())
  .then(data => console.log(data));
```

**Response (200 OK):**
```json
{
  "id": "abc-123",
  "name": "Customer Support",
  "description": "Prompts for customer service automation",
  "created_at": "2024-01-15T09:00:00.000Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Collection not found"
}
```

---

### Create Collection

Create a new collection.

**Endpoint:** `POST /collections`

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Collection name (1-100 chars) |
| description | string | No | Optional description (max 500 chars) |

**Request Example (curl):**
```bash
curl -X POST http://localhost:8000/collections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Support",
    "description": "Prompts for customer service automation"
  }'
```

**Request Example (fetch):**
```javascript
fetch('http://localhost:8000/collections', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'Customer Support',
    description: 'Prompts for customer service automation'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

**Response (201 Created):**
```json
{
  "id": "abc-123",
  "name": "Customer Support",
  "description": "Prompts for customer service automation",
  "created_at": "2024-01-15T09:00:00.000Z"
}
```

**Error Response (422 Validation Error):**
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### Delete Collection

Delete a collection and all associated prompts.

**Endpoint:** `DELETE /collections/{collection_id}`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| collection_id | string | Yes | Unique collection identifier |

**Request Example (curl):**
```bash
curl -X DELETE http://localhost:8000/collections/abc-123
```

**Request Example (fetch):**
```javascript
fetch('http://localhost:8000/collections/abc-123', {
  method: 'DELETE'
})
  .then(response => {
    if (response.status === 204) {
      console.log('Collection deleted successfully');
    }
  });
```

**Response (204 No Content):**
```
No response body
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Collection not found"
}
```

**Note:** Deleting a collection will also delete all prompts associated with that collection.

---

## Error Responses

The API uses standard HTTP status codes and returns error details in JSON format.

### HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created successfully |
| 204 | No Content - Request succeeded, no response body |
| 400 | Bad Request - Invalid request or validation error |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

### Error Response Format

All error responses follow this structure:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Validation Error Format

Validation errors (422) provide detailed information about each invalid field:

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error description",
      "type": "error_type"
    }
  ]
}
```

**Example Validation Errors:**

**Missing Required Field:**
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

**String Too Short:**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

**String Too Long:**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at most 200 characters",
      "type": "value_error.any_str.max_length"
    }
  ]
}
```

### Common Error Scenarios

**1. Resource Not Found (404)**
```json
{
  "detail": "Prompt not found"
}
```
```json
{
  "detail": "Collection not found"
}
```

**2. Invalid Collection Reference (400)**
```json
{
  "detail": "Collection not found"
}
```
Occurs when creating/updating a prompt with a non-existent collection_id.

**3. Validation Error (422)**
```json
{
  "detail": [
    {
      "loc": ["body", "content"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Interactive Documentation

For interactive API documentation and testing, visit:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

These interfaces allow you to:
- View all endpoints and their parameters
- Test API calls directly from the browser
- See request/response schemas
- Download OpenAPI specification

---

## Rate Limiting

Currently, there are no rate limits on API requests.

**Note:** Rate limiting will be implemented in future versions for production use.

---

## Versioning

The API version is included in the health check response. Currently at version `0.1.0`.

Future versions may introduce breaking changes with appropriate version prefixes in the URL (e.g., `/v2/prompts`).

---

## Support

For issues, questions, or feature requests:
- **GitHub Issues:** https://github.com/prashantgupta123/10x-engineer-project-repo/issues
- **Email:** prashant.gupta@tothenew.com
