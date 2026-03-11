import Chat from "./components/Chat";

function App() {
  return (
    <div className="app-root">
      <header className="app-header">
        <div className="app-header-inner">
          <div>
            <h1 className="app-title">Clinical Research Chatbot</h1>
            <p className="app-subtitle">
              Ask questions grounded in your clinical study documents.
            </p>
          </div>
        </div>
      </header>
      <main className="app-main">
        <Chat />
      </main>
      <footer className="app-footer">
        <span>MVP RAG prototype &ndash; not for clinical decision making.</span>
      </footer>
    </div>
  );
}

export default App;

