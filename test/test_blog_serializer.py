# tests/test_blog_serializer.py (or at the root)

from bson.objectid import ObjectId
from serializers.blog import decodeBlog, decodeAllBlogs # Import the functions to test

# --- Test for decodeBlog ---

def test_decode_blog_valid_document():
    # Simulate a MongoDB document
    mock_mongo_doc = {
        "_id": ObjectId("60c72b2f9b1e8a0f7c8b4567"), # A valid ObjectId
        "title": "My First Blog",
        "sub_title": "An introduction",
        "content": "This is the content of my first blog post.",
        "author": "John Doe",
        "tags": ["python", "fastapi"],
        "date": "2023-01-01 10:00:00"
    }
    
    # Expected output after decoding
    expected_output = {
        "id": "60c72b2f9b1e8a0f7c8b4567", # Note: ObjectId is converted to string
        "title": "My First Blog",
        "sub_title": "An introduction",
        "content": "This is the content of my first blog post.",
        "author": "John Doe",
        "tags": ["python", "fastapi"],
        "date": "2023-01-01 10:00:00"
    }
    
    # Call the function and assert the output
    actual_output = decodeBlog(mock_mongo_doc)
    
    # Assert that the actual output matches the expected output
    assert actual_output == expected_output

# tests/test_blog_serializer.py (continued)

def test_decode_blog_none_input():
    # When None is passed, it should return None
    assert decodeBlog(None) is None

# tests/test_blog_serializer.py (continued)

def test_decode_all_blogs_empty_list():
    # When an empty list is passed, it should return an empty list
    assert decodeAllBlogs([]) == []

# tests/test_blog_serializer.py (continued)

def test_decode_all_blogs_with_documents():
    mock_mongo_doc1 = {
        "_id": ObjectId("60c72b2f9b1e8a0f7c8b4567"),
        "title": "Blog One", "sub_title": "Sub One", "content": "Content One", "author": "Author A", "tags": ["a"], "date": "..."
    }
    mock_mongo_doc2 = {
        "_id": ObjectId("60c72b2f9b1e8a0f7c8b4568"),
        "title": "Blog Two", "sub_title": "Sub Two", "content": "Content Two", "author": "Author B", "tags": ["b"], "date": "..."
    }
    
    expected_output = [
        {"id": "60c72b2f9b1e8a0f7c8b4567", "title": "Blog One", "sub_title": "Sub One", "content": "Content One", "author": "Author A", "tags": ["a"], "date": "..."},
        {"id": "60c72b2f9b1e8a0f7c8b4568", "title": "Blog Two", "sub_title": "Sub Two", "content": "Content Two", "author": "Author B", "tags": ["b"], "date": "..."}
    ]
    
    actual_output = decodeAllBlogs([mock_mongo_doc1, mock_mongo_doc2])
    assert actual_output == expected_output
