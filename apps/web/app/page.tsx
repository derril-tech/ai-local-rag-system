import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { 
  FileText, 
  MessageSquare, 
  Database, 
  Settings, 
  Upload, 
  Search,
  Shield,
  Zap
} from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted/20">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <Zap className="w-5 h-5 text-primary-foreground" />
            </div>
            <h1 className="text-xl font-bold">AI Local RAG System</h1>
          </div>
          <nav className="hidden md:flex items-center space-x-6">
            <Link href="/dashboard" className="text-sm font-medium hover:text-primary transition-colors">
              Dashboard
            </Link>
            <Link href="/collections" className="text-sm font-medium hover:text-primary transition-colors">
              Collections
            </Link>
            <Link href="/connectors" className="text-sm font-medium hover:text-primary transition-colors">
              Connectors
            </Link>
            <Link href="/admin" className="text-sm font-medium hover:text-primary transition-colors">
              Admin
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary to-citation bg-clip-text text-transparent">
          Your Private AI Knowledge Base
        </h2>
        <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
          Production-grade, on-prem/local-first RAG platform for instant, trustworthy answers over private documents with strict data residency and zero-trust controls.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button asChild size="lg" className="text-lg px-8 py-6">
            <Link href="/dashboard">
              Get Started
            </Link>
          </Button>
          <Button variant="outline" size="lg" className="text-lg px-8 py-6" asChild>
            <Link href="/about">
              Learn More
            </Link>
          </Button>
        </div>
      </section>

      {/* Features Grid */}
      <section className="container mx-auto px-4 py-16">
        <h3 className="text-3xl font-bold text-center mb-12">Key Features</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <Upload className="w-6 h-6 text-primary" />
              </div>
              <CardTitle>Multi-Format Ingestion</CardTitle>
              <CardDescription>
                Support for PDFs, Office files, HTML, emails with OCR and table extraction
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="w-12 h-12 bg-citation/10 rounded-lg flex items-center justify-center mb-4">
                <Search className="w-6 h-6 text-citation" />
              </div>
              <CardTitle>Hybrid Search</CardTitle>
              <CardDescription>
                BM25 + pgvector + rerankers with semantic filters and temporal boosting
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="w-12 h-12 bg-success/10 rounded-lg flex items-center justify-center mb-4">
                <MessageSquare className="w-6 h-6 text-success" />
              </div>
              <CardTitle>Source-Linked Answers</CardTitle>
              <CardDescription>
                Inline citations with quote spans and page coordinates for verification
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="w-12 h-12 bg-warning/10 rounded-lg flex items-center justify-center mb-4">
                <Database className="w-6 h-6 text-warning" />
              </div>
              <CardTitle>Continuous Sync</CardTitle>
              <CardDescription>
                SharePoint, GDrive, S3, IMAP connectors with delta sync capabilities
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="w-12 h-12 bg-secondary/10 rounded-lg flex items-center justify-center mb-4">
                <Shield className="w-6 h-6 text-secondary-foreground" />
              </div>
              <CardTitle>Role-Based Access</CardTitle>
              <CardDescription>
                Collections, tenant isolation, and per-document ACL inheritance
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center mb-4">
                <FileText className="w-6 h-6 text-accent-foreground" />
              </div>
              <CardTitle>Evaluator Suite</CardTitle>
              <CardDescription>
                Groundedness, answer completeness, and citation validity reports
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* Quick Actions */}
      <section className="container mx-auto px-4 py-16">
        <h3 className="text-3xl font-bold text-center mb-12">Quick Actions</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Button asChild variant="outline" className="h-32 flex flex-col items-center justify-center space-y-2">
            <Link href="/dashboard/ask">
              <MessageSquare className="w-8 h-8" />
              <span>Ask Questions</span>
            </Link>
          </Button>
          
          <Button asChild variant="outline" className="h-32 flex flex-col items-center justify-center space-y-2">
            <Link href="/dashboard/upload">
              <Upload className="w-8 h-8" />
              <span>Upload Documents</span>
            </Link>
          </Button>
          
          <Button asChild variant="outline" className="h-32 flex flex-col items-center justify-center space-y-2">
            <Link href="/collections">
              <Database className="w-8 h-8" />
              <span>Manage Collections</span>
            </Link>
          </Button>
          
          <Button asChild variant="outline" className="h-32 flex flex-col items-center justify-center space-y-2">
            <Link href="/connectors">
              <Settings className="w-8 h-8" />
              <span>Setup Connectors</span>
            </Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-muted/50">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-sm text-muted-foreground">
            <p>© 2024 AI Local RAG System. Built for secure, compliant knowledge management.</p>
            <p className="mt-2">
              <Link href="/privacy" className="hover:text-primary transition-colors">Privacy</Link>
              {' • '}
              <Link href="/security" className="hover:text-primary transition-colors">Security</Link>
              {' • '}
              <Link href="/docs" className="hover:text-primary transition-colors">Documentation</Link>
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
