import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from '@/components/providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AI Local RAG System',
  description: 'Production-grade, on-prem/local-first RAG platform for instant, trustworthy answers over private documents',
  keywords: ['RAG', 'AI', 'Document Processing', 'Knowledge Management', 'Local AI'],
  authors: [{ name: 'AI Local RAG Team' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'noindex, nofollow', // For private/internal use
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
