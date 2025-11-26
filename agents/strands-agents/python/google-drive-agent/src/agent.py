"""
Google Drive RAG Agent - Main Agent Configuration.

Combines all services and tools into a Strands agent that can:
- Search and browse Google Drive
- Extract content from any file type
- Answer questions grounded in Drive content

Following EXCELLENCE principle: Production-ready from inception.
"""

from strands import Agent
from typing import Optional

# Import services
from services.auth_service import AuthService
from services.drive_service import DriveService
from services.content_extractor import ContentExtractor
from services.cache_service import CacheService

# Import tools
from tools.drive_tools import create_drive_tools

# Import configuration
from config.settings import settings


class GoogleDriveAgent:
    """Google Drive document grounding agent using Strands framework."""

    def __init__(
        self,
        model_id,  # Can be string or model object (e.g., GeminiModel)
        enable_cache: bool = True,
        credentials_dir: str = "credentials"
    ):
        """
        Initialize Google Drive agent with all required services.

        Args:
            model_id: Model ID string or model object (e.g., GeminiModel, BedrockModel)
            enable_cache: Enable content caching (default: True)
            credentials_dir: Directory containing OAuth credentials
        """
        print("🚀 Initializing Google Drive Agent...")

        # Step 1: Authenticate with Google Drive API
        print("\n📝 Step 1: Authenticating with Google Drive...")
        auth_service = AuthService(credentials_dir=credentials_dir)
        credentials = auth_service.get_credentials()

        # Step 2: Initialize Drive service
        print("\n📁 Step 2: Initializing Drive service...")
        self.drive_service = DriveService(credentials)

        # Step 3: Initialize content extractor
        print("\n📄 Step 3: Initializing content extractor...")
        self.content_extractor = ContentExtractor(self.drive_service)

        # Step 4: Initialize cache service (optional)
        self.cache_service = None
        if enable_cache:
            print("\n💾 Step 4: Initializing cache service...")
            self.cache_service = CacheService()
            stats = self.cache_service.get_stats()
            print(f"   Cache: {stats['file_count']} files, {stats['total_size_mb']} MB")

        # Step 5: Create tools
        print("\n🛠️  Step 5: Creating agent tools...")
        tools = create_drive_tools(
            drive_service=self.drive_service,
            content_extractor=self.content_extractor,
            cache_service=self.cache_service
        )
        print(f"   Created {len(tools)} tools: search_files, list_folder, get_file_content, list_shared_drives")

        # Step 6: Create Strands agent
        print("\n🤖 Step 6: Creating Strands agent...")
        self.agent = Agent(
            name="Google Drive Document Assistant",
            model=model_id,  # This accepts either a string or model object
            tools=tools,
            description="""You are a helpful assistant that helps users access and understand their Google Drive documents.

You have access to four tools:
1. **search_files** - Search Google Drive by query (searches file names and content)
2. **list_folder** - Browse contents of a specific folder (supports My Drive and Shared Drives)
3. **get_file_content** - Extract full text from any file (Docs, Sheets, PDFs, Word, Excel, etc.)
4. **list_shared_drives** - List all Shared Drives (Team Drives) the user has access to

## Your Capabilities:
- Search for files across Google Drive
- Browse folder structures
- Read and extract content from any supported file type
- Answer questions based on file content (content is in your context)
- Summarize documents or collections of files
- Compare information across multiple documents

## Important Notes:
- When you use get_file_content, the ENTIRE file content is provided to you
- You don't need to retrieve additional information - just analyze what's given
- For questions about specific files, search for them first, then get their content
- Be transparent about what you're doing (searching, reading files, etc.)

## Workflow Example:
1. User asks: "What does my Q4 budget say about marketing spend?"
2. You: Use search_files("Q4 budget") to find the file
3. You: Use get_file_content(file_id) to read the full document
4. You: Answer the question based on the content now in your context

Remember: You have the full content, so answer comprehensively and cite specific details from the documents.

**Biblical Principle - HONOR**: Respect user data sovereignty. Never access files unless explicitly requested. Be transparent about what files you're accessing."""
        )

        print("\n✅ Google Drive Agent initialized successfully!")
        # Print model info (handle both string and object)
        model_name = model_id if isinstance(model_id, str) else getattr(model_id, 'model_id', 'Custom Model')
        print(f"   Model: {model_name}")
        print(f"   Caching: {'Enabled' if enable_cache else 'Disabled'}")

    async def run(self, user_input: str) -> str:
        """
        Run agent with user input (async).

        Args:
            user_input: User's question or request

        Returns:
            Agent's response as string
        """
        response = await self.agent.invoke_async(user_input)
        return response

    def run_sync(self, user_input: str) -> str:
        """
        Run agent with user input (synchronous).

        Args:
            user_input: User's question or request

        Returns:
            Agent's response as string
        """
        response = self.agent.invoke(user_input)
        return response

    async def stream(self, user_input: str):
        """
        Stream agent responses (async).

        Args:
            user_input: User's question or request

        Yields:
            Stream events from agent
        """
        async for event in self.agent.stream_async(user_input):
            yield event

    def clear_cache(self) -> None:
        """Clear all cached file content."""
        if self.cache_service:
            self.cache_service.clear()
        else:
            print("⚠️  Caching is not enabled")

    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        if self.cache_service:
            return self.cache_service.get_stats()
        else:
            return {'error': 'Caching is not enabled'}
