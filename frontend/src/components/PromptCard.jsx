import { Button } from './Button';

export const PromptCard = ({ prompt, onEdit, onDelete, onViewVersions }) => (
  <div className="prompt-card">
    <div className="prompt-header">
      <h3>{prompt.title}</h3>
      <div className="prompt-actions">
        <Button variant="secondary" onClick={() => onViewVersions(prompt)}>Versions</Button>
        <Button variant="secondary" onClick={() => onEdit(prompt)}>Edit</Button>
        <Button variant="danger" onClick={() => onDelete(prompt.id)}>Delete</Button>
      </div>
    </div>
    
    <p className="prompt-content">{prompt.content}</p>
    
    {prompt.description && (
      <p className="prompt-description">{prompt.description}</p>
    )}
    
    <div className="prompt-meta">
      <span>Created: {new Date(prompt.created_at).toLocaleDateString()}</span>
    </div>
  </div>
);
