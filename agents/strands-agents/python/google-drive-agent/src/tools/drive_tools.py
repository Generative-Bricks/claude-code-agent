"""
Strands Agent Tools for Google Drive Operations.

Provides three main tools:
1. search_files - Search Google Drive by query
2. list_folder - Browse folder contents
3. get_file_content - Extract full text from any file

Following SIMPLICITY principle: Each tool has one clear purpose with validation.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from strands import tool


# ============================================================================
# Tool Input Schemas (Pydantic models for validation)
# ============================================================================

class SearchFilesInput(BaseModel):
    """Input schema for search_files tool."""

    query: str = Field(
        description="Search query to find files (searches file names and content)"
    )
    folder_id: Optional[str] = Field(
        default=None,
        description="Optional Google Drive folder ID to search within"
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of results to return (1-50)"
    )


class ListFolderInput(BaseModel):
    """Input schema for list_folder tool."""

    folder_id: str = Field(
        description="Google Drive folder ID to list contents"
    )
    include_files: bool = Field(
        default=True,
        description="Include files in results"
    )
    include_folders: bool = Field(
        default=True,
        description="Include subfolders in results"
    )


class GetFileContentInput(BaseModel):
    """Input schema for get_file_content tool."""

    file_id: str = Field(
        description="Google Drive file ID to extract content from"
    )


# ============================================================================
# Tool Functions
# ============================================================================

def create_drive_tools(drive_service, content_extractor, cache_service):
    """
    Factory function to create tool functions with service dependencies.

    Args:
        drive_service: DriveService instance
        content_extractor: ContentExtractor instance
        cache_service: CacheService instance

    Returns:
        List of tool functions ready for Strands agent
    """

    @tool
    def search_files(query: str, folder_id: Optional[str] = None, limit: int = 10, name_only: bool = False) -> dict:
        """
        Search Google Drive for files matching a query.

        By default, this searches BOTH file names AND file content (full-text search).
        Set name_only=True to search ONLY file names.

        Search Examples:
        - search_files("budget 2024") → finds files with these words in name OR content
        - search_files("comprehensive", name_only=True) → finds only files with "comprehensive" in the name
        - search_files("report", folder_id="abc123", name_only=True) → name search within a folder

        To get a folder_id, use list_folder on 'root' first, or search for the folder name.

        Args:
            query: Search query string
            folder_id: Optional folder ID to search within (use 'root' for My Drive)
            limit: Maximum number of results to return (default 10, max 50)
            name_only: If True, search ONLY file names (not content). Default False.

        Returns:
            Dictionary with search results containing:
            - results: List of matching files with id, name, type, modified date, size, link
            - count: Number of results found

        Example:
            search_files("quarterly report", folder_id="abc123xyz", limit=5)
            search_files("budget", name_only=True)
        """
        try:
            # Execute search
            files = drive_service.search_files(
                query=query,
                folder_id=folder_id,
                limit=limit,
                name_only=name_only
            )

            # Format results for agent
            formatted_results = []
            for file in files:
                formatted_results.append({
                    'id': file['id'],
                    'name': file['name'],
                    'type': file['mimeType'],
                    'modified': file.get('modifiedTime', 'unknown'),
                    'size': file.get('size', 'N/A'),
                    'link': file.get('webViewLink', '')
                })

            return {
                'success': True,
                'query': query,
                'folder_id': folder_id,
                'count': len(formatted_results),
                'results': formatted_results
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to search files: {e}"
            }

    @tool
    def list_folder(
        folder_id: str,
        include_files: bool = True,
        include_folders: bool = True
    ) -> dict:
        """
        List contents of a Google Drive folder.

        This tool browses a specific folder and returns all files and/or subfolders contained within it.

        IMPORTANT: You need a folder_id to use this tool:
        - Use 'root' to list the main "My Drive" folder
        - Use a specific folder ID (like '1abc123xyz') to list that folder's contents
        - To find folder IDs, either:
          1. Use list_folder('root') first to see top-level folders
          2. Use search_files() to search for a folder by name

        Args:
            folder_id: Folder ID to list. Use 'root' for My Drive, or a specific folder ID
            include_files: Include files in results (default True)
            include_folders: Include subfolders in results (default True)

        Returns:
            Dictionary with folder contents containing:
            - files: List of files with id, name, type, modified date
            - folders: List of subfolders with id, name
            - total_count: Total number of items
            - file_count: Number of files
            - folder_count: Number of folders

        Examples:
            list_folder('root')  # List My Drive
            list_folder('1abc123xyz')  # List specific folder
        """
        try:
            # Execute list operation
            items = drive_service.list_folder(
                folder_id=folder_id,
                include_files=include_files,
                include_folders=include_folders
            )

            # Format results for agent
            formatted_items = []
            for item in items:
                item_type = 'folder' if 'folder' in item['mimeType'] else 'file'

                formatted_items.append({
                    'id': item['id'],
                    'name': item['name'],
                    'type': item_type,
                    'mime_type': item['mimeType'],
                    'modified': item.get('modifiedTime', 'unknown'),
                    'size': item.get('size', 'N/A'),
                    'link': item.get('webViewLink', '')
                })

            # Separate files and folders for clarity
            files = [i for i in formatted_items if i['type'] == 'file']
            folders = [i for i in formatted_items if i['type'] == 'folder']

            return {
                'success': True,
                'folder_id': folder_id,
                'total_count': len(formatted_items),
                'file_count': len(files),
                'folder_count': len(folders),
                'files': files,
                'folders': folders
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to list folder: {e}"
            }

    @tool
    def get_file_content(file_id: str) -> dict:
        """
        Extract full text content from a Google Drive file.

        This tool downloads a file and extracts all readable text content.
        Supports: Google Docs, Sheets, Slides, PDF, Word, Excel, and text files.

        The entire file content will be returned, so you can answer questions about it
        or summarize it without needing additional retrieval.

        Args:
            file_id: Google Drive file ID to extract content from

        Returns:
            Dictionary with file content containing:
            - content: Full extracted text content
            - metadata: File name, type, size, modified date
            - cached: Whether content was loaded from cache

        Example:
            get_file_content("abc123xyz")
        """
        try:
            # Get file metadata first
            metadata = drive_service.get_file_metadata(file_id)
            file_name = metadata.get('name', 'unknown')
            mime_type = metadata.get('mimeType', '')
            modified_time = metadata.get('modifiedTime', '')

            # Check cache first (if enabled)
            cached_content = None
            if cache_service:
                cached_content = cache_service.get(
                    file_id=file_id,
                    modified_time=modified_time,
                    file_name=file_name
                )

            if cached_content:
                # Return cached content
                return {
                    'success': True,
                    'file_id': file_id,
                    'file_name': file_name,
                    'mime_type': mime_type,
                    'modified': modified_time,
                    'content': cached_content,
                    'content_length': len(cached_content),
                    'cached': True
                }

            # Extract content (not in cache)
            content = content_extractor.extract_content(file_id, metadata)

            # Cache the extracted content (if caching enabled)
            if cache_service:
                cache_service.set(
                    file_id=file_id,
                    modified_time=modified_time,
                    content=content,
                    file_name=file_name,
                    mime_type=mime_type
                )

            return {
                'success': True,
                'file_id': file_id,
                'file_name': file_name,
                'mime_type': mime_type,
                'modified': modified_time,
                'content': content,
                'content_length': len(content),
                'cached': False
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to get file content: {e}"
            }

    @tool
    def list_shared_drives() -> dict:
        """
        List all Shared Drives (formerly Team Drives) you have access to.

        Shared Drives are collaborative spaces where teams can store, search, and access
        files from any device. Unlike "My Drive", files in Shared Drives belong to the team,
        not to individual users.

        Use this tool to:
        - Discover what Shared Drives you have access to
        - Get the Shared Drive ID to use with list_folder() or search_files()

        Returns:
            Dictionary with:
            - shared_drives: List of shared drives with id and name
            - count: Number of shared drives found

        Example:
            list_shared_drives()  # No parameters needed
        """
        try:
            drives = drive_service.list_shared_drives()

            formatted_drives = []
            for drive in drives:
                formatted_drives.append({
                    'id': drive['id'],
                    'name': drive['name']
                })

            return {
                'success': True,
                'count': len(formatted_drives),
                'shared_drives': formatted_drives
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to list shared drives: {e}"
            }

    # Return all tools
    return [search_files, list_folder, get_file_content, list_shared_drives]
