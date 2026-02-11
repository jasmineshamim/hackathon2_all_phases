'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ChatWindow from '../../components/ChatInterface/ChatWindow';
import ConversationHistory from '../../components/ChatInterface/ConversationHistory';
import { chatAPI } from '../../services/api';
import { authService } from '../../services/auth';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Check authentication
    if (!authService.isAuthenticated()) {
      router.push('/login');
    }
  }, [router]);

  const handleSendMessage = async (messageText: string) => {
    // Add user message to UI
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: messageText,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);

    setIsLoading(true);
    try {
      // Send message to API
      const response = await chatAPI.sendMessage(messageText, conversationId);

      // Update conversation ID if new
      if (response.data.conversation_id && !conversationId) {
        setConversationId(response.data.conversation_id);
      }

      // Add assistant response to UI
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);

      // Add error message
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectConversation = async (selectedConversationId: string) => {
    setIsLoading(true);
    try {
      // Load conversation messages
      const response = await chatAPI.getConversationMessages(selectedConversationId);

      // Convert to Message format
      const loadedMessages: Message[] = response.data.messages.map((msg: any) => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
        timestamp: new Date(msg.timestamp),
      }));

      setMessages(loadedMessages);
      setConversationId(selectedConversationId);
    } catch (error) {
      console.error('Failed to load conversation:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewConversation = () => {
    setMessages([]);
    setConversationId(undefined);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header with Conversation History */}
        <div className="max-w-4xl mx-auto mb-4 flex items-center justify-between">
          <ConversationHistory
            onSelectConversation={handleSelectConversation}
            currentConversationId={conversationId}
          />
          <button
            onClick={handleNewConversation}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
            <span className="text-sm font-medium">New Chat</span>
          </button>
        </div>

        {/* Chat Window */}
        <div className="max-w-4xl mx-auto h-[calc(100vh-8rem)]">
          <ChatWindow
            conversationId={conversationId}
            onSendMessage={handleSendMessage}
            messages={messages}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
}
