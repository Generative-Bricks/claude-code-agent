/**
 * Client Profile Form Component
 *
 * Allows financial advisors to input client information for portfolio analysis.
 * Uses React Hook Form + Zod for validation.
 */

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/shared/Button';
import { Card } from '@/components/shared/Card';
import type { ClientProfile } from '@/types';

// Zod validation schema
const clientProfileSchema = z.object({
  client_id: z.string().min(1, 'Client ID is required'),
  age: z.number().min(18, 'Age must be at least 18').max(120, 'Invalid age'),
  risk_tolerance: z.enum(['Conservative', 'Moderate', 'Aggressive']),
  investment_goals: z.string().min(1, 'At least one investment goal required'),
  time_horizon: z.number().min(1, 'Time horizon must be at least 1 year').max(50),
  annual_income: z.number().optional(),
  net_worth: z.number().optional(),
  liquidity_needs: z.string().optional(),
  constraints: z.string().optional(),
});

type ClientProfileFormData = z.infer<typeof clientProfileSchema>;

interface ClientProfileFormProps {
  onSubmit: (profile: ClientProfile) => void;
  initialData?: Partial<ClientProfile>;
  loading?: boolean;
}

export function ClientProfileForm({ onSubmit, initialData, loading = false }: ClientProfileFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ClientProfileFormData>({
    resolver: zodResolver(clientProfileSchema),
    defaultValues: {
      client_id: initialData?.client_id || '',
      age: initialData?.age || 45,
      risk_tolerance: initialData?.risk_tolerance || 'Moderate',
      investment_goals: initialData?.investment_goals?.join(', ') || '',
      time_horizon: initialData?.time_horizon || 10,
      annual_income: initialData?.annual_income,
      net_worth: initialData?.net_worth,
      liquidity_needs: initialData?.liquidity_needs || '',
      constraints: initialData?.constraints?.join(', ') || '',
    },
  });

  const onFormSubmit = (data: ClientProfileFormData) => {
    // Convert form data to ClientProfile
    const profile: ClientProfile = {
      ...data,
      investment_goals: data.investment_goals.split(',').map(g => g.trim()).filter(Boolean),
      constraints: data.constraints ? data.constraints.split(',').map(c => c.trim()).filter(Boolean) : undefined,
    };
    onSubmit(profile);
  };

  return (
    <Card title="Client Profile">
      <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-6">
        {/* Client ID */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Client ID *
          </label>
          <input
            type="text"
            {...register('client_id')}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="CLT-2024-001"
          />
          {errors.client_id && (
            <p className="mt-1 text-sm text-red-600">{errors.client_id.message}</p>
          )}
        </div>

        {/* Age */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Age *
          </label>
          <input
            type="number"
            {...register('age', { valueAsNumber: true })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          {errors.age && (
            <p className="mt-1 text-sm text-red-600">{errors.age.message}</p>
          )}
        </div>

        {/* Risk Tolerance */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Risk Tolerance *
          </label>
          <select
            {...register('risk_tolerance')}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="Conservative">Conservative</option>
            <option value="Moderate">Moderate</option>
            <option value="Aggressive">Aggressive</option>
          </select>
          {errors.risk_tolerance && (
            <p className="mt-1 text-sm text-red-600">{errors.risk_tolerance.message}</p>
          )}
        </div>

        {/* Time Horizon */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Time Horizon (years) *
          </label>
          <input
            type="number"
            {...register('time_horizon', { valueAsNumber: true })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          {errors.time_horizon && (
            <p className="mt-1 text-sm text-red-600">{errors.time_horizon.message}</p>
          )}
        </div>

        {/* Investment Goals */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Investment Goals * (comma-separated)
          </label>
          <textarea
            {...register('investment_goals')}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Capital preservation, Income generation, Long-term growth"
          />
          {errors.investment_goals && (
            <p className="mt-1 text-sm text-red-600">{errors.investment_goals.message}</p>
          )}
        </div>

        {/* Annual Income (Optional) */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Annual Income (Optional)
          </label>
          <input
            type="number"
            {...register('annual_income', { valueAsNumber: true })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="85000"
          />
        </div>

        {/* Net Worth (Optional) */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Net Worth (Optional)
          </label>
          <input
            type="number"
            {...register('net_worth', { valueAsNumber: true })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="1250000"
          />
        </div>

        {/* Liquidity Needs (Optional) */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Liquidity Needs (Optional)
          </label>
          <input
            type="text"
            {...register('liquidity_needs')}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Moderate - emergency fund needed"
          />
        </div>

        {/* Constraints (Optional) */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Constraints (Optional, comma-separated)
          </label>
          <textarea
            {...register('constraints')}
            rows={2}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="No high-risk investments, Prefer blue-chip stocks"
          />
        </div>

        {/* Submit Button */}
        <div className="flex justify-end pt-4">
          <Button type="submit" loading={loading}>
            Continue to Portfolio Selection
          </Button>
        </div>
      </form>
    </Card>
  );
}
