# AI Local RAG System - Frontend

This is the Next.js frontend application for the AI Local RAG System, providing a modern, responsive interface for document management, chat interactions, and system administration.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-local-rag-system/apps/web
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env.local
   # Edit .env.local with your configuration
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🏗️ Architecture

### Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **State Management**: Zustand
- **Data Fetching**: React Query (TanStack Query)
- **Real-time**: WebSocket/Socket.io
- **Icons**: Lucide React

### Project Structure

```
apps/web/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Landing page
│   ├── globals.css        # Global styles
│   ├── dashboard/         # Dashboard pages
│   ├── collections/       # Collection management
│   ├── connectors/        # Connector setup
│   └── admin/            # Admin interface
├── components/            # Reusable React components
│   ├── ui/               # shadcn/ui components
│   ├── chat/             # Chat interface components
│   ├── upload/           # File upload components
│   ├── viewer/           # Document viewer components
│   └── providers/        # React context providers
├── lib/                  # Utility functions and configurations
│   ├── api.ts           # API client functions
│   ├── utils.ts         # General utilities
│   ├── types.ts         # TypeScript type definitions
│   └── hooks/           # Custom React hooks
├── public/              # Static assets
└── types/               # Additional type definitions
```

## 🎨 Design System

### Color Palette

- **Primary**: Blue (#3B82F6) - Main actions and branding
- **Secondary**: Gray (#6B7280) - Secondary actions
- **Success**: Green (#10B981) - Success states
- **Warning**: Yellow (#F59E0B) - Warning states
- **Error**: Red (#EF4444) - Error states
- **Citation**: Purple (#8B5CF6) - Citation highlights

### Typography

- **Font Family**: Inter (Google Fonts)
- **Headings**: Bold weights (600, 700)
- **Body**: Regular weight (400)
- **Code**: JetBrains Mono

### Components

All UI components are built using shadcn/ui with consistent:
- Border radius (8px default)
- Spacing (4px base unit)
- Hover and focus states
- Dark/light theme support

## 🔧 Development

### Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript type checking
```

### Environment Variables

Create a `.env.local` file with the following variables:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Authentication
NEXT_PUBLIC_AUTH_ENABLED=true

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_DEBUG_MODE=true
```

### Code Style

- **TypeScript**: Strict mode enabled
- **ESLint**: Configured with Next.js rules
- **Prettier**: Code formatting
- **Husky**: Pre-commit hooks

## 📱 Features

### Core Functionality

1. **Authentication & Authorization**
   - JWT-based authentication
   - Role-based access control
   - Protected routes
   - User profile management

2. **Dashboard**
   - System overview and statistics
   - Quick action buttons
   - Recent activity feed
   - System status monitoring

3. **Document Management**
   - Drag-and-drop file upload
   - Document list and search
   - PDF viewer with highlighting
   - Metadata editing

4. **Collections**
   - Create and manage collections
   - Collection settings
   - Permission management
   - Document organization

5. **Chat Interface**
   - Real-time chat with RAG responses
   - Citation highlighting
   - Source document links
   - Chat history management

6. **Connectors**
   - Setup wizards for external systems
   - Connector status monitoring
   - Sync scheduling
   - Troubleshooting tools

7. **Admin Interface**
   - User management
   - System monitoring
   - Audit logs
   - Configuration management

### Advanced Features

- **Real-time Updates**: WebSocket connections for live data
- **Responsive Design**: Mobile-first approach
- **Accessibility**: WCAG 2.1 AA compliant
- **Internationalization**: Multi-language support
- **Dark Mode**: Theme switching
- **Offline Support**: Service worker for offline functionality

## 🔒 Security

### Authentication

- Secure token storage (httpOnly cookies)
- Automatic token refresh
- Session timeout handling
- CSRF protection

### Data Protection

- Input validation and sanitization
- XSS prevention
- Secure API communication
- Error boundary implementation

### Privacy

- No sensitive data in client-side code
- Environment variable protection
- Audit logging
- Data retention policies

## 🧪 Testing

### Testing Strategy

- **Unit Tests**: Component testing with Jest and React Testing Library
- **Integration Tests**: API integration testing
- **E2E Tests**: Complete user journey testing with Playwright
- **Accessibility Tests**: Automated a11y testing

### Running Tests

```bash
npm run test           # Run unit tests
npm run test:e2e       # Run E2E tests
npm run test:coverage  # Run tests with coverage
```

## 📊 Performance

### Optimization

- **Code Splitting**: Route-based and dynamic imports
- **Image Optimization**: Next.js Image component
- **Bundle Analysis**: Webpack bundle analyzer
- **Caching**: Static generation and ISR

### Monitoring

- **Core Web Vitals**: Performance monitoring
- **Error Tracking**: Sentry integration
- **Analytics**: Google Analytics (optional)
- **Real User Monitoring**: Performance insights

## 🚀 Deployment

### Production Build

```bash
npm run build
npm start
```

### Deployment Options

1. **Vercel** (Recommended)
   - Automatic deployments
   - Edge functions
   - Global CDN

2. **Netlify**
   - Static site hosting
   - Form handling
   - Serverless functions

3. **Docker**
   - Containerized deployment
   - Multi-stage builds
   - Environment configuration

### Environment Configuration

- **Development**: Local development setup
- **Staging**: Pre-production testing
- **Production**: Live environment

## 🔄 API Integration

### API Client

Centralized API client with:
- Request/response interceptors
- Error handling
- Authentication headers
- Retry logic

### Real-time Features

- WebSocket connections
- Event-driven updates
- Connection management
- Fallback mechanisms

## 📈 Monitoring & Analytics

### Error Tracking

- Error boundaries
- Sentry integration
- Performance monitoring
- User feedback collection

### Analytics

- Page view tracking
- User interaction analytics
- Performance metrics
- Business intelligence

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests**
5. **Submit a pull request**

### Code Review

- Automated checks (linting, testing)
- Peer review process
- Security review
- Performance review

## 📚 Resources

### Documentation

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [React Query Documentation](https://tanstack.com/query)

### Tools

- [React Developer Tools](https://chrome.google.com/webstore/detail/react-developer-tools)
- [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)
- [TypeScript](https://www.typescriptlang.org/)

### Best Practices

- [React Best Practices](https://react.dev/learn)
- [Next.js Best Practices](https://nextjs.org/docs/basic-features/typescript)
- [Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

## 🆘 Support

### Getting Help

1. **Documentation**: Check the docs first
2. **Issues**: Search existing issues
3. **Discussions**: Community discussions
4. **Contact**: Direct support for enterprise

### Common Issues

- **Build Errors**: Check Node.js version and dependencies
- **API Issues**: Verify environment variables and backend status
- **Performance**: Use bundle analyzer and performance tools
- **Styling**: Check Tailwind CSS configuration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
