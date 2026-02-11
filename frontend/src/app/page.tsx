export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Welcome to Todo Chatbot
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Manage your todos using natural language
        </p>
        <a
          href="/chat"
          className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          Start Chatting
        </a>
      </div>
    </div>
  );
}
