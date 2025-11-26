# Google Drive Agent - Changelog

## [1.1.0] - 2025-01-13

### Added - Shared Drive Support

#### New Features
- **Full Shared Drive (Team Drive) access** across all operations
- **New tool: `list_shared_drives`** - Discover all Shared Drives you have access to
- **Enhanced search capabilities** - Added `name_only` parameter to search only file names (not content)

#### Modified Tools
1. **search_files**
   - Now searches both My Drive and Shared Drives automatically
   - Added `name_only` parameter for precise filename searches
   - Example: `search_files("report", name_only=True)`

2. **list_folder**
   - Now works with both My Drive folders and Shared Drive folders
   - Can browse Shared Drive contents using Shared Drive ID
   - Example: `list_folder('0AB1DZwGY9h1VUk9PVA')`

3. **get_file_content**
   - Now extracts content from files in My Drive AND Shared Drives
   - No changes to API - works transparently with all file locations

4. **list_shared_drives** (NEW)
   - Lists all Shared Drives user has access to
   - Returns Drive ID and name for each Shared Drive
   - No parameters required

#### Technical Changes
- Added `supportsAllDrives=True` to all Google Drive API calls
- Added `includeItemsFromAllDrives=True` to include Shared Drive items in results
- Implemented `drives().list()` endpoint for Shared Drive discovery
- Updated agent description to reflect 4 tools instead of 3

#### Documentation Updates
- README.md: Added Shared Drive features, tool examples, and usage scenarios
- CLAUDE.md: Updated architecture, tool descriptions, and capabilities
- Memory system: Documented patterns and learnings from implementation

### Testing
- ✅ Verified all 4 tools working with real Shared Drive
- ✅ Successfully listed Shared Drive: "generative-bricks-corporate"
- ✅ Successfully browsed Shared Drive contents (8 folders)
- ✅ Verified search functionality within Shared Drives

### Implementation Time
- ~15 minutes total (including testing)
- Demonstrates incremental feature enhancement approach

---

## [1.0.0] - 2025-01-11

### Initial Release

#### Core Features
- OAuth 2.0 authentication with token caching
- Smart content caching to avoid re-downloads
- Support for all major file types (Docs, Sheets, PDFs, Word, Excel, Text)
- Direct context passing (no RAG pipeline needed)

#### Tools (3)
1. search_files - Search Google Drive by query
2. list_folder - Browse folder contents
3. get_file_content - Extract full text from any file

#### Architecture
- Service-based design: AuthService, DriveService, ContentExtractor, CacheService
- Production-ready error handling and logging
- ~1,010 lines of source code

