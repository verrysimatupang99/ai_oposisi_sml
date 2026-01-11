# 🎨 AI Tokoh Oposisi & Intelektual Kritis - Frontend

React frontend application for the AI Tokoh Oposisi & Intelektual Kritis system.

## 🚀 Features

- **Modern UI**: Beautiful Material-UI design with dark theme
- **Authentication**: JWT-based authentication with Redux state management
- **Real-time Chat**: Interactive chat interface with Dr. Arjuna Wibawa persona
- **Political Analysis**: Advanced analysis tools and data visualization
- **Responsive Design**: Mobile-first responsive design
- **Accessibility**: WCAG-compliant accessibility features
- **Performance**: Optimized performance with lazy loading and caching

## 📋 Requirements

- Node.js 16+
- npm or yarn
- Backend API running on http://localhost:8000

## 🛠️ Installation

### 1. Clone and Setup

```bash
cd ai_oposisi_sml/frontend
npm install
```

### 2. Environment Configuration

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Environment Variables

```bash
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000/ws

# Application
REACT_APP_NAME="AI Tokoh Oposisi & Intelektual Kritis"
REACT_APP_VERSION=1.0.0

# Features
REACT_APP_ENABLE_ANALYTICS=false
REACT_APP_ENABLE_NOTIFICATIONS=true
REACT_APP_ENABLE_PWA=true
```

## 🚀 Running the Application

### Development

```bash
npm start
```

### Build

```bash
npm run build
```

### Preview Build

```bash
npm run preview
```

### Testing

```bash
npm test
```

## 📁 Project Structure

```
src/
├── components/           # Reusable components
│   ├── common/          # Common components
│   ├── layout/          # Layout components
│   └── ui/              # UI components
├── pages/               # Page components
│   ├── Login.tsx
│   ├── Register.tsx
│   ├── Dashboard.tsx
│   ├── Chat.tsx
│   ├── Analysis.tsx
│   ├── Persona.tsx
│   ├── Ethics.tsx
│   └── Profile.tsx
├── services/            # API services
│   ├── authService.ts
│   ├── chatService.ts
│   ├── analysisService.ts
│   ├── personaService.ts
│   └── ethicsService.ts
├── store/               # Redux store
│   ├── store.ts
│   └── slices/          # Redux slices
├── hooks/               # Custom hooks
├── types/               # TypeScript types
├── styles/              # Global styles
│   ├── theme.ts         # Material-UI theme
│   ├── globals.css      # Global CSS
│   └── components/      # Component styles
├── utils/               # Utility functions
├── constants/           # Application constants
└── App.tsx              # Main app component
```

## 🎨 UI Components

### Layout Components

- **Layout**: Main application layout with sidebar and header
- **Header**: Application header with navigation and user menu
- **Sidebar**: Navigation sidebar with menu items
- **Footer**: Application footer

### Common Components

- **LoadingSpinner**: Reusable loading spinner
- **ProtectedRoute**: Route protection component
- **Toast**: Toast notification component
- **Modal**: Modal dialog component
- **Button**: Custom button component
- **Input**: Custom input component

### Chat Components

- **ChatInterface**: Main chat interface
- **Message**: Individual chat message
- **InputArea**: Chat input area
- **ConversationHistory**: Chat history component

### Analysis Components

- **AnalysisPanel**: Main analysis panel
- **PoliticalAnalysis**: Political analysis component
- **DataVisualization**: Data charts and graphs
- **AnalysisForm**: Analysis input form

### Persona Components

- **PersonaProfile**: Persona profile display
- **PersonaChat**: Persona-specific chat
- **PersonaSettings**: Persona configuration

### Ethics Components

- **EthicsValidator**: Content validation interface
- **ContentFilter**: Content filtering component
- **ViolationReport**: Violation reporting

## 🔄 State Management

### Redux Store Structure

```typescript
{
  auth: {
    user: User | null,
    token: string | null,
    isAuthenticated: boolean,
    isLoading: boolean,
    error: string | null
  },
  chat: {
    sessions: ChatSession[],
    currentSession: ChatSession | null,
    messages: ChatMessage[],
    isLoading: boolean,
    error: string | null
  },
  analysis: {
    analyses: PoliticalAnalysis[],
    currentAnalysis: PoliticalAnalysis | null,
    isLoading: boolean,
    error: string | null
  },
  persona: {
    personas: Persona[],
    currentPersona: Persona | null,
    isLoading: boolean,
    error: string | null
  },
  ethics: {
    validations: EthicsValidation[],
    isLoading: boolean,
    error: string | null
  },
  ui: {
    theme: 'light' | 'dark',
    sidebarOpen: boolean,
    notifications: Notification[],
    isLoading: boolean
  }
}
```

## 🌐 API Integration

### Service Layer

All API calls are handled through service functions:

```typescript
// Example: Chat service
import { chatService } from '../services/chatService';

// Get chat sessions
const sessions = await chatService.getChatSessions();

// Send message
const response = await chatService.sendMessage({
  sessionId: 'session-id',
  message: 'Hello Dr. Arjuna!'
});
```

### Error Handling

Global error handling with toast notifications:

```typescript
try {
  const result = await apiCall();
} catch (error) {
  toast.error(error.message || 'An error occurred');
}
```

## 🎨 Styling

### Material-UI Theme

Custom theme with dark mode:

```typescript
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#1e88e5',
    },
    // ... other theme options
  },
  // ... typography, components
});
```

### CSS Modules

Component-specific styles using CSS modules:

```css
/* Component.module.css */
.container {
  padding: 2rem;
  border-radius: 12px;
  background: var(--bg-secondary);
}
```

### Global Styles

Global CSS with CSS variables:

```css
:root {
  --primary-color: #1e88e5;
  --bg-primary: #121212;
  --text-primary: #e0e0e0;
}
```

## 📱 Responsive Design

### Breakpoints

```css
/* Mobile */
@media (max-width: 768px) {
  /* Mobile styles */
}

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) {
  /* Tablet styles */
}

/* Desktop */
@media (min-width: 1025px) {
  /* Desktop styles */
}
```

### Grid System

CSS Grid and Flexbox for responsive layouts:

```css
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

@media (max-width: 768px) {
  .grid-3 {
    grid-template-columns: 1fr;
  }
}
```

## 🔒 Authentication

### JWT Token Management

- Automatic token refresh
- Token expiration handling
- Protected routes
- Logout functionality

### User Roles

Role-based access control:

```typescript
const { hasRole, isSuperuser } = useAuth();

if (isSuperuser()) {
  // Show admin features
}
```

## 🤖 AI Integration

### Chat Interface

Real-time chat with AI persona:

```typescript
// Send message to AI
const response = await chatService.sendMessage({
  sessionId: currentSession.id,
  message: userInput,
  personaId: 'dr_arjuna'
});
```

### Analysis Features

Political content analysis:

```typescript
// Analyze political content
const analysis = await analysisService.analyzeContent({
  content: politicalText,
  analysisType: 'election'
});
```

### Ethics Validation

Content filtering and validation:

```typescript
// Validate content
const validation = await ethicsService.validateContent({
  content: userContent,
  contentType: 'text'
});
```

## 📊 Data Visualization

### Charts and Graphs

Using Chart.js and D3.js:

```typescript
import { LineChart } from '../components/charts/LineChart';

<LineChart
  data={chartData}
  options={chartOptions}
  height={400}
/>
```

### Data Tables

Interactive data tables:

```typescript
import { DataTable } from '../components/DataTable';

<DataTable
  columns={columns}
  data={tableData}
  onSort={handleSort}
  onFilter={handleFilter}
/>
```

## 🔔 Notifications

### Toast Notifications

Using react-hot-toast:

```typescript
import { toast } from 'react-hot-toast';

toast.success('Operation completed successfully');
toast.error('An error occurred');
toast.loading('Processing...');
```

### System Notifications

In-app notifications:

```typescript
import { useNotifications } from '../hooks/useNotifications';

const { notifications, addNotification, removeNotification } = useNotifications();
```

## 🧪 Testing

### Unit Tests

Using Jest and React Testing Library:

```bash
npm test
```

### Test Structure

```typescript
// Example test
describe('AuthService', () => {
  test('should login user successfully', async () => {
    const result = await authService.login(credentials);
    expect(result).toBeDefined();
  });
});
```

### Component Tests

Testing React components:

```typescript
import { render, screen } from '@testing-library/react';
import Login from '../pages/Login';

test('renders login form', () => {
  render(<Login />);
  expect(screen.getByText('Sign In')).toBeInTheDocument();
});
```

## 🚀 Performance

### Code Splitting

Lazy loading for better performance:

```typescript
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('../pages/Dashboard'));

<Suspense fallback={<LoadingSpinner />}>
  <Dashboard />
</Suspense>
```

### Caching

Redux caching for API responses:

```typescript
// Cache API responses in Redux store
const selectCachedData = createSelector(
  [selectApiState],
  (apiState) => apiState.cachedData
);
```

### Optimization

- Image optimization
- Bundle splitting
- Virtualization for long lists
- Memoization for expensive calculations

## 🔧 Development Tools

### ESLint

Code linting with custom rules:

```bash
npm run lint
```

### Prettier

Code formatting:

```bash
npm run format
```

### TypeScript

Full TypeScript support with strict mode:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

## 📦 Deployment

### Build Optimization

```bash
npm run build
```

### Environment Variables

Set environment variables for production:

```bash
REACT_APP_API_URL=https://api.example.com
REACT_APP_WS_URL=wss://api.example.com
```

### CDN Deployment

Deploy to CDN for better performance:

```bash
# Build for production
npm run build

# Deploy to CDN (example with Netlify)
netlify deploy --prod
```

## 🌐 PWA Support

### Service Worker

Progressive Web App features:

```typescript
// Register service worker
import * as serviceWorkerRegistration from './serviceWorkerRegistration';
serviceWorkerRegistration.register();
```

### Manifest

PWA manifest configuration:

```json
{
  "name": "AI Tokoh Oposisi",
  "short_name": "AI Oposisi",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#1e88e5",
  "background_color": "#121212"
}
```

## 🔒 Security

### XSS Protection

Input sanitization and validation:

```typescript
// Sanitize user input
import DOMPurify from 'dompurify';

const cleanInput = DOMPurify.sanitize(userInput);
```

### CSRF Protection

CSRF token handling:

```typescript
// Include CSRF token in requests
api.defaults.headers.common['X-CSRF-TOKEN'] = getCsrfToken();
```

### Content Security Policy

CSP headers for security:

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'">
```

## 📈 Monitoring

### Error Tracking

Error boundary and logging:

```typescript
class ErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }
}
```

### Performance Monitoring

Web Vitals monitoring:

```typescript
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:

1. Check the [API Documentation](http://localhost:8000/docs)
2. Review the [Error Logs](logs/error.log)
3. Check [GitHub Issues](https://github.com/your-repo/issues)

---

**⚠️ PERINGATAN ETIKA**: Sistem ini **hanya untuk tujuan edukasi dan simulasi**. Dilarang digunakan untuk aktivitas politik nyata, memengaruhi opini publik, atau kampanye propaganda.