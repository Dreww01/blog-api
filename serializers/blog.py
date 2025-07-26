# serializers/blog.py

from bson.objectid import ObjectId
from typing import Dict, Any, Optional # Import Optional for type hinting

# Function to serialize a single MongoDB document
def decodeBlog(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    # 1. Handle None input: If doc is None, return None immediately.
    if doc is None:
        return None
        
    # 2. Map MongoDB fields to API response fields
    # Ensure _id is converted to a string for the 'id' key
    return {
        "id": str(doc["_id"]), # This line was likely missing or incorrect in your original code
        "title": doc["title"],
        "sub_title": doc["sub_title"],
        "content": doc["content"],
        "author": doc["author"],
        "tags": doc["tags"],
        "date": doc.get("date") # Safely get date if it exists, otherwise None
    }

# Function to serialize a list of MongoDB documents
def decodeAllBlogs(docs: list) -> list:
    # This function uses decodeBlog for each document in the list
    # If decodeBlog correctly handles None, this should work fine.
    return [decodeBlog(doc) for doc in docs]

