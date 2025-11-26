# OpportunityIQ Client Matcher - Production Deployment Guide

**Status:** Production Deployment Roadmap  
**Version:** 1.0.0  
**Last Updated:** 2025-01-21

---

## 📋 Overview

This guide outlines multiple paths to deploy the OpportunityIQ Client Matcher to production as a web application. The agent currently runs as a CLI tool, and this document provides step-by-step instructions for web deployment.

### Current State

- ✅ **CLI Application** - Fully functional command-line interface
- ✅ **Agent Class** - `OpportunityIQAgent` with complete workflow
- ✅ **Three-Layer Architecture** - Models, Services, Tools
- ✅ **5 Core Tools** - All matching and reporting functionality
- ✅ **JSON-Based Data** - Scenarios and clients stored as JSON files

### Production Goals

- 🌐 **Web API** - RESTful API for programmatic access
- 🖥️ **Web Interface** - User-friendly web UI for advisors
- 🔐 **Authentication** - Secure access control
- 📊 **Dashboard** - Visual opportunity reports
- 💾 **Data Management** - Upload/manage clients and scenarios via UI

---

## 🎯 Deployment Options

### Option 1: FastAPI + React (Recommended)

**Best for:** Full-featured web application with modern UI

**Stack:**
- **Backend:** FastAPI (Python)
- **Frontend:** React + TypeScript
- **Database:** SQLite (MVP) or PostgreSQL (production)
- **Deployment:** Docker + Cloud (AWS, GCP, Azure)

**Pros:**
- Modern, fast API framework
- Auto-generated API documentation (Swagger/OpenAPI)
- Type-safe frontend with TypeScript
- Easy to scale horizontally
- Great developer experience

**Cons:**
- Requires frontend development
- More complex deployment

**Timeline:** 2-3 weeks

---

### Option 2: FastAPI + Simple HTML/JavaScript

**Best for:** Quick deployment with minimal frontend work

**Stack:**
- **Backend:** FastAPI (Python)
- **Frontend:** Vanilla JavaScript + HTML/CSS
- **Database:** JSON files (MVP) or SQLite
- **Deployment:** Docker + Cloud

**Pros:**
- Fastest to deploy
- No build process needed
- Simple to maintain
- Works well for internal tools

**Cons:**
- Less modern UI
- Limited interactivity
- Harder to scale frontend features

**Timeline:** 1 week

---

### Option 3: Streamlit (Simplest)

**Best for:** Rapid prototyping and internal tools

**Stack:**
- **Framework:** Streamlit (Python)
- **Database:** JSON files or SQLite
- **Deployment:** Streamlit Cloud or Docker

**Pros:**
- Fastest deployment (hours, not days)
- No frontend code needed
- Built-in UI components
- Great for data apps

**Cons:**
- Less customizable UI
- Not ideal for external users
- Limited real-time features

**Timeline:** 2-3 days

---

### Option 4: Flask + Jinja2 Templates

**Best for:** Traditional web application

**Stack:**
- **Backend:** Flask (Python)
- **Frontend:** Jinja2 templates + Bootstrap
- **Database:** SQLite or PostgreSQL
- **Deployment:** Docker + Cloud

**Pros:**
- Simple, familiar framework
- Server-side rendering
- Easy to get started
- Good for traditional web apps

**Cons:**
- Less modern than FastAPI
- Limited real-time capabilities
- More boilerplate code

**Timeline:** 1-2 weeks

---

## 🚀 Recommended Path: FastAPI + React

This section provides a complete implementation guide for Option 1 (FastAPI + React).

### Phase 1: FastAPI Backend (Week 1)

#### Step 1: Create API Structure

```
opportunityiq-client-matcher/
├── src/
│   ├── api/                    # NEW: API layer
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app
│   │   ├── config.py           # Settings
│   │   ├── dependencies.py     # Auth, DB connections
│   │   └── routes/             # API endpoints
│   │       ├── __init__.py
│   │       ├── analysis.py     # Analysis endpoints
│   │       ├── clients.py      # Client management
│   │       ├── scenarios.py    # Scenario management
│   │       └── reports.py      # Report generation
│   ├── agent.py                # Existing agent
│   ├── models/                 # Existing models
│   ├── services/               # Existing services
│   └── tools/                  # Existing tools
├── frontend/                    # NEW: React app
│   ├── src/
│   ├── public/
│   └── package.json
└── docker-compose.yml          # NEW: Docker setup
```

#### Step 2: Install FastAPI Dependencies

Add to `requirements.txt`:

```txt
# Web API
fastapi>=0.104.0,<1.0.0
uvicorn[standard]>=0.24.0,<1.0.0
python-multipart>=0.0.6,<1.0.0  # File uploads
pydantic-settings>=2.0.0,<3.0.0  # Settings management

# Authentication (optional for MVP)
python-jose[cryptography]>=3.3.0,<4.0.0
passlib[bcrypt]>=1.7.4,<2.0.0

# CORS
python-cors>=1.0.0,<2.0.0
```

#### Step 3: Create FastAPI Application

**File:** `src/api/main.py`

```python
"""
FastAPI Main Application for OpportunityIQ Client Matcher.

Provides REST API endpoints for web-based client matching and opportunity analysis.

Biblical Principle: SERVE - Simple, accessible API for powerful opportunity matching.
Biblical Principle: EXCELLENCE - Production-ready API with comprehensive error handling.
"""

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.logs_dir / "api.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("=" * 80)
    logger.info("OpportunityIQ API Starting")
    logger.info("=" * 80)
    logger.info(f"Environment: {'Development' if settings.api_reload else 'Production'}")
    logger.info(f"Host: {settings.api_host}:{settings.api_port}")
    logger.info(f"Scenarios Directory: {settings.scenarios_directory}")
    
    # Verify Anthropic API key
    if not settings.anthropic_api_key:
        logger.warning("⚠️  ANTHROPIC_API_KEY not set - AI insights will fail")
    else:
        logger.info("✓ Anthropic API key configured")
    
    logger.info("=" * 80)
    logger.info("API Ready")
    logger.info("=" * 80)
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("=" * 80)
    logger.info("OpportunityIQ API Shutting Down")
    logger.info("=" * 80)


# Create FastAPI app
app = FastAPI(
    title="OpportunityIQ Client Matcher API",
    description="Match financial advisor clients to revenue opportunity scenarios",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "type": type(exc).__name__,
        },
    )


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "OpportunityIQ Client Matcher API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "anthropic_configured": bool(settings.anthropic_api_key),
    }


# Import and register routes
from src.api.routes import analysis, clients, scenarios, reports

app.include_router(analysis.router, prefix="/api", tags=["Analysis"])
app.include_router(clients.router, prefix="/api", tags=["Clients"])
app.include_router(scenarios.router, prefix="/api", tags=["Scenarios"])
app.include_router(reports.router, prefix="/api", tags=["Reports"])

logger.info("✓ API routes registered")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower(),
    )
```

#### Step 4: Create API Configuration

**File:** `src/api/config.py`

```python
"""API configuration settings."""

from pathlib import Path
from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    """API configuration settings."""
    
    # API Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logs_dir: Path = Path("logs")
    
    # Anthropic
    anthropic_api_key: str = ""
    
    # Data Paths
    scenarios_directory: str = "data/scenarios"
    clients_directory: str = "data/clients"
    reports_directory: str = "outputs"
    
    # Matching Defaults
    min_match_threshold: float = 60.0
    default_match_weight: float = 0.4
    default_revenue_weight: float = 0.6
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = APISettings()
```

#### Step 5: Create Analysis Endpoint

**File:** `src/api/routes/analysis.py`

```python
"""Analysis API endpoints."""

import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from src.agent import OpportunityIQAgent
from src.models import ClientProfile, Opportunity

logger = logging.getLogger(__name__)
router = APIRouter()


class AnalysisRequest(BaseModel):
    """Request model for analysis endpoint."""
    clients: List[dict]
    scenarios: Optional[List[dict]] = None
    min_match_threshold: float = 60.0
    ranking_strategy: str = "composite"
    match_weight: float = 0.4
    revenue_weight: float = 0.6
    limit: Optional[int] = None
    generate_insights: bool = False
    insights_count: int = 3


class AnalysisResponse(BaseModel):
    """Response model for analysis endpoint."""
    success: bool
    opportunities: List[dict]
    summary: dict
    report: str
    config: dict
    ai_insights: Optional[List[dict]] = None


def get_agent() -> OpportunityIQAgent:
    """Dependency to get agent instance."""
    return OpportunityIQAgent()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_clients(
    request: AnalysisRequest,
    agent: OpportunityIQAgent = Depends(get_agent)
):
    """
    Analyze clients for revenue opportunities.
    
    Matches client profiles against scenarios and generates prioritized reports.
    """
    try:
        # Convert client dicts to ClientProfile objects
        clients = [ClientProfile(**client) for client in request.clients]
        
        # Run analysis
        results = agent.analyze_clients(
            clients=clients,
            scenarios=request.scenarios,
            min_match_threshold=request.min_match_threshold,
            ranking_strategy=request.ranking_strategy,
            match_weight=request.match_weight,
            revenue_weight=request.revenue_weight,
            limit=request.limit,
            report_format="json"  # Return JSON for API
        )
        
        # Generate AI insights if requested
        ai_insights = None
        if request.generate_insights:
            ai_insights = agent.generate_insights_with_llm(
                opportunities=results["opportunities"],
                top_n=request.insights_count
            )
        
        # Convert opportunities to dicts
        opportunities_dict = [
            opp.model_dump() for opp in results["opportunities"]
        ]
        
        return AnalysisResponse(
            success=True,
            opportunities=opportunities_dict,
            summary=results["summary"],
            report=results["report"],
            config=results["config"],
            ai_insights=ai_insights
        )
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
```

#### Step 6: Create Additional Endpoints

**File:** `src/api/routes/clients.py`

```python
"""Client management endpoints."""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

from src.agent import OpportunityIQAgent
from src.models import ClientProfile

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/clients")
async def list_clients(agent: OpportunityIQAgent = Depends(get_agent)):
    """List all available client files."""
    # Implementation: scan clients directory
    pass


@router.post("/clients/upload")
async def upload_clients(file: UploadFile = File(...)):
    """Upload client data JSON file."""
    # Implementation: save and validate uploaded file
    pass


@router.get("/clients/{client_id}")
async def get_client(client_id: str):
    """Get specific client profile."""
    # Implementation: load and return client
    pass
```

**File:** `src/api/routes/scenarios.py`

```python
"""Scenario management endpoints."""

import logging
from fastapi import APIRouter, Depends

from src.agent import OpportunityIQAgent

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/scenarios")
async def list_scenarios(agent: OpportunityIQAgent = Depends(get_agent)):
    """List all available scenarios."""
    info = agent.get_scenario_info()
    return info
```

**File:** `src/api/routes/reports.py`

```python
"""Report generation endpoints."""

import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from src.agent import OpportunityIQAgent

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/reports/{report_id}")
async def get_report(report_id: str):
    """Download generated report."""
    # Implementation: return report file
    pass
```

#### Step 7: Run API Server

```bash
# Development
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Phase 2: React Frontend (Week 2)

#### Step 1: Create React App

```bash
cd opportunityiq-client-matcher
npx create-react-app frontend --template typescript
cd frontend
npm install axios react-router-dom @tanstack/react-query
```

#### Step 2: Create API Client

**File:** `frontend/src/api/client.ts`

```typescript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface AnalysisRequest {
  clients: any[];
  scenarios?: any[];
  min_match_threshold?: number;
  ranking_strategy?: string;
  match_weight?: number;
  revenue_weight?: number;
  limit?: number;
  generate_insights?: boolean;
  insights_count?: number;
}

export interface Opportunity {
  client_name: string;
  scenario_name: string;
  match_score: number;
  estimated_revenue: number;
  priority: string;
  // ... other fields
}

export interface AnalysisResponse {
  success: boolean;
  opportunities: Opportunity[];
  summary: {
    total_opportunities: number;
    total_revenue: number;
    average_match_score: number;
  };
  report: string;
  config: any;
  ai_insights?: any[];
}

export const analyzeClients = async (request: AnalysisRequest): Promise<AnalysisResponse> => {
  const response = await apiClient.post<AnalysisResponse>('/api/analyze', request);
  return response.data;
};

export const getScenarios = async () => {
  const response = await apiClient.get('/api/scenarios');
  return response.data;
};
```

#### Step 3: Create Main Components

**File:** `frontend/src/components/AnalysisForm.tsx`

```typescript
import React, { useState } from 'react';
import { analyzeClients, AnalysisRequest } from '../api/client';

export const AnalysisForm: React.FC = () => {
  const [clients, setClients] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const request: AnalysisRequest = {
        clients,
        min_match_threshold: 60.0,
        ranking_strategy: 'composite',
        generate_insights: true,
      };
      
      const response = await analyzeClients(request);
      setResults(response);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Client upload/input form */}
      <button type="submit" disabled={loading}>
        {loading ? 'Analyzing...' : 'Run Analysis'}
      </button>
    </form>
  );
};
```

**File:** `frontend/src/components/OpportunityList.tsx`

```typescript
import React from 'react';
import { Opportunity } from '../api/client';

interface Props {
  opportunities: Opportunity[];
}

export const OpportunityList: React.FC<Props> = ({ opportunities }) => {
  return (
    <div className="opportunity-list">
      <h2>Opportunities ({opportunities.length})</h2>
      {opportunities.map((opp, idx) => (
        <div key={idx} className="opportunity-card">
          <h3>{opp.client_name} - {opp.scenario_name}</h3>
          <p>Match Score: {opp.match_score}%</p>
          <p>Revenue: ${opp.estimated_revenue.toLocaleString()}</p>
          <p>Priority: {opp.priority}</p>
        </div>
      ))}
    </div>
  );
};
```

### Phase 3: Docker Deployment (Week 3)

#### Step 1: Create Dockerfile

**File:** `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run API server
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Step 2: Create docker-compose.yml

**File:** `docker-compose.yml`

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - API_HOST=0.0.0.0
      - API_PORT=8000
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
      - ./logs:/app/logs
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - api
    restart: unless-stopped
```

#### Step 3: Deploy

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🚀 Quick Start: Streamlit Option (Fastest)

For the fastest deployment, use Streamlit:

### Step 1: Install Streamlit

```bash
uv pip install streamlit
```

### Step 2: Create Streamlit App

**File:** `streamlit_app.py`

```python
import streamlit as st
import json
from pathlib import Path
from src.agent import OpportunityIQAgent

st.set_page_config(
    page_title="OpportunityIQ Client Matcher",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 OpportunityIQ Client Matcher")

# Initialize agent
@st.cache_resource
def get_agent():
    return OpportunityIQAgent()

agent = get_agent()

# Sidebar: Configuration
with st.sidebar:
    st.header("Configuration")
    min_threshold = st.slider("Min Match Threshold", 0, 100, 60)
    match_weight = st.slider("Match Weight", 0.0, 1.0, 0.4)
    revenue_weight = st.slider("Revenue Weight", 0.0, 1.0, 0.6)
    top_n = st.number_input("Top N Opportunities", 1, 100, 25)

# Main: Client Upload
st.header("Upload Client Data")
uploaded_file = st.file_uploader("Upload JSON file", type=["json"])

if uploaded_file:
    clients_data = json.load(uploaded_file)
    clients = [ClientProfile(**c) for c in clients_data]
    
    if st.button("Run Analysis"):
        with st.spinner("Analyzing clients..."):
            results = agent.analyze_clients(
                clients=clients,
                min_match_threshold=min_threshold,
                match_weight=match_weight,
                revenue_weight=revenue_weight,
                limit=top_n
            )
        
        # Display results
        st.header("Results")
        st.metric("Total Opportunities", results["summary"]["total_opportunities"])
        st.metric("Total Revenue", f"${results['summary']['total_revenue']:,.2f}")
        
        # Display opportunities
        for opp in results["opportunities"]:
            with st.expander(f"{opp.client_name} - {opp.scenario_name}"):
                st.write(f"Match Score: {opp.match_score}%")
                st.write(f"Revenue: ${opp.estimated_revenue:,.2f}")
                st.write(f"Priority: {opp.priority}")
        
        # Download report
        st.download_button(
            "Download Report",
            results["report"],
            file_name="opportunity_report.md"
        )
```

### Step 3: Run Streamlit

```bash
streamlit run streamlit_app.py
```

**Deploy to Streamlit Cloud:**
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect repository
4. Deploy!

---

## 🔐 Authentication (Optional for MVP)

For production, add authentication:

### Option A: API Keys (Simplest)

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key
```

### Option B: JWT Tokens

```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
```

---

## 📊 Database Migration (Optional)

Currently uses JSON files. For production, consider:

### SQLite (MVP)

```python
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    client_id = Column(String, unique=True)
    data = Column(JSON)
```

### PostgreSQL (Production)

```python
# Use same SQLAlchemy models
# Change connection string to PostgreSQL
DATABASE_URL = "postgresql://user:pass@localhost/opportunityiq"
```

---

## 🚢 Deployment Platforms

### AWS (Recommended)

**Option 1: Elastic Beanstalk**
- Easiest AWS deployment
- Handles scaling automatically
- Good for MVP

**Option 2: ECS/Fargate**
- Container-based
- More control
- Better for production

**Option 3: Lambda + API Gateway**
- Serverless
- Pay per request
- Good for low traffic

### Google Cloud Platform

**Cloud Run**
- Container-based
- Auto-scaling
- Simple deployment

### Azure

**App Service**
- Managed service
- Easy deployment
- Good integration

### Heroku (Simplest)

```bash
# Install Heroku CLI
heroku create opportunityiq-matcher
git push heroku main
```

---

## 📝 Next Steps

1. **Choose deployment option** based on timeline and requirements
2. **Start with FastAPI backend** - Reuse existing agent code
3. **Add frontend** - React for full-featured, Streamlit for quick
4. **Add authentication** - API keys for MVP, JWT for production
5. **Deploy to cloud** - Start with Heroku/Streamlit Cloud, move to AWS/GCP later
6. **Monitor and iterate** - Add logging, metrics, error tracking

---

## 🔗 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Docker Documentation](https://docs.docker.com/)
- [AWS Deployment Guide](https://aws.amazon.com/getting-started/)

---

**Remember:** *"Whatever you do, work heartily, as for the Lord"* - Colossians 3:23

Start simple, deploy early, iterate based on user feedback.

---

*Last updated: 2025-01-21*
*Version: 1.0.0*





