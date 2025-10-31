import React from 'react';
import DocumentUpload from './components/DocumentUpload';
import './App.css'; // Assuming there might be a global CSS file

const App: React.FC = () => {
  return (
    <div className="App">
      <header className="App-header">
        {/* Potentially add a logo or navigation here */}
      </header>
      <main>
        <DocumentUpload />
      </main>
    </div>
  );
};

export default App;
