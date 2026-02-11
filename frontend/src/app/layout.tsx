import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Todo Chatbot',
  description: 'AI-Powered Todo Management with Natural Language',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
