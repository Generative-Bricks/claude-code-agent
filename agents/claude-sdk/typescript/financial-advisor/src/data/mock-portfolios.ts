import type {
  ClientProfile,
  AnnuityProduct,
  MarketRates,
  PortfolioAllocation
} from '../types/index.js';

// Sample client profiles for testing
export const sampleClients: ClientProfile[] = [
  {
    name: "Sarah Johnson",
    age: 62,
    retirementAge: 65,
    currentSavings: 750000,
    monthlyIncome: 8500,
    monthlyExpenses: 5200,
    riskTolerance: "conservative",
    taxBracket: 0.24,
    healthStatus: "good",
    hasSpouse: true,
    spouseAge: 64,
    existingAnnuities: 0,
    investmentGoals: [
      "Guaranteed income stream",
      "Protect principal",
      "Leave legacy for children"
    ]
  },
  {
    name: "Michael Chen",
    age: 58,
    retirementAge: 62,
    currentSavings: 1200000,
    monthlyIncome: 15000,
    monthlyExpenses: 8000,
    riskTolerance: "moderate",
    taxBracket: 0.32,
    healthStatus: "excellent",
    hasSpouse: false,
    existingAnnuities: 200000,
    investmentGoals: [
      "Growth potential",
      "Supplement retirement income",
      "Tax-deferred growth"
    ]
  },
  {
    name: "Linda Martinez",
    age: 70,
    retirementAge: 65,
    currentSavings: 450000,
    monthlyIncome: 4200,
    monthlyExpenses: 4800,
    riskTolerance: "conservative",
    taxBracket: 0.22,
    healthStatus: "fair",
    hasSpouse: true,
    spouseAge: 72,
    existingAnnuities: 150000,
    investmentGoals: [
      "Immediate income needs",
      "Cover monthly expenses",
      "Lifetime income guarantee"
    ]
  },
  {
    name: "David Thompson",
    age: 55,
    retirementAge: 60,
    currentSavings: 900000,
    monthlyIncome: 12000,
    monthlyExpenses: 6500,
    riskTolerance: "aggressive",
    taxBracket: 0.35,
    healthStatus: "excellent",
    hasSpouse: false,
    existingAnnuities: 0,
    investmentGoals: [
      "Maximize growth",
      "Tax optimization",
      "Flexible withdrawal options"
    ]
  },
  {
    name: "Emily Rodriguez",
    age: 67,
    retirementAge: 65,
    currentSavings: 580000,
    monthlyIncome: 5800,
    monthlyExpenses: 5000,
    riskTolerance: "moderate",
    taxBracket: 0.22,
    healthStatus: "good",
    hasSpouse: true,
    spouseAge: 69,
    existingAnnuities: 100000,
    investmentGoals: [
      "Stable income",
      "Inflation protection",
      "Joint survivor benefits"
    ]
  }
];

// Sample annuity products
export const sampleAnnuityProducts: AnnuityProduct[] = [
  {
    id: "FIXED-001",
    name: "Secure Income Fixed Annuity",
    type: "fixed",
    provider: "American Life Insurance Co.",
    minimumPremium: 25000,
    currentRate: 0.045, // 4.5%
    feePercentage: 0.01,
    surrenderPeriod: 7,
    surrenderCharge: 0.08,
    riderOptions: [
      "Cost of Living Adjustment (COLA)",
      "Enhanced Death Benefit"
    ],
    features: [
      "Guaranteed rate for 5 years",
      "No market risk",
      "Predictable payments"
    ]
  },
  {
    id: "VAR-001",
    name: "Growth Plus Variable Annuity",
    type: "variable",
    provider: "National Investment Services",
    minimumPremium: 50000,
    feePercentage: 0.025,
    surrenderPeriod: 8,
    surrenderCharge: 0.10,
    riderOptions: [
      "Guaranteed Minimum Income Benefit (GMIB)",
      "Guaranteed Minimum Withdrawal Benefit (GMWB)",
      "Long-term Care Rider"
    ],
    features: [
      "Multiple investment subaccounts",
      "Market participation",
      "Tax-deferred growth",
      "Death benefit protection"
    ]
  },
  {
    id: "INDEX-001",
    name: "Market Edge Indexed Annuity",
    type: "indexed",
    provider: "Premier Financial Group",
    minimumPremium: 35000,
    feePercentage: 0.015,
    surrenderPeriod: 10,
    surrenderCharge: 0.09,
    riderOptions: [
      "Income for Life Rider",
      "Enhanced Death Benefit",
      "Nursing Home Waiver"
    ],
    features: [
      "Upside market participation (cap rate 6%)",
      "Downside protection (0% floor)",
      "Annual reset",
      "Multiple index options (S&P 500, NASDAQ)"
    ]
  },
  {
    id: "IMMED-001",
    name: "Instant Income Immediate Annuity",
    type: "immediate",
    provider: "Retirement Solutions Inc.",
    minimumPremium: 100000,
    currentRate: 0.055, // 5.5% payout rate
    feePercentage: 0,
    surrenderPeriod: 0,
    surrenderCharge: 0,
    riderOptions: [
      "Period Certain (10, 15, 20 years)",
      "Joint Life with 100% Survivor",
      "Cost of Living Adjustment"
    ],
    features: [
      "Payments start within 30 days",
      "Lifetime income guarantee",
      "Simple and transparent",
      "No ongoing fees"
    ]
  },
  {
    id: "DEFER-001",
    name: "Future Wealth Deferred Annuity",
    type: "deferred",
    provider: "Strategic Retirement Planning",
    minimumPremium: 40000,
    currentRate: 0.048, // 4.8%
    feePercentage: 0.012,
    surrenderPeriod: 6,
    surrenderCharge: 0.07,
    riderOptions: [
      "Income Doubler for Long-term Care",
      "Enhanced Death Benefit",
      "Return of Premium"
    ],
    features: [
      "Flexible deferral period (5-30 years)",
      "Guaranteed minimum rate (2.5%)",
      "Tax-deferred accumulation",
      "Multiple payout options at maturity"
    ]
  }
];

// Current market rates (mock data with realistic 2025 estimates)
export const currentMarketRates: MarketRates = {
  fixedAnnuityRate: 0.045,        // 4.5% average fixed annuity rate
  variableAnnuityAvgReturn: 0.068, // 6.8% historical average
  indexedAnnuityCap: 0.06,         // 6% cap rate for indexed annuities
  treasuryYield10Year: 0.042,      // 4.2% 10-year Treasury yield
  inflationRate: 0.028,            // 2.8% inflation estimate
  lastUpdated: "2025-01-15"
};

// Sample portfolio allocations
export const samplePortfolioAllocations: Record<string, PortfolioAllocation> = {
  conservative: {
    stocks: 30,
    bonds: 40,
    cash: 10,
    annuities: 15,
    other: 5
  },
  moderate: {
    stocks: 50,
    bonds: 30,
    cash: 5,
    annuities: 10,
    other: 5
  },
  aggressive: {
    stocks: 70,
    bonds: 15,
    cash: 5,
    annuities: 5,
    other: 5
  },
  retirement: {
    stocks: 20,
    bonds: 30,
    cash: 15,
    annuities: 30,
    other: 5
  }
};

// Helper function to get a sample client by name or index
export function getSampleClient(identifier: string | number): ClientProfile | undefined {
  if (typeof identifier === 'number') {
    return sampleClients[identifier];
  }
  return sampleClients.find(client =>
    client.name.toLowerCase().includes(identifier.toLowerCase())
  );
}

// Helper function to get annuity product by type or ID
export function getAnnuityProduct(identifier: string): AnnuityProduct | undefined {
  return sampleAnnuityProducts.find(product =>
    product.id === identifier || product.type === identifier
  );
}

// Helper function to get all annuity products by type
export function getAnnuityProductsByType(type: string): AnnuityProduct[] {
  return sampleAnnuityProducts.filter(product => product.type === type);
}
