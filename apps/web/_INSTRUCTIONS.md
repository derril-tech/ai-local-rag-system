# Frontend Development Instructions

## 🎯 Overview

This directory contains the Next.js frontend application for the AI Local RAG System. The application uses:
- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **shadcn/ui** for component library
- **React Query** for data fetching
- **Zustand** for state management

## 📁 Directory Structure

```
apps/web/
├── app/                    # Next.js App Router pages
├── components/            # Reusable React components
├── lib/                  # Utility functions and configurations
├── public/               # Static assets
└── types/                # TypeScript type definitions
```

## 🚀 TODO: Implementation Tasks

### 1. Component Library Setup
- [ ] **TODO**: Install and configure shadcn/ui components
- [ ] **TODO**: Create base UI components (Button, Input, Card, etc.)
- [ ] **TODO**: Set up design system with custom color tokens
- [ ] **TODO**: Implement dark/light theme switching

### 2. Authentication & Authorization
- [ ] **TODO**: Create login/register pages
- [ ] **TODO**: Implement JWT token management
- [ ] **TODO**: Add protected route middleware
- [ ] **TODO**: Create user profile management

### 3. Dashboard Interface
- [ ] **TODO**: Build main dashboard layout with sidebar navigation
- [ ] **TODO**: Create collection overview cards
- [ ] **TODO**: Add system statistics widgets
- [ ] **TODO**: Implement recent activity feed

### 4. Chat Interface
- [ ] **TODO**: Create chat message components
- [ ] **TODO**: Implement streaming response handling
- [ ] **TODO**: Add citation highlighting and source links
- [ ] **TODO**: Build chat session management

### 5. Document Management
- [ ] **TODO**: Create file upload component with drag-and-drop
- [ ] **TODO**: Build document list and search interface
- [ ] **TODO**: Implement document viewer with PDF support
- [ ] **TODO**: Add document metadata editing

### 6. Collection Management
- [ ] **TODO**: Create collection creation/editing forms
- [ ] **TODO**: Build collection list with filtering
- [ ] **TODO**: Implement collection settings management
- [ ] **TODO**: Add collection sharing and permissions

### 7. Connector Setup
- [ ] **TODO**: Build connector configuration wizards
- [ ] **TODO**: Create connector status monitoring
- [ ] **TODO**: Implement sync scheduling interface
- [ ] **TODO**: Add connector troubleshooting tools

### 8. Admin Interface
- [ ] **TODO**: Create user management interface
- [ ] **TODO**: Build system monitoring dashboard
- [ ] **TODO**: Implement audit log viewer
- [ ] **TODO**: Add system configuration management

## 🎨 Design Guidelines

### Color Scheme
- **Primary**: Blue (#3B82F6) - Main actions and branding
- **Secondary**: Gray (#6B7280) - Secondary actions
- **Success**: Green (#10B981) - Success states
- **Warning**: Yellow (#F59E0B) - Warning states
- **Error**: Red (#EF4444) - Error states
- **Citation**: Purple (#8B5CF6) - Citation highlights

### Typography
- **Headings**: Inter font, bold weights
- **Body**: Inter font, regular weight
- **Code**: JetBrains Mono for code blocks

### Spacing
- Use Tailwind's spacing scale (4px base unit)
- Consistent padding: 16px (p-4), 24px (p-6), 32px (p-8)
- Card spacing: 24px between cards

### Components
- Use shadcn/ui components as base
- Maintain consistent border radius (8px default)
- Implement hover and focus states for all interactive elements

## 🔧 Development Setup

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Git

### Installation
```bash
cd apps/web
npm install
```

### Development
```bash
npm run dev
```

### Building
```bash
npm run build
npm start
```

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Mobile-First Approach
- Start with mobile layouts
- Use Tailwind's responsive prefixes
- Test on real devices

## 🔒 Security Considerations

### Input Validation
- Validate all form inputs on frontend
- Sanitize user-generated content
- Implement CSRF protection

### Authentication
- Store tokens securely (httpOnly cookies)
- Implement automatic token refresh
- Handle authentication errors gracefully

### Data Protection
- Never expose sensitive data in client-side code
- Use environment variables for API keys
- Implement proper error boundaries

## 🧪 Testing Strategy

### Unit Tests
- Test individual components
- Mock API calls
- Test user interactions

### Integration Tests
- Test component interactions
- Test API integration
- Test authentication flows

### E2E Tests
- Test complete user journeys
- Test critical business flows
- Test responsive design

## 📊 Performance Optimization

### Code Splitting
- Use dynamic imports for large components
- Implement route-based code splitting
- Lazy load non-critical components

### Image Optimization
- Use Next.js Image component
- Implement proper image formats
- Optimize for different screen sizes

### Bundle Optimization
- Monitor bundle size
- Remove unused dependencies
- Implement tree shaking

## 🔄 State Management

### Local State
- Use React useState for component state
- Use React useReducer for complex state

### Global State
- Use Zustand for global state
- Keep state minimal and normalized
- Implement proper state persistence

### Server State
- Use React Query for API data
- Implement proper caching strategies
- Handle loading and error states

## 🌐 Internationalization

### Setup
- Use next-intl for i18n
- Support multiple languages
- Implement RTL support

### Content
- Extract all user-facing text
- Support date and number formatting
- Implement proper pluralization

## ♿ Accessibility

### Standards
- Follow WCAG 2.1 AA guidelines
- Implement proper ARIA labels
- Ensure keyboard navigation

### Testing
- Use screen readers for testing
- Test with keyboard only
- Validate color contrast

## 📈 Monitoring & Analytics

### Error Tracking
- Implement error boundaries
- Log errors to monitoring service
- Track user interactions

### Performance Monitoring
- Monitor Core Web Vitals
- Track API response times
- Monitor bundle sizes

## 🚀 Deployment

### Environment Variables
- Set up proper environment configuration
- Use different configs for dev/staging/prod
- Secure sensitive information

### Build Optimization
- Optimize for production builds
- Implement proper caching
- Use CDN for static assets

## 📝 Code Quality

### Linting
- Use ESLint for JavaScript/TypeScript
- Use Prettier for code formatting
- Implement pre-commit hooks

### Type Safety
- Use TypeScript strictly
- Define proper interfaces
- Avoid any types

### Documentation
- Document complex components
- Maintain README files
- Use JSDoc for functions

## 🔄 API Integration

### API Client
- Create centralized API client
- Implement proper error handling
- Add request/response interceptors

### Real-time Features
- Implement WebSocket connections
- Handle connection errors
- Implement reconnection logic

### File Upload
- Implement chunked uploads
- Show upload progress
- Handle upload errors

## 🎯 Success Metrics

### User Experience
- Page load times < 3 seconds
- Smooth animations (60fps)
- Responsive design on all devices

### Functionality
- All features working correctly
- Proper error handling
- Intuitive user interface

### Performance
- Lighthouse score > 90
- Core Web Vitals in green
- Bundle size optimized

## 🚨 Common Issues & Solutions

### Hydration Errors
- Use suppressHydrationWarning for dynamic content
- Implement proper SSR/CSR handling
- Test with different data states

### API Integration
- Handle network errors gracefully
- Implement retry logic
- Show appropriate loading states

### State Management
- Avoid prop drilling
- Use proper state lifting
- Implement optimistic updates

## 📚 Resources

### Documentation
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)

### Tools
- [React Developer Tools](https://chrome.google.com/webstore/detail/react-developer-tools)
- [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)

### Best Practices
- [React Best Practices](https://react.dev/learn)
- [TypeScript Best Practices](https://www.typescriptlang.org/docs)
- [Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
