"""API tests for PromptLab

These tests verify the API endpoints work correctly.
Students should expand these tests significantly in Week 3.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealth:
    """Tests for health endpoint."""
    
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestPrompts:
    """Tests for prompt endpoints."""
    
    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_prompt_with_invalid_collection(self, client: TestClient, sample_prompt_data):
        prompt_data = {**sample_prompt_data, "collection_id": "invalid-id"}
        response = client.post("/prompts", json=prompt_data)
        assert response.status_code == 400
        assert "Collection not found" in response.json()["detail"]
    
    def test_create_prompt_with_valid_collection(self, client: TestClient, sample_prompt_data, sample_collection_data):
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        response = client.post("/prompts", json=prompt_data)
        assert response.status_code == 201
        assert response.json()["collection_id"] == collection_id
    
    def test_list_prompts_empty(self, client: TestClient):
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0
    
    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        client.post("/prompts", json=sample_prompt_data)
        
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1
    
    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id
    
    def test_get_prompt_not_found(self, client: TestClient):
        """Test that getting a non-existent prompt returns 404.
        
        NOTE: This test currently FAILS due to Bug #1!
        The API returns 500 instead of 404.
        """
        response = client.get("/prompts/nonexistent-id")
        # This should be 404, but there's a bug...
        assert response.status_code == 404  # Will fail until bug is fixed
    
    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/prompts/{prompt_id}")
        # Note: This might fail due to Bug #1
        assert get_response.status_code in [404, 500]  # 404 after fix
    
    def test_update_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Update it
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content for the prompt",
            "description": "Updated description"
        }
        
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp would change
        
        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        
        # NOTE: This assertion will fail due to Bug #2!
        # The updated_at should be different from original
        # assert data["updated_at"] != original_updated_at  # Uncomment after fix
    
    def test_update_prompt_not_found(self, client: TestClient):
        updated_data = {"title": "New", "content": "New content", "description": "New"}
        response = client.put("/prompts/nonexistent", json=updated_data)
        assert response.status_code == 404
    
    def test_update_prompt_with_invalid_collection(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        updated_data = {**sample_prompt_data, "collection_id": "invalid-id"}
        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 400
    
    def test_patch_prompt(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        response = client.patch(f"/prompts/{prompt_id}", json={"title": "Patched", "content": "content"})
        assert response.status_code == 200
        assert response.json()["title"] == "Patched"
    
    def test_patch_prompt_not_found(self, client: TestClient):
        response = client.patch("/prompts/nonexistent", json={"title": "New", "content": "content"})
        assert response.status_code == 404
    
    def test_patch_prompt_with_invalid_collection(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        response = client.patch(f"/prompts/{prompt_id}", json={**sample_prompt_data, "collection_id": "invalid-id"})
        assert response.status_code == 400
    
    def test_sorting_order(self, client: TestClient):
        """Test that prompts are sorted newest first.
        
        NOTE: This test might fail due to Bug #3!
        """
        import time
        
        # Create prompts with delay
        prompt1 = {"title": "First", "content": "First prompt content"}
        prompt2 = {"title": "Second", "content": "Second prompt content"}
        
        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)
        
        response = client.get("/prompts")
        prompts = response.json()["prompts"]
        
        # Newest (Second) should be first
        assert prompts[0]["title"] == "Second"  # Will fail until Bug #3 fixed
    
    def test_filter_by_collection(self, client: TestClient, sample_prompt_data, sample_collection_data):
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        client.post("/prompts", json={**sample_prompt_data, "collection_id": collection_id})
        client.post("/prompts", json={**sample_prompt_data, "title": "Other"})
        response = client.get(f"/prompts?collection_id={collection_id}")
        assert response.json()["total"] == 1
    
    def test_search_prompts(self, client: TestClient, sample_prompt_data):
        client.post("/prompts", json=sample_prompt_data)
        client.post("/prompts", json={"title": "Other", "content": "Different content"})
        response = client.get("/prompts?search=Code")
        assert response.json()["total"] == 1
        assert "Code" in response.json()["prompts"][0]["title"]


class TestCollections:
    """Tests for collection endpoints."""
    
    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data
    
    def test_list_collections(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert len(data["collections"]) == 1
    
    def test_get_collection_not_found(self, client: TestClient):
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Test deleting a collection that has prompts.
        
        NOTE: Bug #4 - prompts become orphaned after collection deletion.
        This test documents the current (buggy) behavior.
        After fixing, update the test to verify correct behavior.
        """
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompt in collection
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]
        
        # Delete collection
        client.delete(f"/collections/{collection_id}")
        
        # The prompt still exists but has invalid collection_id
        # This is Bug #4 - should be handled properly
        prompts = client.get("/prompts").json()["prompts"]
        if prompts:
            # Prompt exists with orphaned collection_id
            assert prompts[0]["collection_id"] == collection_id
            # After fix, collection_id should be None or prompt should be deleted
    
    def test_delete_collection_not_found(self, client: TestClient):
        response = client.delete("/collections/nonexistent")
        assert response.status_code == 404
    
    def test_list_collections_empty(self, client: TestClient):
        response = client.get("/collections")
        assert response.status_code == 200
        assert response.json()["total"] == 0


class TestPromptVersions:
    """Tests for prompt version endpoints."""
    
    def test_list_versions_for_nonexistent_prompt(self, client: TestClient):
        response = client.get("/prompts/nonexistent/versions")
        assert response.status_code == 404
    
    def test_list_versions_empty(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        response = client.get(f"/prompts/{prompt_id}/versions")
        assert response.status_code == 200
        assert response.json()["total"] == 0
    
    def test_create_version(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        version_data = {
            "title": "Version 1",
            "content": "First version content",
            "description": "Initial version"
        }
        response = client.post(f"/prompts/{prompt_id}/versions", json=version_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == version_data["title"]
        assert data["version_number"] == 1
        assert data["prompt_id"] == prompt_id
        assert "id" in data
    
    def test_create_version_for_nonexistent_prompt(self, client: TestClient):
        version_data = {"title": "Test", "content": "Content"}
        response = client.post("/prompts/nonexistent/versions", json=version_data)
        assert response.status_code == 404
    
    def test_version_number_auto_increment(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        v1 = client.post(f"/prompts/{prompt_id}/versions", json={"title": "V1", "content": "C1"})
        v2 = client.post(f"/prompts/{prompt_id}/versions", json={"title": "V2", "content": "C2"})
        v3 = client.post(f"/prompts/{prompt_id}/versions", json={"title": "V3", "content": "C3"})
        
        assert v1.json()["version_number"] == 1
        assert v2.json()["version_number"] == 2
        assert v3.json()["version_number"] == 3
    
    def test_list_versions_sorted(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        client.post(f"/prompts/{prompt_id}/versions", json={"title": "V1", "content": "C1"})
        client.post(f"/prompts/{prompt_id}/versions", json={"title": "V2", "content": "C2"})
        client.post(f"/prompts/{prompt_id}/versions", json={"title": "V3", "content": "C3"})
        
        response = client.get(f"/prompts/{prompt_id}/versions")
        versions = response.json()["versions"]
        assert len(versions) == 3
        assert versions[0]["version_number"] == 3
        assert versions[1]["version_number"] == 2
        assert versions[2]["version_number"] == 1
    
    def test_get_specific_version(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        version_response = client.post(f"/prompts/{prompt_id}/versions", json={"title": "V1", "content": "C1"})
        version_id = version_response.json()["id"]
        
        response = client.get(f"/prompts/{prompt_id}/versions/{version_id}")
        assert response.status_code == 200
        assert response.json()["id"] == version_id
    
    def test_get_version_not_found(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        response = client.get(f"/prompts/{prompt_id}/versions/nonexistent")
        assert response.status_code == 404
    
    def test_revert_to_version(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        v1 = client.post(f"/prompts/{prompt_id}/versions", json={"title": "V1", "content": "Content1"})
        v2 = client.post(f"/prompts/{prompt_id}/versions", json={"title": "V2", "content": "Content2"})
        v1_id = v1.json()["id"]
        
        response = client.post(f"/prompts/{prompt_id}/versions/{v1_id}/revert")
        assert response.status_code == 201
        data = response.json()
        assert data["version_number"] == 3
        assert data["content"] == "Content1"
        assert "Reverted to version 1" in data["description"]
    
    def test_revert_to_nonexistent_version(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        response = client.post(f"/prompts/{prompt_id}/versions/nonexistent/revert")
        assert response.status_code == 404
    
    def test_get_version_wrong_prompt(self, client: TestClient, sample_prompt_data):
        p1 = client.post("/prompts", json=sample_prompt_data)
        p2 = client.post("/prompts", json={**sample_prompt_data, "title": "Other"})
        p1_id = p1.json()["id"]
        p2_id = p2.json()["id"]
        
        v1 = client.post(f"/prompts/{p1_id}/versions", json={"title": "V1", "content": "C1"})
        v1_id = v1.json()["id"]
        
        response = client.get(f"/prompts/{p2_id}/versions/{v1_id}")
        assert response.status_code == 404
    
    def test_revert_version_wrong_prompt(self, client: TestClient, sample_prompt_data):
        p1 = client.post("/prompts", json=sample_prompt_data)
        p2 = client.post("/prompts", json={**sample_prompt_data, "title": "Other"})
        p1_id = p1.json()["id"]
        p2_id = p2.json()["id"]
        
        v1 = client.post(f"/prompts/{p1_id}/versions", json={"title": "V1", "content": "C1"})
        v1_id = v1.json()["id"]
        
        response = client.post(f"/prompts/{p2_id}/versions/{v1_id}/revert")
        assert response.status_code == 404
    
    def test_version_without_description(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        response = client.post(f"/prompts/{prompt_id}/versions", json={"title": "V1", "content": "C1"})
        assert response.status_code == 201
        assert response.json()["description"] is None
