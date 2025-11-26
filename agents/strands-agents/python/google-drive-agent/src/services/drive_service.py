"""
Google Drive API Service Wrapper.

Provides simplified interface for Google Drive operations:
- Search files by query
- List folder contents
- Get file metadata
- Download file content

Following SIMPLICITY principle: Each method has one clear purpose.
"""

from typing import List, Optional, Dict, Any
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
import io


class DriveService:
    """Wrapper for Google Drive API operations."""

    def __init__(self, credentials: Credentials):
        """
        Initialize Drive service with OAuth credentials.

        Args:
            credentials: Valid Google OAuth2 credentials
        """
        self.service = build('drive', 'v3', credentials=credentials)
        print("✅ Google Drive service initialized")

    def search_files(
        self,
        query: str,
        folder_id: Optional[str] = None,
        file_types: Optional[List[str]] = None,
        limit: int = 20,
        name_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Search Google Drive for files matching query.

        Args:
            query: Search query string (searches name and/or content)
            folder_id: Optional folder ID to search within
            file_types: Optional list of MIME types to filter
            limit: Maximum number of results (default 20)
            name_only: If True, search only file names (not content)

        Returns:
            List of file dictionaries with id, name, mimeType, modifiedTime

        Example:
            files = drive.search_files("budget 2024", folder_id="abc123")
            files = drive.search_files("report", name_only=True)
        """
        # Build search query using Google Drive query syntax
        # Reference: https://developers.google.com/drive/api/guides/search-files
        if name_only:
            query_parts = [f"name contains '{query}'"]
        else:
            query_parts = [f"fullText contains '{query}'"]

        # Filter by folder if specified
        if folder_id:
            query_parts.append(f"'{folder_id}' in parents")

        # Filter by MIME types if specified
        if file_types:
            mime_filters = " or ".join([f"mimeType='{mt}'" for mt in file_types])
            query_parts.append(f"({mime_filters})")

        # Exclude trashed files
        query_parts.append("trashed=false")

        # Combine query parts with AND
        search_query = " and ".join(query_parts)

        try:
            # Execute search (includes Shared Drives)
            results = self.service.files().list(
                q=search_query,
                pageSize=limit,
                fields="files(id, name, mimeType, modifiedTime, size, webViewLink)",
                orderBy="modifiedTime desc",  # Most recent first
                supportsAllDrives=True,  # Enable Shared Drives support
                includeItemsFromAllDrives=True  # Include Shared Drive items in results
            ).execute()

            files = results.get('files', [])
            print(f"🔍 Found {len(files)} files matching '{query}'")
            return files

        except Exception as e:
            print(f"❌ Search failed: {e}")
            raise Exception(f"Failed to search files: {e}")

    def list_folder(
        self,
        folder_id: str,
        recursive: bool = False,
        include_files: bool = True,
        include_folders: bool = True
    ) -> List[Dict[str, Any]]:
        """
        List contents of a Google Drive folder.

        Args:
            folder_id: Google Drive folder ID
            recursive: If True, include subfolders (not implemented yet)
            include_files: Include files in results
            include_folders: Include folders in results

        Returns:
            List of file/folder dictionaries

        Example:
            contents = drive.list_folder("abc123xyz")
        """
        # Build query based on options
        query_parts = [f"'{folder_id}' in parents", "trashed=false"]

        # Filter by type
        mime_filters = []
        if include_folders:
            mime_filters.append("mimeType='application/vnd.google-apps.folder'")
        if include_files:
            mime_filters.append("mimeType!='application/vnd.google-apps.folder'")

        if mime_filters:
            query_parts.append(f"({' or '.join(mime_filters)})")

        query = " and ".join(query_parts)

        try:
            # Execute list request (includes Shared Drives)
            results = self.service.files().list(
                q=query,
                pageSize=100,  # Max page size
                fields="files(id, name, mimeType, modifiedTime, size, webViewLink)",
                orderBy="folder,name",  # Folders first, then alphabetical
                supportsAllDrives=True,  # Enable Shared Drives support
                includeItemsFromAllDrives=True  # Include Shared Drive items
            ).execute()

            items = results.get('files', [])
            print(f"📂 Found {len(items)} items in folder")
            return items

        except Exception as e:
            print(f"❌ List folder failed: {e}")
            raise Exception(f"Failed to list folder: {e}")

    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        """
        Get detailed metadata for a specific file.

        Args:
            file_id: Google Drive file ID

        Returns:
            File metadata dictionary

        Example:
            metadata = drive.get_file_metadata("abc123xyz")
        """
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields="id, name, mimeType, size, createdTime, modifiedTime, "
                       "owners, description, webViewLink, iconLink",
                supportsAllDrives=True  # Enable Shared Drives support
            ).execute()

            print(f"📄 Retrieved metadata for: {file.get('name')}")
            return file

        except Exception as e:
            print(f"❌ Get metadata failed: {e}")
            raise Exception(f"Failed to get file metadata: {e}")

    def list_shared_drives(self) -> List[Dict[str, Any]]:
        """
        List all Shared Drives (Team Drives) the user has access to.

        Returns:
            List of shared drive dictionaries with id, name

        Example:
            shared_drives = drive.list_shared_drives()
        """
        try:
            results = self.service.drives().list(
                pageSize=100,
                fields="drives(id, name)"
            ).execute()

            drives = results.get('drives', [])
            print(f"🗂️  Found {len(drives)} Shared Drives")
            return drives

        except Exception as e:
            print(f"❌ List shared drives failed: {e}")
            raise Exception(f"Failed to list shared drives: {e}")

    def download_file(self, file_id: str) -> bytes:
        """
        Download binary content of a file.

        Use this for: PDFs, Office files, images, etc.
        Do NOT use for Google Docs/Sheets (use export_google_doc instead).

        Args:
            file_id: Google Drive file ID

        Returns:
            File content as bytes

        Example:
            pdf_bytes = drive.download_file("abc123xyz")
        """
        try:
            request = self.service.files().get_media(fileId=file_id)

            # Download to memory buffer
            buffer = io.BytesIO()
            downloader = MediaIoBaseDownload(buffer, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    print(f"⬇️  Download progress: {int(status.progress() * 100)}%")

            print("✅ File downloaded successfully")
            return buffer.getvalue()

        except Exception as e:
            print(f"❌ Download failed: {e}")
            raise Exception(f"Failed to download file: {e}")

    def export_google_doc(
        self,
        file_id: str,
        mime_type: str = 'text/plain'
    ) -> str:
        """
        Export Google Workspace files (Docs, Sheets, Slides) to text.

        Args:
            file_id: Google Drive file ID
            mime_type: Export format (default: text/plain)
                - 'text/plain' for plain text
                - 'text/csv' for Sheets as CSV
                - 'application/pdf' for PDF export

        Returns:
            Exported content as string

        Example:
            text = drive.export_google_doc("abc123xyz", "text/plain")
        """
        try:
            # Export to specified format
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType=mime_type
            )

            # Download exported content
            buffer = io.BytesIO()
            downloader = MediaIoBaseDownload(buffer, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            content = buffer.getvalue().decode('utf-8')
            print(f"✅ Google Doc exported successfully ({len(content)} characters)")
            return content

        except Exception as e:
            print(f"❌ Export failed: {e}")
            raise Exception(f"Failed to export Google Doc: {e}")

    def get_folder_id_by_name(self, folder_name: str) -> Optional[str]:
        """
        Find folder ID by name (searches entire Drive).

        Args:
            folder_name: Folder name to search for

        Returns:
            Folder ID if found, None otherwise

        Example:
            folder_id = drive.get_folder_id_by_name("Research Papers")
        """
        query = (
            f"name='{folder_name}' and "
            "mimeType='application/vnd.google-apps.folder' and "
            "trashed=false"
        )

        try:
            results = self.service.files().list(
                q=query,
                pageSize=10,
                fields="files(id, name)"
            ).execute()

            files = results.get('files', [])

            if not files:
                print(f"❌ Folder '{folder_name}' not found")
                return None

            if len(files) > 1:
                print(f"⚠️  Multiple folders named '{folder_name}' found. Using first one.")

            folder_id = files[0]['id']
            print(f"✅ Found folder: {folder_name} (ID: {folder_id})")
            return folder_id

        except Exception as e:
            print(f"❌ Folder search failed: {e}")
            return None
