const API_BASE = '/api';

const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || 'Request failed');
  }
  return response.status === 204 ? null : response.json();
};

export const api = {
  // Prompts
  getPrompts: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return fetch(`${API_BASE}/prompts${query ? `?${query}` : ''}`).then(handleResponse);
  },
  
  getPrompt: (id) => 
    fetch(`${API_BASE}/prompts/${id}`).then(handleResponse),
  
  createPrompt: (data) =>
    fetch(`${API_BASE}/prompts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(handleResponse),
  
  updatePrompt: (id, data) =>
    fetch(`${API_BASE}/prompts/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(handleResponse),
  
  deletePrompt: (id) =>
    fetch(`${API_BASE}/prompts/${id}`, { method: 'DELETE' }).then(handleResponse),

  // Collections
  getCollections: () =>
    fetch(`${API_BASE}/collections`).then(handleResponse),
  
  getCollection: (id) =>
    fetch(`${API_BASE}/collections/${id}`).then(handleResponse),
  
  createCollection: (data) =>
    fetch(`${API_BASE}/collections`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(handleResponse),
  
  deleteCollection: (id) =>
    fetch(`${API_BASE}/collections/${id}`, { method: 'DELETE' }).then(handleResponse),

  // Prompt Versions
  getPromptVersions: (promptId) =>
    fetch(`${API_BASE}/prompts/${promptId}/versions`).then(handleResponse),
  
  getPromptVersion: (promptId, versionId) =>
    fetch(`${API_BASE}/prompts/${promptId}/versions/${versionId}`).then(handleResponse),
  
  createPromptVersion: (promptId, data) =>
    fetch(`${API_BASE}/prompts/${promptId}/versions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(handleResponse),
  
  revertToVersion: (promptId, versionId) =>
    fetch(`${API_BASE}/prompts/${promptId}/versions/${versionId}/revert`, {
      method: 'POST'
    }).then(handleResponse)
};
