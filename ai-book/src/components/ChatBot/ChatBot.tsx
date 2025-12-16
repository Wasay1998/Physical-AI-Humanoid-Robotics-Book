import React, { useState, useRef, useEffect } from 'react';
import './ChatBot.css';

// Define TypeScript interfaces to match backend API
interface Citation {
  chunk_id: string;
  page_number: number;
  section_title: string;
  content: string;
}

interface BackendResponse {
  response: string;
  citations: Citation[];
  session_token: string;
  query_id: string;
  relevance_score: number;
}

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

const ChatBot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionToken, setSessionToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    // Add user message to the chat
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // Prepare the request payload
      const requestBody = {
        book_id: 'main-book', // Using a default book ID for this implementation
        query: inputValue,
        session_token: sessionToken || undefined, // Use session token if available
      };

      // Make the API call to the backend
      const response = await fetch('http://127.0.0.1:8000/api/v1/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': process.env.REACT_APP_API_KEY || 'your-default-api-key', // Use API key from env
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`Backend API error: ${response.status} ${response.statusText}`);
      }

      const data: BackendResponse = await response.json();

      // Update session token if we got a new one
      if (!sessionToken && data.session_token) {
        setSessionToken(data.session_token);
      }

      // Add bot response to the chat
      const botMessage: Message = {
        id: data.query_id,
        content: data.response,
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
      
      // Add error message to the chat
      const errorMessage: Message = {
        id: Date.now().toString(),
        content: `Error: ${err instanceof Error ? err.message : 'Failed to send message'}`,
        sender: 'bot',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      {/* Chat Window */}
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <h3>AI Assistant</h3>
            <button className="chatbot-close-btn" onClick={toggleChat}>
              ×
            </button>
          </div>
          
          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="chatbot-welcome">
                <p>Hello! I'm your AI assistant for this book.</p>
                <p>Ask me anything about the content.</p>
              </div>
            ) : (
              <>
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`chatbot-message ${
                      message.sender === 'user' ? 'user-message' : 'bot-message'
                    }`}
                  >
                    <div className="message-content">{message.content}</div>
                    <div className="message-timestamp">
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="chatbot-message bot-message">
                    <div className="message-content">
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>
          
          <form onSubmit={handleSubmit} className="chatbot-input-form">
            <input
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              placeholder="Ask a question..."
              disabled={isLoading}
              className="chatbot-input"
            />
            <button 
              type="submit" 
              disabled={isLoading || !inputValue.trim()}
              className="chatbot-send-btn"
            >
              Send
            </button>
          </form>
          
          {error && (
            <div className="chatbot-error">
              {error}
            </div>
          )}
        </div>
      )}
      
      {/* Toggle Button */}
      <button 
        className={`chatbot-toggle-btn ${isOpen ? 'open' : ''}`}
        onClick={toggleChat}
      >
        {isOpen ? '×' : 'AI'}
      </button>
    </div>
  );
};

export default ChatBot;