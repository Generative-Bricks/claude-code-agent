<!-- markdownlint-disable -->

# Shared UI Components Reference

This guide documents the reusable UI components available in the portfolio collaboration frontend.

All components are located in `/src/components/shared/` and can be imported using the barrel export.

## Quick Start

### Import Components

```tsx
// Recommended: Barrel import
import { Button, Card, Badge, LoadingSpinner, ErrorBoundary } from '@/components/shared';

// Alternative: Individual imports
import { Button } from '@/components/shared/Button';
import { Card } from '@/components/shared/Card';
```

### Wrap Your App

```tsx
import { ErrorBoundary } from '@/components/shared';

export function App() {
  return (
    <ErrorBoundary>
      <YourApplication />
    </ErrorBoundary>
  );
}
```

---

## Components

### Button

Versatile button component with multiple variants and sizes.

**Props:**

- `variant?: 'primary' | 'secondary' | 'danger' | 'ghost'` - Button style (default: 'primary')
- `size?: 'sm' | 'md' | 'lg'` - Button size (default: 'md')
- `loading?: boolean` - Show loading spinner (default: false)
- `disabled?: boolean` - Disable button
- `children: React.ReactNode` - Button label
- All standard HTML button attributes

**Examples:**

```tsx
// Primary button
<Button onClick={handleAnalyze}>Analyze Portfolio</Button>

// Different variants
<Button variant="secondary">Cancel</Button>
<Button variant="danger">Delete</Button>
<Button variant="ghost">Learn More</Button>

// Different sizes
<Button size="sm">Compact</Button>
<Button size="lg">Large</Button>

// Loading state
<Button loading={isAnalyzing}>
  Analyzing...
</Button>

// Disabled
<Button disabled>Unavailable</Button>
```

**Styling:**

- Primary: Blue background with white text
- Secondary: Gray background with white text
- Danger: Red background with white text
- Ghost: Transparent with gray text, visible on hover
- All variants include focus rings and active states

---

### Card

Container component for displaying content in a card layout.

**Props:**

- `children: React.ReactNode` - Card content
- `title?: string` - Optional header title
- `footer?: React.ReactNode` - Optional footer content
- `className?: string` - Additional CSS classes

**Examples:**

```tsx
// Simple card
<Card>
  <p>Your content here</p>
</Card>

// Card with title
<Card title="Client Profile">
  <form>{/* form fields */}</form>
</Card>

// Card with title and footer
<Card
  title="Portfolio Analysis"
  footer={<Button>Generate Report</Button>}
>
  <div>{/* analysis results */}</div>
</Card>
```

**Styling:**

- White background with subtle shadow
- Optional title section with border
- Optional footer section with gray background
- Responsive padding on all sides

---

### LoadingSpinner

Display an animated loading state with optional message.

**Props:**

- `size?: 'sm' | 'md' | 'lg'` - Spinner size (default: 'md')
- `message?: string` - Optional loading message

**Examples:**

```tsx
// Just spinner
<LoadingSpinner />

// With message
<LoadingSpinner message="Analyzing portfolio..." />

// Different sizes
<LoadingSpinner size="sm" message="Loading..." />
<LoadingSpinner size="lg" message="Please wait..." />

// In a card
<Card title="Analysis">
  {isLoading ? (
    <LoadingSpinner message="Analyzing portfolio..." />
  ) : (
    <AnalysisResults />
  )}
</Card>
```

**Styling:**

- Smooth CSS animation
- Blue color scheme
- Centered layout
- Optional text below spinner

---

### ErrorBoundary

Catch and handle runtime errors gracefully.

**Props:**

- `children: React.ReactNode` - Child components

**Examples:**

```tsx
// Wrap your entire app
<ErrorBoundary>
  <App />
</ErrorBoundary>

// Wrap feature sections
<ErrorBoundary>
  <PortfolioAnalysis />
</ErrorBoundary>

// Nested error boundaries
<ErrorBoundary>
  <MainSection>
    <ErrorBoundary>
      <NestedFeature />
    </ErrorBoundary>
  </MainSection>
</ErrorBoundary>
```

**Behavior:**

- Catches JavaScript errors in child components
- Displays user-friendly error message
- Provides "Try Again" button to reset state
- Logs errors to browser console for debugging
- Uses Card component for consistent styling

---

### Badge

Small label component for status indicators and tags.

**Props:**

- `variant?: 'success' | 'warning' | 'danger' | 'info' | 'neutral'` - Badge style (default: 'neutral')
- `size?: 'sm' | 'md'` - Badge size (default: 'md')
- `children: React.ReactNode` - Badge label

**Examples:**

```tsx
// Status indicators for suitability scores
<Badge variant="success">Highly Suitable (80-100)</Badge>
<Badge variant="success">Suitable (60-79)</Badge>
<Badge variant="warning">Marginal Fit (40-59)</Badge>
<Badge variant="danger">Not Suitable (0-39)</Badge>

// Category labels
<Badge>Portfolio</Badge>
<Badge>Client</Badge>

// Information labels
<Badge variant="info">New</Badge>
<Badge variant="neutral">Draft</Badge>

// Different sizes
<Badge size="sm">Small</Badge>
<Badge size="md">Medium</Badge>

// In a table or list
<div className="flex gap-2">
  <Badge variant="success">Conservative</Badge>
  <Badge variant="info">Client 001</Badge>
</div>
```

**Color Scheme:**

- Success: Green - Positive status
- Warning: Orange - Caution status
- Danger: Red - Error/critical status
- Info: Blue - Informational status
- Neutral: Gray - Default status

---

## Common Patterns

### Form with Loading State

```tsx
import { Button, Card, LoadingSpinner } from '@/components/shared';

function ClientProfileForm() {
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (data) => {
    setLoading(true);
    try {
      await submitProfile(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card title="Client Profile">
      {loading && <LoadingSpinner message="Saving..." />}
      {!loading && (
        <form onSubmit={handleSubmit}>
          {/* form fields */}
          <Button type="submit">Save Profile</Button>
        </form>
      )}
    </Card>
  );
}
```

### Results with Status Badge

```tsx
import { Card, Badge } from '@/components/shared';

function AnalysisResults({ suitability }) {
  const getSuitabilityBadge = (score) => {
    if (score >= 80) return <Badge variant="success">Highly Suitable</Badge>;
    if (score >= 60) return <Badge variant="success">Suitable</Badge>;
    if (score >= 40) return <Badge variant="warning">Marginal Fit</Badge>;
    return <Badge variant="danger">Not Suitable</Badge>;
  };

  return (
    <Card title="Portfolio Analysis Results">
      <div className="flex items-center justify-between">
        <span>Overall Score: {suitability}</span>
        {getSuitabilityBadge(suitability)}
      </div>
    </Card>
  );
}
```

### Error Handling

```tsx
import { ErrorBoundary, Card, Button } from '@/components/shared';

function ProtectedFeature() {
  return (
    <ErrorBoundary>
      <RiskyComponent />
    </ErrorBoundary>
  );
}
```

### Loading States

```tsx
import { LoadingSpinner, Card } from '@/components/shared';

function DataDisplay() {
  const { data, isLoading } = useQuery(...);

  if (isLoading) {
    return <LoadingSpinner message="Loading data..." />;
  }

  return <Card>{/* display data */}</Card>;
}
```

---

## Tailwind CSS

All components use Tailwind CSS utility classes. Customize appearance using the `className` prop:

```tsx
// Add custom spacing
<Card className="max-w-2xl mx-auto">
  Content
</Card>

// Override styling
<Button className="w-full">Full Width Button</Button>

// Responsive classes
<Card className="p-4 md:p-6 lg:p-8">
  Responsive padding
</Card>
```

---

## Accessibility

All components are built with accessibility in mind:

- **Button:** Full keyboard navigation, focus indicators, semantic HTML
- **Card:** Semantic sections with proper heading hierarchy
- **LoadingSpinner:** ARIA-friendly animated content, optional text alternative
- **ErrorBoundary:** Clear error messages, obvious recovery action
- **Badge:** Appropriate color contrast, semantic inline elements

---

## TypeScript Types

All components are fully typed with TypeScript:

```tsx
import { ButtonProps, CardProps, LoadingSpinnerProps, BadgeProps } from '@/components/shared';

// Extend component props
interface CustomButtonProps extends ButtonProps {
  customProp?: string;
}
```

---

## Performance

- Components use React functional components
- No unnecessary re-renders (proper prop passing)
- Minimal CSS (Tailwind utilities only)
- Icons are inline SVGs (no external dependencies)

---

## Integration Checklist

When adding new components to the app:

- [ ] Import from '@/components/shared'
- [ ] Wrap app with ErrorBoundary for global error handling
- [ ] Use Button for all interactive elements
- [ ] Use Card for content containers
- [ ] Use Badge for status indicators
- [ ] Use LoadingSpinner for async operations
- [ ] Maintain consistent spacing using Tailwind classes
- [ ] Test keyboard navigation
- [ ] Verify color contrast for accessibility

---

**Last Updated:** November 19, 2025
