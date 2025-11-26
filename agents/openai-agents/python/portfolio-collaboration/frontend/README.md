# Portfolio Collaboration - Web Frontend

Modern React + TypeScript frontend for the multi-agent portfolio analysis system built with Vite, Tailwind CSS, and production-grade tooling.

**Status:** Production-Ready | Version 1.0.0

---

## Overview

A comprehensive web interface for financial advisors to:
- Upload and analyze client portfolios
- View detailed risk, compliance, and performance metrics
- Interact with specialist AI agents in real-time
- Generate professional analysis reports
- Track analysis history and recommendations

**Key Technologies:**
- **Build Tool:** Vite (sub-second HMR, optimized builds)
- **Framework:** React 18+ with TypeScript strict mode
- **Styling:** Tailwind CSS with custom theme
- **State Management:** Zustand + React Query
- **Charts:** Recharts for financial visualizations
- **Forms:** React Hook Form + Zod for validation
- **Routing:** React Router v6
- **HTTP Client:** Axios with request/response interceptors
- **Real-time:** Socket.io for live updates

---

## Project Structure

```
frontend/
├── public/                          # Static assets
├── src/
│   ├── components/
│   │   ├── analysis/               # Portfolio analysis components
│   │   ├── charts/                 # Financial chart components
│   │   ├── chat/                   # Agent conversation interface
│   │   ├── forms/                  # Form components
│   │   ├── upload/                 # File upload components
│   │   └── shared/                 # Reusable UI components
│   ├── pages/                       # Page-level components
│   ├── services/                    # API client services
│   ├── hooks/                       # Custom React hooks
│   ├── types/                       # TypeScript type definitions
│   ├── utils/                       # Utility functions
│   ├── App.tsx                      # Main app component
│   ├── main.tsx                     # Entry point
│   └── index.css                    # Global styles with Tailwind
├── .env                             # Local environment variables
├── .env.example                     # Environment template
├── vite.config.ts                   # Vite configuration
├── tsconfig.json                    # TypeScript root config
├── tsconfig.app.json                # TypeScript app config
├── tailwind.config.js               # Tailwind CSS configuration
├── postcss.config.js                # PostCSS configuration
├── package.json                     # Dependencies and scripts
└── index.html                       # HTML entry point
```

---

## Quick Start

### Prerequisites

- Node.js 18+
- Backend server running on `http://localhost:8000`

### Setup

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Start development server
npm run dev

# Navigate to http://localhost:5173
```

### Configuration

Edit `.env` to customize:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

---

## Available Scripts

### Development
- `npm run dev` - Start dev server with HMR
- `npm run lint` - Run ESLint
- `npm run type-check` - Check TypeScript types

### Production
- `npm run build` - Build optimized production bundle
- `npm run preview` - Preview production build locally

---

## Development Workflow

### 1. Component Development

Create components in `src/components/`:

```typescript
import React from 'react';

interface ButtonProps {
  label: string;
  onClick: () => void;
}

export function Button({ label, onClick }: ButtonProps) {
  return (
    <button className="btn btn-primary" onClick={onClick}>
      {label}
    </button>
  );
}
```

### 2. API Integration

Services in `src/services/`:

```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

export default apiClient;
```

### 3. State Management

Use Zustand for state:

```typescript
import { create } from 'zustand';

export const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));
```

### 4. Form Validation

Use React Hook Form + Zod:

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  name: z.string().min(1),
});

export function MyForm() {
  const { register, handleSubmit } = useForm({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <input {...register('name')} />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### 5. Data Fetching

Use React Query:

```typescript
import { useQuery } from '@tanstack/react-query';

export function useAnalysis(clientId: string) {
  return useQuery({
    queryKey: ['analysis', clientId],
    queryFn: () => apiClient.get(`/api/analysis/${clientId}`),
  });
}
```

---

## Tailwind CSS

### Custom Theme

```tailwindcss
/* Financial advisor themed colors */
bg-primary-600      /* Primary actions */
bg-success-600      /* Positive metrics */
bg-warning-600      /* Alerts */
bg-danger-600       /* Risks */
```

### Component Classes

```html
<div class="card p-6">Content</div>
<button class="btn btn-primary">Click</button>
<span class="badge badge-success">Success</span>
<input class="input" type="text" />
```

---

## Building for Production

```bash
npm run build

# Output in dist/ directory
# Files:
# - dist/index.html         # Entry point
# - dist/assets/main-*.js   # App bundle
# - dist/assets/vendor-*.js # Vendor bundles
# - dist/assets/*.css       # Compiled styles
```

### Deploy to AWS

```bash
# Build
npm run build

# Upload to S3
aws s3 sync dist/ s3://your-bucket-name/ --delete

# Invalidate CloudFront
aws cloudfront create-invalidation \
  --distribution-id DISTRIBUTION_ID \
  --paths "/*"
```

---

## Naming Conventions

### Files
- Components: `ComponentName.tsx` (PascalCase)
- Hooks: `useHookName.ts` (camelCase with "use" prefix)
- Services: `serviceName.ts` (camelCase)
- Types: `types.ts` (descriptive names)

### Functions & Variables
- Components: `PascalCase`
- Functions: `camelCase`
- Constants: `UPPER_CASE`
- Types/Interfaces: `PascalCase`

---

## Performance Tips

### Code Splitting

```typescript
import { lazy, Suspense } from 'react';

const Page = lazy(() => import('@/pages/Page'));

export function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Page />
    </Suspense>
  );
}
```

### Memoization

```typescript
import { memo, useMemo, useCallback } from 'react';

const Component = memo(({ data }) => <div>{data}</div>);

const results = useMemo(() => compute(data), [data]);

const handleClick = useCallback(() => {}, []);
```

### React Query Optimization

```typescript
const { data } = useQuery({
  queryKey: ['analysis', id],
  queryFn: () => fetchAnalysis(id),
  staleTime: 5 * 60 * 1000,
  gcTime: 10 * 60 * 1000,
});
```

---

## Debugging

### Browser DevTools
- React DevTools - Inspect components
- Network Tab - View API requests

### VS Code

Create `.vscode/launch.json`:

```json
{
  "type": "chrome",
  "request": "launch",
  "name": "Launch frontend",
  "url": "http://localhost:5173",
  "webRoot": "${workspaceFolder}/frontend/src"
}
```

---

## Common Issues

**Cannot find module '@/...'**
- Verify `vite.config.ts` and `tsconfig.app.json` have path aliases

**Styles not applying**
- Ensure `src/index.css` has Tailwind directives

**API requests failing**
- Verify backend runs on `VITE_API_BASE_URL`
- Check CORS configuration

**TypeScript errors**
- Run `npm run type-check` to see all errors

---

## Security Best Practices

1. Never commit `.env` files
2. Validate all API responses
3. Use Zod for runtime validation
4. Escape user input (React does this by default)
5. Let backend handle authentication/CSRF

---

## Contributing

1. Create feature branch
2. Make focused, atomic changes
3. Ensure `npm run type-check` passes
4. Create pull request with clear description

### Code Review Checklist
- [ ] TypeScript types are correct
- [ ] No unused imports/variables
- [ ] Components properly memoized
- [ ] Error handling is comprehensive
- [ ] Tailwind classes used correctly

---

## Resources

- [Vite Documentation](https://vitejs.dev)
- [React 18 Docs](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS](https://tailwindcss.com)
- [React Router v6](https://reactrouter.com)
- [React Hook Form](https://react-hook-form.com)
- [Zod Documentation](https://zod.dev)

---

**Remember:** Excellence is doing simple things consistently well.

*Last updated: January 2025*
*Project Version: 1.0.0*
