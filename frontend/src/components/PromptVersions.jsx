import { useState, useEffect } from 'react';
import { Button } from './Button';
import { Modal } from './Modal';
import { api } from '../api/client';

export const PromptVersions = ({ promptId, onClose }) => {
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchVersions();
  }, [promptId]);

  const fetchVersions = async () => {
    try {
      setLoading(true);
      const data = await api.getPromptVersions(promptId);
      setVersions(data.versions);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRevert = async (versionId) => {
    if (!confirm('Revert to this version?')) return;
    try {
      // Revert creates a new version
      await api.revertToVersion(promptId, versionId);
      // Get the version data to update the prompt
      const version = await api.getPromptVersion(promptId, versionId);
      // Update the actual prompt with version data
      await api.updatePrompt(promptId, {
        title: version.title,
        content: version.content,
        description: version.description || ''
      });
      fetchVersions();
      onClose();
    } catch (err) {
      alert(`Failed to revert: ${err.message}`);
    }
  };

  if (loading) return <div className="loading-container"><div className="spinner"></div></div>;
  if (error) return <div className="error-banner">⚠️ {error}</div>;

  return (
    <div className="versions-list">
      <div className="versions-header">
        <h3>Version History</h3>
        <Button variant="secondary" onClick={onClose}>Close</Button>
      </div>
      
      {versions.length === 0 ? (
        <p className="empty-message">No versions yet</p>
      ) : (
        <div className="versions-grid">
          {versions.map((version) => (
            <div key={version.id} className="version-card">
              <div className="version-header">
                <span className="version-number">v{version.version_number}</span>
                <span className="version-date">{new Date(version.created_at).toLocaleDateString()}</span>
              </div>
              <h4>{version.title}</h4>
              <p className="version-content">{version.content}</p>
              {version.description && <p className="version-description">{version.description}</p>}
              <Button variant="secondary" onClick={() => handleRevert(version.id)}>Revert</Button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
