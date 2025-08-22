import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { 
  Shield, 
  Zap, 
  Search, 
  FileText, 
  Users, 
  BarChart3,
  Globe,
  Lock,
  Cpu,
  Database
} from "lucide-react"
import Link from "next/link"

export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">About Our RAG System</h1>
        <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
          A production-grade, on-prem/local-first RAG platform for instant, trustworthy answers 
          over private documents with strict data residency and zero-trust controls.
        </p>
      </div>

      {/* Key Features Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Multi-Format Ingestion
            </CardTitle>
            <CardDescription>
              Support for PDFs, Office files, HTML, and emails with OCR capabilities
            </CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="h-5 w-5" />
              Hybrid Search
            </CardTitle>
            <CardDescription>
              BM25 + pgvector + rerankers with semantic filters and temporal boosting
            </CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5" />
              Source-Linked Answers
            </CardTitle>
            <CardDescription>
              Inline citations with quote spans and page coordinates
            </CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Globe className="h-5 w-5" />
              Continuous Sync
            </CardTitle>
            <CardDescription>
              SharePoint, GDrive, S3, IMAP, Jira/Confluence connectors
            </CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5" />
              Role-Based Access
            </CardTitle>
            <CardDescription>
              Collections, tenant isolation, and per-doc ACL inheritance
            </CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Evaluator Suite
            </CardTitle>
            <CardDescription>
              Groundedness, answer completeness, and citation validity reports
            </CardDescription>
          </CardHeader>
        </Card>
      </div>

      {/* Technical Stack */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Cpu className="h-5 w-5" />
            Technical Architecture
          </CardTitle>
          <CardDescription>
            Built with modern, scalable technologies for enterprise-grade performance
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold mb-3">Frontend Stack</h3>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">Next.js 14</Badge>
                  <span className="text-sm text-muted-foreground">App Router, React 18</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">TypeScript</Badge>
                  <span className="text-sm text-muted-foreground">Type-safe development</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">Tailwind CSS</Badge>
                  <span className="text-sm text-muted-foreground">Utility-first styling</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">shadcn/ui</Badge>
                  <span className="text-sm text-muted-foreground">Component library</span>
                </div>
              </div>
            </div>
            <div>
              <h3 className="font-semibold mb-3">Backend Stack</h3>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">FastAPI</Badge>
                  <span className="text-sm text-muted-foreground">Async Python framework</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">PostgreSQL</Badge>
                  <span className="text-sm text-muted-foreground">+ pgvector for embeddings</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">LangChain</Badge>
                  <span className="text-sm text-muted-foreground">+ LangGraph for RAG pipeline</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">Redis</Badge>
                  <span className="text-sm text-muted-foreground">Caching & task queue</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Security & Compliance */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Security & Compliance
          </CardTitle>
          <CardDescription>
            Enterprise-grade security with zero-trust architecture
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold mb-3">Security Features</h3>
              <ul className="space-y-2 text-sm">
                <li className="flex items-center gap-2">
                  <Lock className="h-4 w-4 text-green-500" />
                  Zero-trust architecture with per-tenant KMS keys
                </li>
                <li className="flex items-center gap-2">
                  <Lock className="h-4 w-4 text-green-500" />
                  Row-level security in PostgreSQL
                </li>
                <li className="flex items-center gap-2">
                  <Lock className="h-4 w-4 text-green-500" />
                  Envelope encryption for blobs and embeddings
                </li>
                <li className="flex items-center gap-2">
                  <Lock className="h-4 w-4 text-green-500" />
                  PII/PHI detection and redaction pipeline
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-3">Compliance Ready</h3>
              <ul className="space-y-2 text-sm">
                <li className="flex items-center gap-2">
                  <Database className="h-4 w-4 text-blue-500" />
                  SOC2-friendly logging and audit trails
                </li>
                <li className="flex items-center gap-2">
                  <Database className="h-4 w-4 text-blue-500" />
                  GDPR/CCPA tooling (DSAR export/delete)
                </li>
                <li className="flex items-center gap-2">
                  <Database className="h-4 w-4 text-blue-500" />
                  Tamper-evident hashing for data integrity
                </li>
                <li className="flex items-center gap-2">
                  <Database className="h-4 w-4 text-blue-500" />
                  Air-gap mode for sensitive environments
                </li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* CTA Section */}
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-4">Ready to Get Started?</h2>
        <p className="text-muted-foreground mb-6">
          Experience the power of local-first RAG with enterprise-grade security
        </p>
        <div className="flex gap-4 justify-center">
          <Button asChild>
            <Link href="/dashboard">Go to Dashboard</Link>
          </Button>
          <Button variant="outline" asChild>
            <Link href="/">Back to Home</Link>
          </Button>
        </div>
      </div>
    </div>
  )
}
