from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    sub_title: str
    content: str
    author: str
    tags : list

