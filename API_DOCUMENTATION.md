# PromptLab API Documentation

Welcome to the PromptLab API, an AI Prompt Engineering Platform, designed to manage prompts and collections through a RESTful interface. This documentation provides an overview of each endpoint, its parameters, expected responses, and potential error codes.

## API Details

- **Title**: PromptLab API
- **Description**: AI Prompt Engineering Platform
- **Version**: [Insert API Version]

## Base URL

Replace `[BASE_URL]` with your server's URL:

```
http://[BASE_URL]
```

## CORS Middleware

- Allows all origins (`*`)
- Allows credentials
- Allows all methods
- Allows all headers

## Endpoints

### Health Check

#### `GET /health`

- **Response**
  - Status: 200
  - Body:
    ```json
    {
      "status": "healthy",
      "version": "[API Version]"
    }
    ```

- **cURL**
  ```bash
  curl -X GET http://[BASE_URL]/health
  ```

### Prompts

#### List Prompts

- **Query Parameters**
  - `collection_id` (Optional): Filter prompts by collection ID.
  - `search` (Optional): Perform a text search on prompts.
- **Response**
  - Status: 200
  - Body: List of prompts.
- **Notes**
  - Prompts are sorted by date, newest first.

- **cURL**
  ```bash
  curl -X GET 'http://[BASE_URL]/prompts?collection_id=[COLLECTION_ID]&search=[SEARCH_QUERY]'
  ```

#### Get Prompt by ID

- **Response**
  - Status: 200
  - Body: Prompt detail.
- **Error**
  - Status: 404, prompt not found.

- **cURL**
  ```bash
  curl -X GET http://[BASE_URL]/prompts/[PROMPT_ID]
  ```

#### Create Prompt

- **Body**
  - Required: `PromptCreate` schema.
- **Response**
  - Status: 201
  - Body: Created prompt.
- **Error**
  - Status: 400, collection not found.

- **cURL**
  ```bash
  curl -X POST http://[BASE_URL]/prompts \
       -H "Content-Type: application/json" \
       -d '{
             "title": "New Prompt",
             "content": "Prompt content here.",
             "description": "Description of the prompt.",
             "collection_id": "[COLLECTION_ID]"
           }'
  ```

#### Update Prompt

- **Body**
  - Required: `PromptUpdate` schema.
- **Response**
  - Status: 200
  - Body: Updated prompt.
- **Error**
  - Status: 404, prompt not found.
  - Bug: Updated prompts don't update `updated_at` timestamp.

- **cURL**
  ```bash
  curl -X PUT http://[BASE_URL]/prompts/[PROMPT_ID] \
       -H "Content-Type: application/json" \
       -d '{
             "title": "Updated Prompt",
             "content": "Updated content.",
             "description": "Updated description.",
             "collection_id": "[UPDATED_COLLECTION_ID]"
           }'
  ```

#### Delete Prompt

- **Response**
  - Status: 204, no content.
- **Error**
  - Status: 404, prompt not found.

- **cURL**
  ```bash
  curl -X DELETE http://[BASE_URL]/prompts/[PROMPT_ID]
  ```

### Collections

#### List Collections

- **Response**
  - Status: 200
  - Body: List of collections.

- **cURL**
  ```bash
  curl -X GET http://[BASE_URL]/collections
  ```

#### Get Collection by ID

- **Response**
  - Status: 200
  - Body: Collection detail.
- **Error**
  - Status: 404, collection not found.

- **cURL**
  ```bash
  curl -X GET http://[BASE_URL]/collections/[COLLECTION_ID]
  ```

#### Create Collection

- **Body**
  - Required: `CollectionCreate` schema.
- **Response**
  - Status: 201
  - Body: Created collection.

- **cURL**
  ```bash
  curl -X POST http://[BASE_URL]/collections \
       -H "Content-Type: application/json" \
       -d '{
             "name": "New Collection",
             "description": "Description of the new collection."
           }'
  ```

#### Delete Collection

- **Response**
  - Status: 204, no content.
- **Error**
  - Status: 404, collection not found.
- **Notes**
  - **Bug**: Deleting a collection leaves prompts orphaned; handle accordingly.

- **cURL**
  ```bash
  curl -X DELETE http://[BASE_URL]/collections/[COLLECTION_ID]
  ```

## Known Bugs and Missing Features

1. **Prompt GET by ID**: Accessing a non-existent prompt ID raises a 500 error instead of a 404.
2. **Prompt PUT**: `updated_at` timestamp is not updated.
3. **Collection DELETE**: Does not handle prompts associated with a deleted collection.
4. **PATCH Endpoint Missing**: Necessary for partial updates.

## Error Handling

- Standard HTTP error status codes are used.
- Detailed error messages are returned in the response detail.

For any issues, suggestions, or contributions, please contact the development team or open a ticket in [Your Issue Tracker/Contact Point].