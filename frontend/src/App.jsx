import { useState } from 'react';
import { PromptList } from './components/PromptList';
import { CollectionList } from './components/CollectionList';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('prompts');

  return (
    <div className="app">
      <header className="app-header">
        <h1>PromptLab</h1>
        <nav>
          <button
            className={activeTab === 'prompts' ? 'active' : ''}
            onClick={() => setActiveTab('prompts')}
          >
            Prompts
          </button>
          <button
            className={activeTab === 'collections' ? 'active' : ''}
            onClick={() => setActiveTab('collections')}
          >
            Collections
          </button>
        </nav>
      </header>

      <main className="app-main">
        {activeTab === 'prompts' ? <PromptList /> : <CollectionList />}
      </main>
    </div>
  );
}

export default App;
