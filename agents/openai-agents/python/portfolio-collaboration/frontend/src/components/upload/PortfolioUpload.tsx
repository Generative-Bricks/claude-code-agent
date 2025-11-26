/**
 * Portfolio Upload Component
 *
 * Allows uploading portfolio data via CSV/JSON or selecting from existing portfolios.
 */

import React, { useState, useCallback } from 'react';
import { Button } from '@/components/shared/Button';
import { Card } from '@/components/shared/Card';
import type { Portfolio } from '@/types';

interface PortfolioUploadProps {
  onPortfolioSelected: (portfolio: Portfolio) => void;
  availablePortfolios?: Portfolio[];
  loading?: boolean;
}

export function PortfolioUpload({
  onPortfolioSelected,
  availablePortfolios = [],
  loading = false,
}: PortfolioUploadProps) {
  const [uploadMode, setUploadMode] = useState<'select' | 'upload'>('select');
  const [selectedPortfolioId, setSelectedPortfolioId] = useState<string>('');
  const [uploadError, setUploadError] = useState<string>('');

  const handleFileUpload = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (!file) return;

      setUploadError('');

      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const content = e.target?.result as string;
          let portfolio: Portfolio;

          if (file.name.endsWith('.json')) {
            portfolio = JSON.parse(content);
          } else if (file.name.endsWith('.csv')) {
            // Basic CSV parsing (implement if needed)
            setUploadError('CSV parsing not yet implemented. Please use JSON format.');
            return;
          } else {
            setUploadError('Unsupported file format. Please use JSON or CSV.');
            return;
          }

          // Validate portfolio structure
          if (!portfolio.portfolio_id || !portfolio.holdings) {
            setUploadError('Invalid portfolio format. Missing required fields.');
            return;
          }

          onPortfolioSelected(portfolio);
        } catch (error) {
          setUploadError('Failed to parse file. Please check format.');
          console.error('Upload error:', error);
        }
      };

      reader.readAsText(file);
    },
    [onPortfolioSelected]
  );

  const handleSelectPortfolio = () => {
    const portfolio = availablePortfolios.find((p) => p.portfolio_id === selectedPortfolioId);
    if (portfolio) {
      onPortfolioSelected(portfolio);
    }
  };

  return (
    <Card title="Portfolio Selection">
      <div className="space-y-6">
        {/* Mode Selector */}
        <div className="flex gap-4 border-b border-gray-200 pb-4">
          <button
            type="button"
            onClick={() => setUploadMode('select')}
            className={`px-4 py-2 font-medium ${
              uploadMode === 'select'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Select Existing
          </button>
          <button
            type="button"
            onClick={() => setUploadMode('upload')}
            className={`px-4 py-2 font-medium ${
              uploadMode === 'upload'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Upload File
          </button>
        </div>

        {/* Select Mode */}
        {uploadMode === 'select' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Choose Portfolio</label>
            <select
              value={selectedPortfolioId}
              onChange={(e) => setSelectedPortfolioId(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">-- Select a portfolio --</option>
              {availablePortfolios.map((portfolio) => (
                <option key={portfolio.portfolio_id} value={portfolio.portfolio_id}>
                  {portfolio.portfolio_id} ({portfolio.holdings.length} holdings, $
                  {portfolio.total_value.toLocaleString()})
                </option>
              ))}
            </select>
            <div className="mt-4">
              <Button onClick={handleSelectPortfolio} disabled={!selectedPortfolioId} loading={loading}>
                Analyze Portfolio
              </Button>
            </div>
          </div>
        )}

        {/* Upload Mode */}
        {uploadMode === 'upload' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Upload Portfolio (JSON)</label>
            <div className="mt-2 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-blue-400 transition-colors">
              <div className="space-y-2 text-center">
                <svg
                  className="mx-auto h-12 w-12 text-gray-400"
                  stroke="currentColor"
                  fill="none"
                  viewBox="0 0 48 48"
                >
                  <path
                    d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                    strokeWidth={2}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                <div className="text-sm text-gray-600">
                  <label
                    htmlFor="file-upload"
                    className="relative cursor-pointer rounded-md font-medium text-blue-600 hover:text-blue-500"
                  >
                    <span>Upload a file</span>
                    <input
                      id="file-upload"
                      name="file-upload"
                      type="file"
                      accept=".json,.csv"
                      className="sr-only"
                      onChange={handleFileUpload}
                    />
                  </label>
                  <p className="pl-1">or drag and drop</p>
                </div>
                <p className="text-xs text-gray-500">JSON or CSV up to 10MB</p>
              </div>
            </div>
            {uploadError && <p className="mt-2 text-sm text-red-600">{uploadError}</p>}
          </div>
        )}
      </div>
    </Card>
  );
}
