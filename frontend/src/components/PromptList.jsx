import { useState } from 'react';
import { PromptCard } from './PromptCard';
import { PromptForm } from './PromptForm';
import { PromptVersions } from './PromptVersions';
import { Modal } from './Modal';
import { Button } from './Button';
import { usePrompts, useCollections } from '../hooks/useData';
import { api } from '../api/client';

export const PromptList = () => {
  const [filters, setFilters] = useState({ search: '', collection_id: '' });
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isVersionsOpen, setIsVersionsOpen] = useState(false);
  const [editingPrompt, setEditingPrompt] = useState(null);
  const [selectedPrompt, setSelectedPrompt] = useState(null);
  const [actionError, setActionError] = useState(null);
  
  const { prompts, loading, error, refetch } = usePrompts(filters);
  const { collections } = useCollections();

  const handleCreate = async (data) => {
    try {
      setActionError(null);
      await api.createPrompt(data);
      setIsModalOpen(false);
      refetch();
    } catch (err) {
      setActionError(err.message);
    }
  };

  const handleUpdate = async (data) => {
    try {
      setActionError(null);
      // Fetch current prompt state from server
      const currentPrompt = await api.getPrompt(editingPrompt.id);
      // Create version snapshot of current state
      await api.createPromptVersion(editingPrompt.id, {
        title: currentPrompt.title,
        content: currentPrompt.content,
        description: currentPrompt.description || 'Version snapshot'
      });
      // Update prompt with new data
      await api.updatePrompt(editingPrompt.id, data);
      setIsModalOpen(false);
      setEditingPrompt(null);
      refetch();
    } catch (err) {
      setActionError(err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this prompt?')) return;
    try {
      await api.deletePrompt(id);
      refetch();
    } catch (err) {
      alert(`Failed to delete: ${err.message}`);
    }
  };

  const openEditModal = (prompt) => {
    setEditingPrompt(prompt);
    setActionError(null);
    setIsModalOpen(true);
  };

  const openVersions = (prompt) => {
    setSelectedPrompt(prompt);
    setIsVersionsOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingPrompt(null);
    setActionError(null);
  };

  const closeVersions = () => {
    setIsVersionsOpen(false);
    setSelectedPrompt(null);
  };

  if (loading) return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>Loading prompts...</p>
    </div>
  );

  if (error) return (
    <div className="error-container">
      <div className="error-icon">⚠️</div>
      <h2>Failed to Load Prompts</h2>
      <p>{error}</p>
      <Button onClick={refetch}>Try Again</Button>
    </div>
  );

  return (
    <div className="prompt-list">
      <div className="list-header">
        <h1>Prompts</h1>
        <Button onClick={() => setIsModalOpen(true)}>+ Create Prompt</Button>
      </div>

      <div className="filters">
        <input
          type="text"
          placeholder="🔍 Search prompts..."
          value={filters.search}
          onChange={(e) => setFilters({ ...filters, search: e.target.value })}
        />
        <select
          value={filters.collection_id}
          onChange={(e) => setFilters({ ...filters, collection_id: e.target.value })}
        >
          <option value="">All Collections</option>
          {collections.map((col) => (
            <option key={col.id} value={col.id}>{col.name}</option>
          ))}
        </select>
      </div>

      {prompts.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📝</div>
          <h2>No Prompts Yet</h2>
          <p>Create your first prompt to get started with PromptLab</p>
          <Button onClick={() => setIsModalOpen(true)}>Create Your First Prompt</Button>
        </div>
      ) : (
        <div className="prompts-grid">
          {prompts.map((prompt) => (
            <PromptCard
              key={prompt.id}
              prompt={prompt}
              onEdit={openEditModal}
              onDelete={handleDelete}
              onViewVersions={openVersions}
            />
          ))}
        </div>
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={closeModal}
        title={editingPrompt ? 'Edit Prompt' : 'Create Prompt'}
      >
        {actionError && (
          <div className="error-banner">
            <span>⚠️ {actionError}</span>
          </div>
        )}
        <PromptForm
          prompt={editingPrompt}
          collections={collections}
          onSubmit={editingPrompt ? handleUpdate : handleCreate}
          onCancel={closeModal}
        />
      </Modal>

      <Modal
        isOpen={isVersionsOpen}
        onClose={closeVersions}
        title="Prompt Versions"
      >
        {selectedPrompt && (
          <PromptVersions
            promptId={selectedPrompt.id}
            onClose={() => { closeVersions(); refetch(); }}
          />
        )}
      </Modal>
    </div>
  );
};
