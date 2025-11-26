# Google Drive Document Assistant

A Python-based Strands agent that enables natural language Q&A, search, and document summarization over your Google Drive files - **without complex RAG infrastructure**.

## 🎯 Purpose

Ground your questions in Google Drive content by directly accessing files. The agent searches, reads, and analyzes documents using the LLM's large context window (no vector databases or embeddings needed).

## ✨ Features

- 🔍 **Search Google Drive** - Find files by keyword across names and content (supports full-text and name-only search)
- 📂 **Browse Folders** - Navigate folder structures in My Drive and Shared Drives
- 🗂️ **Access Shared Drives** - List and access all Shared Drives (Team Drives) you have permissions for
- 📄 **Extract Content** - Read text from Docs, Sheets, PDFs, Word, Excel, and more
- 💬 **Answer Questions** - Ask questions grounded in actual file content
- 📊 **Summarize Documents** - Get summaries of single files or collections
- 💾 **Smart Caching** - Avoid re-downloading unchanged files

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ installed
- `uv` package manager ([install here](https://github.com/astral-sh/uv))
- Google account with Drive access
- AWS credentials (for Bedrock) or Gemini API key

### 1. Install Dependencies

```bash
# Navigate to project directory
cd agents/strands-agents/python/google-drive-agent

# Create virtual environment using uv
uv venv

# Activate virtual environment (Windows Git Bash)
source .venv/Scripts/activate

# Install dependencies
uv pip install -r requirements.txt
```

### 2. Set Up Google Drive API

#### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Create Project** or select existing project
3. Note the Project ID

#### Step 2: Enable Google Drive API

1. Navigate to **APIs & Services** > **Library**
2. Search for "**Google Drive API**"
3. Click **Enable**

#### Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. If prompted, configure OAuth consent screen:
   - Select **External** (or Internal if using Google Workspace)
   - App name: "Google Drive Document Assistant"
   - User support email: Your email
   - Developer contact: Your email
   - Click **Save and Continue** (skip scopes, test users)
4. Back in Credentials, create **OAuth client ID**:
   - Application type: **Desktop app**
   - Name: "Drive Agent Desktop Client"
   - Click **Create**
5. **Download** the JSON file
6. Rename it to `credentials.json`
7. Move it to: `credentials/credentials.json`

### 3. Configure Environment (Optional)

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env if needed (optional - defaults work fine)
nano .env
```

### 4. Run the Agent

```bash
# Interactive mode (conversation loop)
uv run python src/main.py

# Single query mode
uv run python src/main.py "What files are in my Research Papers folder?"
```

#### First Run: OAuth Flow

On first run, the agent will:
1. Open your browser automatically
2. Ask you to log in to Google
3. Request permission to read your Drive (read-only access)
4. Save a token for future runs (no browser needed next time)

## 📖 Usage Examples

### Example 1: Search for a File

```
You: Find my Q4 budget document

Agent: 🔧 Using tool: search_files...
      Found "Q4_Budget_2024.pdf" in your Drive.
      File ID: abc123xyz
      Last modified: 2024-01-15

You: Read it and tell me the marketing budget.

Agent: 🔧 Using tool: get_file_content...
      According to the Q4 Budget document, the marketing budget is $125,000,
      allocated as follows:
      - Digital advertising: $60,000
      - Content creation: $35,000
      - Events: $30,000
```

### Example 2: Browse a Folder

```
You: What's in my "Research Papers" folder?

Agent: 🔧 Using tool: list_folder...
      Your "Research Papers" folder contains:

      Files (8):
      1. quantum_computing_review.pdf
      2. machine_learning_trends.docx
      3. ai_ethics_framework.pdf
      ...

      Subfolders (2):
      1. 2024 Papers
      2. Archive
```

### Example 4: Access Shared Drives

```
You: List my Shared Drives

Agent: 🔧 Using tool: list_shared_drives...
      I found one Shared Drive: "generative-bricks-corporate"

You: What's in that Shared Drive?

Agent: 🔧 Using tool: list_folder...
      The Shared Drive 'generative-bricks-corporate' contains 8 folders:
      - 01_advisorcrm
      - 02_clients
      - 03_products
      - 04_internal
      - 05_speaking-engagements
      - 06_knowledge-base
      ...
```

### Example 3: Summarize a Document

```
You: Summarize the project_proposal.docx file

Agent: 🔧 Using tool: search_files...
      🔧 Using tool: get_file_content...

      **Summary of project_proposal.docx:**

      The proposal outlines a 6-month initiative to modernize the customer
      portal. Key points:
      - Budget: $250K
      - Timeline: Q2-Q3 2024
      - Team: 5 developers, 1 designer
      - Expected outcomes: 40% faster load times, improved UX
```

## 🛠️ Architecture

### The Simple Approach (No RAG Needed)

Traditional RAG systems require:
- ❌ Vector databases (ChromaDB, Pinecone, etc.)
- ❌ Embedding models (expensive or compute-heavy)
- ❌ Chunking strategies
- ❌ Retrieval pipelines

**This agent doesn't need any of that** because:
- ✅ Modern LLMs have huge context windows (200K-2M tokens)
- ✅ You're working with 1 file at a time (not thousands)
- ✅ Files are small-to-medium size (5-20 pages each)
- ✅ Content fits easily in context

### Component Flow

```
User Query
    ↓
Search Files (search_files tool)
    ↓
Get File Content (get_file_content tool)
    ↓
LLM Context (full file content available)
    ↓
Answer Question
```

That's it. Simple and effective.

## 📂 Project Structure

```
google-drive-agent/
├── src/
│   ├── agent.py                 # Main agent class
│   ├── main.py                  # CLI entry point
│   ├── services/
│   │   ├── auth_service.py      # OAuth authentication
│   │   ├── drive_service.py     # Google Drive API wrapper
│   │   ├── content_extractor.py # Text extraction from files
│   │   └── cache_service.py     # Content caching
│   ├── tools/
│   │   └── drive_tools.py       # Strands agent tools
│   └── config/
│       └── settings.py          # Configuration management
├── credentials/
│   └── credentials.json         # OAuth credentials (gitignored)
├── data/
│   └── cache/                   # Cached file content
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## 🔧 Tools Available

### 1. `search_files`

Search Google Drive by keyword (searches both My Drive and Shared Drives).

**Parameters:**
- `query` (str): Search query
- `folder_id` (optional): Limit search to folder
- `limit` (int): Max results (default 10)
- `name_only` (bool): Search only file names, not content (default False)

**Returns:** List of matching files with metadata

**Examples:**
- `search_files("budget 2024")` → Full-text search across all files
- `search_files("report", name_only=True)` → Search only file names

### 2. `list_folder`

Browse folder contents (works with My Drive folders and Shared Drive folders).

**Parameters:**
- `folder_id` (str): Folder ID to list (use 'root' for My Drive)
- `include_files` (bool): Include files
- `include_folders` (bool): Include subfolders

**Returns:** Files and folders in the specified folder

**Examples:**
- `list_folder('root')` → List My Drive contents
- `list_folder('0AB1DZwGY9h1VUk9PVA')` → List Shared Drive contents

### 3. `get_file_content`

Extract full text from any file (supports files from My Drive and Shared Drives).

**Parameters:**
- `file_id` (str): File ID to extract content from

**Returns:** Full file content as text

**Supported File Types:**
- Google Docs, Sheets, Slides
- PDF (text-based, not scanned)
- Word (.docx)
- Excel (.xlsx)
- Plain text, CSV

### 4. `list_shared_drives`

List all Shared Drives (Team Drives) you have access to.

**Parameters:** None

**Returns:** List of Shared Drives with ID and name

**Example:**
- `list_shared_drives()` → Returns all accessible Shared Drives

## 🔒 Security & Privacy

- **Read-only access**: Agent can only read files, never modify or delete
- **OAuth 2.0**: Industry-standard authentication
- **Local credentials**: Token stored locally (credentials/token.json)
- **No data transmission**: Files only sent to your chosen LLM (Bedrock/Gemini)
- **Transparent operations**: All file access is logged and visible

## 🚫 Troubleshooting

### Issue: "credentials.json not found"

**Solution**: Follow Step 2 (Google Drive API Setup) to create and download credentials.

### Issue: "Failed to refresh credentials"

**Solution**: Delete `credentials/token.json` and re-authenticate:
```bash
rm credentials/token.json
uv run python src/main.py
```

### Issue: "Unsupported file type"

**Solution**: Currently supported types are:
- Google Workspace files (Docs, Sheets, Slides)
- PDF (text-based only, not scanned images)
- Microsoft Office (Word, Excel)
- Plain text, CSV

For scanned PDFs, OCR would be needed (not currently implemented).

### Issue: "Rate limit exceeded"

**Solution**: Google Drive API has rate limits. If hit:
- Wait a few minutes
- Enable caching (avoids re-downloading files)
- Reduce number of files processed at once

## 📊 Cache Management

### View Cache Stats

```bash
# In interactive mode, type:
cache stats
```

Shows:
- Number of cached files
- Total cache size (MB)
- Cache location

### Clear Cache

```bash
# In interactive mode, type:
cache clear
```

Useful when:
- Files have been updated in Drive
- Testing content extraction
- Freeing disk space

## 🧪 Testing

Run tests with:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_drive_tools.py

# Run with coverage
pytest --cov=src tests/
```

## 🔄 Development Workflow

### Adding New File Type Support

1. Add MIME type mapping in `content_extractor.py`
2. Implement extraction method (e.g., `_extract_pptx`)
3. Update README with supported type
4. Add tests

### Extending Tools

1. Add tool function in `drive_tools.py`
2. Define Pydantic input schema
3. Add tool to factory function
4. Update agent description in `agent.py`

## 📝 License

MIT License - see LICENSE file

## 🤝 Contributing

Contributions welcome! Please:
1. Follow existing code style
2. Add tests for new features
3. Update documentation
4. Submit PR with clear description

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check troubleshooting section above
- Review Google Drive API documentation

---

**Built with:**
- [Strands Agents](https://strands.ai/) - Agent framework
- [Google Drive API](https://developers.google.com/drive) - File access
- [Claude (Bedrock)](https://aws.amazon.com/bedrock/) - LLM reasoning

**Repository:** [claude-code-agent](https://github.com/yourusername/claude-code-agent)

**Last Updated:** January 2025