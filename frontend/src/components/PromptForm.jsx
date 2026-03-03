import { useState, useEffect } from 'react';
import { Button } from './Button';

export const PromptForm = ({ prompt, collections, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    description: '',
    collection_id: ''
  });

  useEffect(() => {
    if (prompt) {
      setFormData({
        title: prompt.title || '',
        content: prompt.content || '',
        description: prompt.description || '',
        collection_id: prompt.collection_id || ''
      });
    }
  }, [prompt]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="prompt-form">
      <div className="form-group">
        <label>Title *</label>
        <input
          type="text"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          required
          maxLength={200}
        />
      </div>

      <div className="form-group">
        <label>Content *</label>
        <textarea
          value={formData.content}
          onChange={(e) => setFormData({ ...formData, content: e.target.value })}
          required
          rows={6}
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

      <div className="form-group">
        <label>Collection</label>
        <select
          value={formData.collection_id}
          onChange={(e) => setFormData({ ...formData, collection_id: e.target.value })}
        >
          <option value="">None</option>
          {collections.map((col) => (
            <option key={col.id} value={col.id}>{col.name}</option>
          ))}
        </select>
      </div>

      <div className="form-actions">
        <Button type="submit" variant="primary">
          {prompt ? 'Update' : 'Create'}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
      </div>
    </form>
  );
};
