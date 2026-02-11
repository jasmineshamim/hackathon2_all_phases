'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ChatInterface from '@/components/chat/ChatInterface';
import { apiClient } from '@/lib/api-client';

export default function ChatPage() {
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated after component mounts (client-side only)
    if (!apiClient.isAuthenticated()) {
      router.push('/auth/signin');
    } else {
      setIsLoading(false); // User is authenticated, allow chat to render
    }
  }, [router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Checking authentication...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            AI Task Assistant
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your tasks through natural conversation
          </p>
        </div>

        <div className="h-[calc(100vh-200px)]">
          <ChatInterface />
        </div>
      </div>
    </div>
  );
}
