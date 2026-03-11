import { FormEvent, useState } from "react";
import { API_BASE_URL } from "../config";

type Source = {
  label: string;
  text: string;
  metadata: Record<string, unknown>;
};

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

type ChatResponse = {
  answer: string;
  sources: Source[];
};

const createId = () => Math.random().toString(36).slice(2);

async function sendQuestion(question: string): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    const message =
      (errorBody && (errorBody.detail as string)) ||
      `Request failed with status ${response.status}`;
    throw new Error(message);
  }

  return response.json();
}

function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [question, setQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const trimmed = question.trim();
    if (!trimmed || isLoading) return;

    setError(null);

    const userMessage: ChatMessage = {
      id: createId(),
      role: "user",
      content: trimmed,
    };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setIsLoading(true);

    try {
      const result = await sendQuestion(trimmed);
      const assistantMessage: ChatMessage = {
        id: createId(),
        role: "assistant",
        content: result.answer,
        sources: result.sources,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "An unexpected error occurred while contacting the API.";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  const lastAssistantSources =
    [...messages].reverse().find((m) => m.role === "assistant")?.sources ?? [];

  return (
    <div className="chat-layout">
      <section className="chat-panel">
        <div className="chat-messages" aria-label="Chat messages">
          {messages.length === 0 && (
            <div className="chat-empty-state">
              <h2>Start your clinical research query</h2>
              <p>
                Examples:
                <br />
                &bull; &ldquo;What are the side effects of Treatment X?&rdquo;
                <br />
                &bull; &ldquo;What was the primary endpoint in this study?&rdquo;
              </p>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`chat-bubble ${
                message.role === "user"
                  ? "chat-bubble-user"
                  : "chat-bubble-assistant"
              }`}
            >
              <div className="chat-bubble-role">
                {message.role === "user" ? "You" : "Assistant"}
              </div>
              <div className="chat-bubble-content">{message.content}</div>
            </div>
          ))}

          {isLoading && (
            <div className="chat-bubble chat-bubble-assistant">
              <div className="chat-bubble-role">Assistant</div>
              <div className="chat-bubble-content">
                <span className="typing-dot" />
                <span className="typing-dot" />
                <span className="typing-dot" />
              </div>
            </div>
          )}
        </div>

        <form className="chat-input-bar" onSubmit={handleSubmit}>
          <input
            type="text"
            className="chat-input"
            placeholder="Ask a question about your clinical study..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            disabled={isLoading}
          />
          <button
            type="submit"
            className="chat-submit"
            disabled={isLoading || !question.trim()}
          >
            {isLoading ? "Thinking..." : "Ask"}
          </button>
        </form>

        {error && <div className="chat-error">{error}</div>}
      </section>

      <aside className="sources-panel" aria-label="Answer sources">
        <h2 className="sources-title">Sources</h2>
        {lastAssistantSources.length === 0 ? (
          <p className="sources-empty">
            Sources for the latest answer will appear here.
          </p>
        ) : (
          <ul className="sources-list">
            {lastAssistantSources.map((source, index) => (
              <li key={`${source.label}-${index}`} className="sources-item">
                <div className="sources-label">{source.label}</div>
                {source.metadata?.source && (
                  <div className="sources-meta">
                    {String(source.metadata.source)}
                  </div>
                )}
                <p className="sources-text">{source.text}</p>
              </li>
            ))}
          </ul>
        )}
      </aside>
    </div>
  );
}

export default Chat;

