"""
OAuth2 Authentication Service for Google Drive API.

Handles:
- Initial OAuth flow (opens browser for user consent)
- Token caching (saves token.json for reuse)
- Token refresh (automatic refresh when expired)

Following TRUTH principle: All authentication steps are logged and observable.
"""

import os
import pickle
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Google Drive API scopes - read-only access
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]


class AuthService:
    """Manages Google Drive API authentication."""

    def __init__(self, credentials_dir: str = "credentials"):
        """
        Initialize authentication service.

        Args:
            credentials_dir: Directory containing credentials.json and token cache
        """
        self.credentials_dir = Path(credentials_dir)
        self.credentials_path = self.credentials_dir / "credentials.json"
        self.token_path = self.credentials_dir / "token.pickle"

        # Ensure credentials directory exists
        self.credentials_dir.mkdir(exist_ok=True)

    def get_credentials(self) -> Credentials:
        """
        Get valid user credentials from storage or run OAuth flow.

        Returns:
            Valid Google OAuth2 credentials

        Raises:
            FileNotFoundError: If credentials.json is missing
            Exception: If OAuth flow fails
        """
        creds: Optional[Credentials] = None

        # Step 1: Try to load existing token from cache
        if self.token_path.exists():
            print("📂 Loading cached credentials...")
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
            print("✅ Cached credentials loaded successfully")

        # Step 2: Refresh if expired, or run OAuth flow if no valid credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Token expired but can be refreshed
                print("🔄 Refreshing expired credentials...")
                try:
                    creds.refresh(Request())
                    print("✅ Credentials refreshed successfully")
                except Exception as e:
                    print(f"❌ Refresh failed: {e}")
                    print("🔐 Running OAuth flow to get new credentials...")
                    creds = self._run_oauth_flow()
            else:
                # No valid credentials - run OAuth flow
                print("🔐 No valid credentials found. Running OAuth flow...")
                creds = self._run_oauth_flow()

            # Step 3: Save credentials for next run
            print("💾 Saving credentials to cache...")
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
            print("✅ Credentials cached successfully")

        return creds

    def _run_oauth_flow(self) -> Credentials:
        """
        Run OAuth2 flow - opens browser for user consent.

        Returns:
            Fresh Google OAuth2 credentials

        Raises:
            FileNotFoundError: If credentials.json doesn't exist
            Exception: If OAuth flow fails
        """
        if not self.credentials_path.exists():
            raise FileNotFoundError(
                f"❌ OAuth credentials file not found: {self.credentials_path}\n\n"
                "📋 Setup Instructions:\n"
                "1. Go to https://console.cloud.google.com/\n"
                "2. Create a project or select existing one\n"
                "3. Enable Google Drive API\n"
                "4. Create OAuth 2.0 credentials (Desktop app)\n"
                "5. Download credentials.json\n"
                "6. Place it in: {self.credentials_dir}/"
            )

        try:
            # Run local server OAuth flow (opens browser automatically)
            flow = InstalledAppFlow.from_client_secrets_file(
                str(self.credentials_path),
                SCOPES
            )

            print("\n🌐 Opening browser for Google Drive authorization...")
            print("📝 Please log in and grant permissions\n")

            # Run local server on random available port
            creds = flow.run_local_server(port=0)

            print("✅ Authorization successful!")
            return creds

        except Exception as e:
            raise Exception(f"OAuth flow failed: {e}")

    def revoke_credentials(self) -> None:
        """
        Revoke current credentials and delete cached token.

        Use this to force re-authentication or when switching Google accounts.
        """
        if self.token_path.exists():
            print("🗑️  Revoking and deleting cached credentials...")
            self.token_path.unlink()
            print("✅ Credentials revoked successfully")
        else:
            print("ℹ️  No cached credentials to revoke")
