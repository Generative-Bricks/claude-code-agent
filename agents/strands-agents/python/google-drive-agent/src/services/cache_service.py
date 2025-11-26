"""
Caching Service for File Content.

Caches extracted file content based on file ID and modification time.
Avoids re-downloading and re-processing unchanged files.

Following PERSEVERE principle: Resilient system that handles failures gracefully.
"""

import hashlib
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class CacheService:
    """Manages caching of extracted file content."""

    def __init__(self, cache_dir: str = "data/cache"):
        """
        Initialize cache service.

        Args:
            cache_dir: Directory for storing cached content
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.cache_dir / "cache_metadata.json"

        # Load existing metadata
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict[str, Any]:
        """Load cache metadata from disk."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Failed to load cache metadata: {e}")
                return {}
        return {}

    def _save_metadata(self) -> None:
        """Save cache metadata to disk."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to save cache metadata: {e}")

    def _get_cache_key(self, file_id: str, modified_time: str) -> str:
        """
        Generate cache key based on file ID and modification time.

        Args:
            file_id: Google Drive file ID
            modified_time: File modification timestamp

        Returns:
            Cache key (hash)
        """
        key_string = f"{file_id}_{modified_time}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(
        self,
        file_id: str,
        modified_time: str,
        file_name: str = "unknown"
    ) -> Optional[str]:
        """
        Get cached content if available and not stale.

        Args:
            file_id: Google Drive file ID
            modified_time: Current file modification time
            file_name: File name (for logging)

        Returns:
            Cached content if valid, None otherwise
        """
        cache_key = self._get_cache_key(file_id, modified_time)
        cache_file = self.cache_dir / f"{cache_key}.txt"

        # Check if cache file exists
        if not cache_file.exists():
            print(f"💾 Cache miss: {file_name}")
            return None

        # Verify cache metadata
        if cache_key not in self.metadata:
            print(f"⚠️  Cache metadata missing for: {file_name}")
            return None

        metadata = self.metadata[cache_key]

        # Check if modification time matches
        if metadata.get('modified_time') != modified_time:
            print(f"⚠️  Cache stale (file modified): {file_name}")
            return None

        # Load cached content
        try:
            content = cache_file.read_text(encoding='utf-8')
            print(f"✅ Cache hit: {file_name} ({len(content)} chars)")
            return content
        except Exception as e:
            print(f"❌ Failed to read cache: {e}")
            return None

    def set(
        self,
        file_id: str,
        modified_time: str,
        content: str,
        file_name: str = "unknown",
        mime_type: str = "unknown"
    ) -> None:
        """
        Store content in cache.

        Args:
            file_id: Google Drive file ID
            modified_time: File modification time
            content: Extracted content to cache
            file_name: File name (for metadata)
            mime_type: MIME type (for metadata)
        """
        cache_key = self._get_cache_key(file_id, modified_time)
        cache_file = self.cache_dir / f"{cache_key}.txt"

        try:
            # Write content to cache file
            cache_file.write_text(content, encoding='utf-8')

            # Update metadata
            self.metadata[cache_key] = {
                'file_id': file_id,
                'file_name': file_name,
                'mime_type': mime_type,
                'modified_time': modified_time,
                'cached_at': datetime.now().isoformat(),
                'content_length': len(content)
            }

            self._save_metadata()
            print(f"💾 Cached: {file_name} ({len(content)} chars)")

        except Exception as e:
            print(f"❌ Failed to cache content: {e}")

    def clear(self) -> None:
        """Clear all cached content."""
        try:
            # Delete all cache files
            for cache_file in self.cache_dir.glob("*.txt"):
                cache_file.unlink()

            # Clear metadata
            self.metadata = {}
            self._save_metadata()

            print("✅ Cache cleared successfully")

        except Exception as e:
            print(f"❌ Failed to clear cache: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats (file count, total size, etc.)
        """
        file_count = len(list(self.cache_dir.glob("*.txt")))
        total_size = sum(
            f.stat().st_size
            for f in self.cache_dir.glob("*.txt")
        )

        return {
            'file_count': file_count,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / 1024 / 1024, 2),
            'cache_dir': str(self.cache_dir)
        }
