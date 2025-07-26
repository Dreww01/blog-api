from fastapi import FastAPI
from routes.entry import entry_root
from routes.blog import blog_root

# initalize the fastapi app
app = FastAPI()

#include the router--entry root
app.include_router(entry_root)

# include the router--blog root
app.include_router(blog_root)