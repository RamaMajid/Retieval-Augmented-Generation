"""
Search History Manager for storing and retrieving search history.
"""
import json
import uuid
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel


class SearchHistoryEntry(BaseModel):
    """Model for a single search history entry."""
    id: str
    timestamp: str
    query: str
    query_type: str  # "text" or "image"
    results: List[Dict]
    narrative: Optional[str] = None
    is_favorite: bool = False
    num_results: int


class HistoryManager:
    """
    Manager for search history with JSON file storage.
    """
    
    def __init__(self, history_file: str = "data/search_history.json"):
        """
        Initialize history manager.
        
        Args:
            history_file: Path to JSON file for storing history
        """
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize file if it doesn't exist
        if not self.history_file.exists():
            self._save_data({"searches": []})
    
    def _load_data(self) -> Dict:
        """Load history data from JSON file."""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
            return {"searches": []}
    
    def _save_data(self, data: Dict):
        """Save history data to JSON file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def save_search(
        self,
        query: str,
        query_type: str,
        results: List[Dict],
        narrative: Optional[str] = None
    ) -> str:
        """
        Save a search to history.
        
        Args:
            query: Search query text
            query_type: "text" or "image"
            results: List of search results
            narrative: Optional generated narrative
            
        Returns:
            ID of saved search
        """
        data = self._load_data()
        
        # Create new entry
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "query": query,
            "query_type": query_type,
            "results": results,
            "narrative": narrative,
            "is_favorite": False,
            "num_results": len(results)
        }
        
        # Add to beginning of list (most recent first)
        data["searches"].insert(0, entry)
        
        # Optional: Limit history size (keep last 1000)
        if len(data["searches"]) > 1000:
            data["searches"] = data["searches"][:1000]
        
        self._save_data(data)
        return entry["id"]
    
    def get_all(
        self,
        limit: Optional[int] = None,
        offset: int = 0,
        favorites_only: bool = False
    ) -> List[Dict]:
        """
        Get all search history entries.
        
        Args:
            limit: Maximum number of entries to return
            offset: Number of entries to skip
            favorites_only: Only return favorited searches
            
        Returns:
            List of search history entries
        """
        data = self._load_data()
        searches = data["searches"]
        
        # Filter favorites if requested
        if favorites_only:
            searches = [s for s in searches if s.get("is_favorite", False)]
        
        # Apply pagination
        if limit:
            searches = searches[offset:offset + limit]
        else:
            searches = searches[offset:]
        
        return searches
    
    def get_by_id(self, search_id: str) -> Optional[Dict]:
        """
        Get a specific search by ID.
        
        Args:
            search_id: ID of the search
            
        Returns:
            Search entry or None if not found
        """
        data = self._load_data()
        for search in data["searches"]:
            if search["id"] == search_id:
                return search
        return None
    
    def delete(self, search_id: str) -> bool:
        """
        Delete a search from history.
        
        Args:
            search_id: ID of the search to delete
            
        Returns:
            True if deleted, False if not found
        """
        data = self._load_data()
        original_length = len(data["searches"])
        
        data["searches"] = [
            s for s in data["searches"] if s["id"] != search_id
        ]
        
        if len(data["searches"]) < original_length:
            self._save_data(data)
            return True
        return False
    
    def clear_all(self) -> int:
        """
        Clear all search history.
        
        Returns:
            Number of entries deleted
        """
        data = self._load_data()
        count = len(data["searches"])
        
        data["searches"] = []
        self._save_data(data)
        
        return count
    
    def toggle_favorite(self, search_id: str) -> Optional[bool]:
        """
        Toggle favorite status of a search.
        
        Args:
            search_id: ID of the search
            
        Returns:
            New favorite status, or None if not found
        """
        data = self._load_data()
        
        for search in data["searches"]:
            if search["id"] == search_id:
                search["is_favorite"] = not search.get("is_favorite", False)
                self._save_data(data)
                return search["is_favorite"]
        
        return None
    
    def export_all(self) -> Dict:
        """
        Export all history data.
        
        Returns:
            Complete history data
        """
        return self._load_data()
    
    def get_stats(self) -> Dict:
        """
        Get statistics about search history.
        
        Returns:
            Dictionary with stats
        """
        data = self._load_data()
        searches = data["searches"]
        
        return {
            "total_searches": len(searches),
            "favorites": len([s for s in searches if s.get("is_favorite", False)]),
            "text_searches": len([s for s in searches if s["query_type"] == "text"]),
            "image_searches": len([s for s in searches if s["query_type"] == "image"]),
            "oldest_search": searches[-1]["timestamp"] if searches else None,
            "newest_search": searches[0]["timestamp"] if searches else None
        }
