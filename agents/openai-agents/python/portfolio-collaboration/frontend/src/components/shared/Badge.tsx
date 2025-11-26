/**
 * Badge Component
 *
 * A small label component for displaying status, tags, or brief information.
 * Commonly used for displaying scores, status indicators, or category labels.
 *
 * Variants:
 * - success: Green, for positive/passed status
 * - warning: Orange, for caution/warning status
 * - danger: Red, for error/critical status
 * - info: Blue, for informational status
 * - neutral: Gray, for default/neutral status
 *
 * Sizes:
 * - sm: Small badge (compact)
 * - md: Medium badge (default)
 *
 * Example:
 * ```tsx
 * <Badge variant="success">Suitable</Badge>
 * <Badge variant="warning">Marginal Fit</Badge>
 * <Badge variant="danger">Not Suitable</Badge>
 * ```
 */

import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'success' | 'warning' | 'danger' | 'info' | 'neutral';
  size?: 'sm' | 'md';
}

export function Badge({ children, variant = 'neutral', size = 'md' }: BadgeProps) {
  // Variant-specific styles
  const variantStyles = {
    success: 'bg-green-100 text-green-800 border-green-200',
    warning: 'bg-orange-100 text-orange-800 border-orange-200',
    danger: 'bg-red-100 text-red-800 border-red-200',
    info: 'bg-blue-100 text-blue-800 border-blue-200',
    neutral: 'bg-gray-100 text-gray-800 border-gray-200',
  };

  // Size-specific styles
  const sizeStyles = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm',
  };

  return (
    <span
      className={`inline-flex items-center font-medium rounded-full border ${variantStyles[variant]} ${sizeStyles[size]}`}
    >
      {children}
    </span>
  );
}
