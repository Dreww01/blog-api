from fastapi import APIRouter


entry_root = APIRouter()

#endpoint
@entry_root.get("/")
async def apiRunnng():
    res = {
        "status": "ok",
        "message": "The api is running and IF YOURE SEEING THIS YOURE ALIVE"
    }
    return res

    