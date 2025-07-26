from fastapi import APIRouter
from models.blog import Blog
from config.config import blogs_collection
from datetime import datetime
from serializers.blog import decodeAllBlogs, decodeBlog
from bson.objectid import ObjectId

blog_root = APIRouter()

#post request
@blog_root.post("/new/blog")
async def newBlog(doc:Blog):
    try:
        doc = dict(doc)
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        doc["date"] = str(current_date)
        
        # this means we are inerting a single document into the collection --.insert_one
        res = blogs_collection.insert_one(doc)

        # this returns the id of the inserted document
        doc_id = str(res.inserted_id) 
        
        return {
            "status": "ok",
            "message": "Blog created successfully",
            "blog_id": doc_id,
            "created_at": current_date
        }

    # This block catches errors from insert_one, dict(doc), datetime, etc.
    except Exception as e:

        print(f"Error creating blog: {e}")
        return {
            "status": "error",
            "message": "Something went wrong, failed to create the blog"
        }, 500

# get blogs
@blog_root.get("/all/blogs")
async def getBlogs():
    try:
        res = blogs_collection.find()

        # Error handling-- to check if no blog found
        if not res:
            return {
                "status": "error",
                "message": "No blog found"
            }, 404

        # return the blog data
        decoded_data = decodeAllBlogs(res)
        return {
            "status": "ok",
            "data": decoded_data
        }, 200

    #except block to check if any other thing when wrong.
    except Exception as e:
        return {
            "status": "error",
            "message": "Something went wrong, failed to find the blog"
        }, 500


# GET BLOG ID
@blog_root.get("/blog/{_id}")
async def getBlogId(_id:str):

    #check if the id is valid
    if not ObjectId.is_valid(_id):
        return {
            "status": "error",
            "message": "Invalid blog id"
        }, 400
    
    try:
    #Try to find the blog
        res = blogs_collection.find_one({"_id": ObjectId(_id)})
    
        # Error handling-- if blog not found
        if not res:
            return {
                "status": "error",
                "message": "Blog not found"
            }, 404
    
        # return the blog data
        decoded_data = decodeBlog(res)
        return {
            "status": "ok",
            "data": decoded_data
        }, 200

    #except block to check if any other thing when wrong. 
    except Exception as e:
        return {
            "status": "error",
            "message": "Something went wrong, failed to find the blog"
        }, 500

@blog_root.put("/blog/update/{_id}")
async def updateBlog(_id: str, doc: Blog):
   
    #check if the id is valid
    if not ObjectId.is_valid(_id):
        return {
            "status": "error",
            "message": "Invalid blog id, please provide a valid id"
        }, 400

    try:
        # Convert Pydantic model to dictionary
        update_data = dict(doc.model_dump()) # Use model_dump() for Pydantic v2+

        # Update the blog
        res = blogs_collection.update_one({"_id": ObjectId(_id)}, {"$set": update_data})

        # Error handling-- if the blog in question is not found
        if res.matched_count == 0:
            return {
                "status": "error",
                "message": "Blog not found"
            }, 404


        # Document was found, but no changes were made (e.g., sent the same data)
        # This is often considered a successful operation, but you might want to inform the user.
        elif res.modified_count == 0:
            return {
                "status": "ok",
                "message": "Blog found, but no changes were needed"
            }, 200

        # return the blog data
        return {
            "status": "ok",
            "message": "Blog updated successfully"
        }, 200

    #except block to check if any other thing when wrong. 
    except Exception as e:
        return {
            "status": "error",
            "message": "Something went wrong, failed to update the blog"
        }, 500

    
@blog_root.delete("/blog/{_id}")
async def deleteBlog(_id: str):

    # Validate the blog ID format
    if not ObjectId.is_valid(_id):
        return {
            "status": "error", 
            "message": "Invalid blog ID format"
        }, 400

    try:
        # Attempt to delete the blog by its ID
        res = blogs_collection.delete_one({"_id": ObjectId(_id)})

        # Check if a document was actually deleted
        if res.deleted_count == 0:
            # If deleted_count is 0, it means no blog matched the ID
            return {"status": "error", "message": "Blog not found"}, 404
        else:
            # If deleted_count is 1, the blog was successfully deleted
            return {"status": "ok", "message": "Blog deleted successfully"}, 200

    except Exception as e:
        # Catch any unexpected errors during the database operation
        print(f"Error deleting blog {_id}: {e}") # Log the error for debugging

        return {
            "status": "error", 
            "message": "Something went wrong, failed to delete the blog"  
        }, 500

