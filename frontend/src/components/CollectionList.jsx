import { useState } from 'react';
import { Button } from './Button';
import { Modal } from './Modal';
import { useCollections } from '../hooks/useData';
import { api } from '../api/client';

export const CollectionList = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '' });
  const [actionError, setActionError] = useState(null);
  const { collections, loading, error, refetch } = useCollections();

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      setActionError(null);
      await api.createCollection(formData);
      setIsModalOpen(false);
      setFormData({ name: '', description: '' });
      refetch();
    } catch (err) {
      setActionError(err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this collection and all its prompts?')) return;
    try {
      await api.deleteCollection(id);
      refetch();
    } catch (err) {
      alert(`Failed to delete: ${err.message}`);
    }
  };

  if (loading) return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>Loading collections...</p>
    </div>
  );

  if (error) return (
    <div className="error-container">
      <div className="error-icon">⚠️</div>
      <h2>Failed to Load Collections</h2>
      <p>{error}</p>
      <Button onClick={refetch}>Try Again</Button>
    </div>
  );

  return (
    <div className="collection-list">
      <div className="list-header">
        <h1>Collections</h1>
        <Button onClick={() => setIsModalOpen(true)}>+ Create Collection</Button>
      </div>

      {collections.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📁</div>
          <h2>No Collections Yet</h2>
          <p>Organize your prompts by creating collections</p>
          <Button onClick={() => setIsModalOpen(true)}>Create Your First Collection</Button>
        </div>
      ) : (
        <div className="collections-grid">
          {collections.map((col) => (
            <div key={col.id} className="collection-card">
              <h3>{col.name}</h3>
              {col.description && <p>{col.description}</p>}
              <div className="collection-meta">
                <span>Created: {new Date(col.created_at).toLocaleDateString()}</span>
              </div>
              <Button variant="danger" onClick={() => handleDelete(col.id)}>Delete</Button>
            </div>
          ))}
        </div>
      )}

      <Modal isOpen={isModalOpen} onClose={() => { setIsModalOpen(false); setActionError(null); }} title="Create Collection">
        {actionError && (
          <div className="error-banner">
            <span>⚠️ {actionError}</span>
          </div>
        )}
        <form onSubmit={handleCreate} className="collection-form">
          <div className="form-group">
            <label>Name *</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
              maxLength={100}
            />
          </div>
          <div className="form-group">
            <label>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              maxLength={500}
              rows={3}
            />
          </div>
          <div className="form-actions">
            <Button type="submit">Create</Button>
            <Button type="button" variant="secondary" onClick={() => { setIsModalOpen(false); setActionError(null); }}>
              Cancel
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
