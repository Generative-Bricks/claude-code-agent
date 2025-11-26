/**
 * Card Component
 *
 * A container component for displaying content in a card layout.
 * Provides optional title and footer sections with consistent styling.
 *
 * Features:
 * - Optional title header
 * - Optional footer section
 * - Clean white background with subtle shadow
 * - Responsive padding
 */

import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  footer?: React.ReactNode;
}

export function Card({ children, className = '', title, footer }: CardProps) {
  return (
    <div className={`bg-white rounded-lg shadow-md border border-gray-200 ${className}`}>
      {/* Optional title section */}
      {title && (
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        </div>
      )}

      {/* Main content area */}
      <div className="px-6 py-4">{children}</div>

      {/* Optional footer section */}
      {footer && (
        <div className="px-6 py-4 border-t border-gray-200 bg-gray-50 rounded-b-lg">
          {footer}
        </div>
      )}
    </div>
  );
}
