# FIA Product Analyzer - Complete Package

This package contains everything you need to analyze Fixed Indexed Annuities (FIAs) using Claude.

---

## 📦 What's Included

### 1. Example Analysis (Allianz Benefit Control)
- **`allianz_benefit_control_analysis.md`** - Markdown version (LLM-friendly)
- **`allianz_benefit_control_analysis.pdf`** - PDF version (professional)

These demonstrate the complete output you'll get for any FIA product.

### 2. The Skill
- **`fia-product-analyzer-skill/SKILL.md`** - Complete skill definition

This is the reusable framework you can use in any Claude chat to analyze FIA products.

### 3. Instructions & Quick Start
- **`FIA_SKILL_INSTRUCTIONS.md`** - Comprehensive guide on how to use the skill
- **`QUICK_START_PROMPT.md`** - Copy-paste templates to get started immediately

---

## 🚀 Quick Start (3 Options)

### Option 1: Use the Skill File
1. Open the **`fia-product-analyzer-skill/SKILL.md`** file
2. Copy its entire contents
3. In a new Claude chat, paste it and say: "Use this skill to analyze [Product Name]"

### Option 2: Use the Quick Start Prompt
1. Open **`QUICK_START_PROMPT.md`**
2. Copy the prompt template
3. Fill in the product name and client details (optional)
4. Paste into a new Claude chat

### Option 3: Manual Request
Just ask Claude in a new chat:
```
Analyze the [Product Name] FIA with surrender charges, index options, 
crediting methods, riders, fees, and a 40-question suitability assessment. 
Output in both Markdown and PDF formats.
```

---

## 🎯 What You'll Get

Every analysis includes:

### Product Data
- Surrender charge schedule (10 years)
- All index options with descriptions
- Crediting methods (point-to-point, multi-year, etc.)
- Current caps and participation rates
- Riders (built-in and optional) with costs
- Special features (Index Lock, bonuses, etc.)
- Commission structure
- Company information

### Suitability Analysis
- 40-question assessment
- Smart scoring that handles missing data
- Good fit profile (8-10 categories)
- Not a fit profile (8-10 categories)
- Score interpretation
- Clear recommendations

### Output Formats
- **Markdown** - LLM-friendly, searchable, easy to parse
- **PDF** - Professional formatting, ready for presentations

---

## 📊 Understanding the Scoring System

### How It Works
```
Suitability Score = (Total YES answers ÷ Total Answerable Questions) × 100
```

**Key Feature:** Questions without data are marked "N/A" and excluded from calculation.

### Example
- 40 total questions
- 10 questions can't be answered (N/A)
- 30 answerable questions
- 24 answered YES
- **Score = (24 ÷ 30) × 100 = 80% (Highly Suitable)**

### Interpretation
| Score | Result | Action |
|-------|--------|--------|
| 80-100% | Highly Suitable | ✅ Proceed with confidence |
| 60-79% | Suitable | ⚠️ Address minor concerns |
| 40-59% | Marginal | 🔍 Detailed review needed |
| <40% | Not Suitable | ❌ Recommend alternatives |

---

## 📋 The 40-Question Framework

Questions cover 11 categories:

1. **Financial Capacity** (5 questions) - Can afford, can commit, has reserves
2. **Age & Time Horizon** (3 questions) - Appropriate age, longevity expectations
3. **Investment Objectives** (5 questions) - Goals, protection needs, return expectations
4. **Risk Tolerance** (4 questions) - Conservative preference, volatility comfort
5. **Liquidity Needs** (3 questions) - Access requirements, emergency funds
6. **Understanding** (4 questions) - Product comprehension, fee awareness
7. **Health & Long-Term Care** (3 questions) - Health status, care planning
8. **Tax Situation** (3 questions) - Tax benefits, withdrawal penalties
9. **Alternative Options** (3 questions) - Comparison awareness, due diligence
10. **Product Features** (4 questions) - Interest in specific features
11. **Disqualifying Factors** (3 questions) - Major red flags (reverse scored)

---

## 💡 Use Cases

### For Financial Advisors
- ✅ Product due diligence
- ✅ Client suitability determination  
- ✅ Compliance documentation
- ✅ Client presentations
- ✅ Training materials

### For Internal Analysis
- ✅ Product comparison
- ✅ Competitive intelligence
- ✅ Rate shopping
- ✅ Portfolio construction
- ✅ Knowledge base building

### For LLM/Agent Systems
- ✅ Automated recommendations
- ✅ Client matching
- ✅ Portfolio optimization
- ✅ Compliance checking
- ✅ Natural language queries

---

## 🔧 Customization

The framework is flexible and can be customized:

### Adjust Questions
- Add product-specific questions
- Remove irrelevant questions
- Modify for different client types

### Change Thresholds
- Adjust score interpretation ranges
- Add custom categories
- Modify weighting

### Enhance Output
- Add company branding
- Include comparison tables
- Customize PDF styling

---

## 📝 Example Prompts

### Basic Analysis
```
Analyze the Nationwide Peak 10 FIA
```

### With Client Context
```
Analyze the Lincoln OptiBlend 10 for a 58-year-old conservative 
investor with $75,000 who needs guaranteed income starting in 5 years
```

### Multiple Products
```
Compare these FIAs:
1. Allianz Benefit Control
2. Nationwide Peak 10  
3. F&G Prosperity Elite
```

### Update Existing Analysis
```
Update my Allianz Benefit Control analysis with current rates as of today
```

---

## 🎓 Best Practices

### Do:
✅ Be specific with product names
✅ Provide client context when available
✅ Request both Markdown and PDF
✅ Acknowledge data limitations
✅ Verify critical information independently

### Don't:
❌ Make up data if unavailable
❌ Guarantee future performance
❌ Ignore fees and charges
❌ Skip disclaimers
❌ Recommend without understanding needs

---

## 📚 File Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| **allianz_benefit_control_analysis.md** | Example output (Markdown) | Review sample format |
| **allianz_benefit_control_analysis.pdf** | Example output (PDF) | See professional styling |
| **fia-product-analyzer-skill/SKILL.md** | Skill definition | Install as Claude skill |
| **FIA_SKILL_INSTRUCTIONS.md** | Detailed guide | Learn how to use |
| **QUICK_START_PROMPT.md** | Copy-paste templates | Start immediately |
| **README.md** | This file | Overview of package |

---

## 🔄 Workflow Example

**Step 1:** Choose your starting method (Skill, Quick Start, or Manual)

**Step 2:** Provide product name and optional client context

**Step 3:** Claude will:
- Search for current product information
- Gather all data points
- Create comprehensive analysis
- Generate both Markdown and PDF
- Save to outputs with download links

**Step 4:** Review outputs and request adjustments if needed

**Step 5:** Use suitability score to guide recommendations

---

## ⚠️ Important Notes

### Data Accuracy
- Rates and features change frequently
- Always verify current information
- Note when data was collected
- Confirm with product materials

### Disclaimers
- Not investment advice
- For informational purposes only
- Consult licensed professionals
- Past performance ≠ future results

### Limitations
- Some data may be unavailable
- Rates are not guaranteed
- Product variations exist by state
- Scoring is a tool, not a decision

---

## 🆘 Troubleshooting

**Q: Skill doesn't trigger**
A: Include "FIA" or "Fixed Indexed Annuity" in your request

**Q: Missing data in analysis**
A: Normal - not all info is public. Questions marked N/A automatically

**Q: PDF formatting issues**
A: Request specific formatting or use Markdown version

**Q: Need to update rates**
A: Say "Update with current rates as of [date]"

**Q: Want to modify questions**
A: Ask Claude to add/remove/change specific questions

---

## 📞 Getting Help

**In Your Claude Chat:**
- "How do I use the FIA Product Analyzer?"
- "Explain the suitability scoring"
- "Show me an example analysis"
- "What questions are included?"

**Review These Files:**
1. Start with: `QUICK_START_PROMPT.md`
2. For details: `FIA_SKILL_INSTRUCTIONS.md`  
3. For example: `allianz_benefit_control_analysis.pdf`
4. For framework: `fia-product-analyzer-skill/SKILL.md`

---

## 🎉 You're Ready!

Pick your preferred starting method and begin analyzing FIA products. The framework handles the complexity while you focus on matching products to client needs.

**Questions? Just ask Claude!**

---

*Created: November 12, 2025*  
*Version: 1.0*  
*Framework: FIA Product Analyzer*
