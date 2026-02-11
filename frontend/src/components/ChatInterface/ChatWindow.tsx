import React, { useState, useRef, useEffect } from 'react';
import Message from './Message';
import InputArea from './InputArea';

interface MessageType {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatWindowProps {
  conversationId?: string;
  onSendMessage: (message: string) => Promise<void>;
  messages: MessageType[];
  isLoading: boolean;
}

const ChatWindow: React.FC<ChatWindowProps> = ({
  conversationId,
  onSendMessage,
  messages,
  isLoading
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-800">
          Todo Chatbot
        </h2>
        {conversationId && (
          <p className="text-sm text-gray-500">
            Conversation ID: {conversationId.slice(0, 8)}...
          </p>
        )}
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center text-gray-500">
              <p className="text-lg font-medium mb-2">
                Welcome to Todo Chatbot!
              </p>
              <p className="text-sm">
                Ask me to manage your todos using natural language.
              </p>
              <p className="text-sm mt-2">
                Try: "Add a task to buy groceries" or "Show me my tasks"
              </p>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <Message
                key={message.id}
                role={message.role}
                content={message.content}
                timestamp={message.timestamp}
              />
            ))}
            {isLoading && (
              <div className="flex items-center space-x-2 text-gray-500">
                <div className="animate-pulse">●</div>
                <div className="animate-pulse delay-100">●</div>
                <div className="animate-pulse delay-200">●</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200">
        <InputArea
          onSendMessage={onSendMessage}
          disabled={isLoading}
        />
      </div>
    </div>
  );
};

export default ChatWindow;
