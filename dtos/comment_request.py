from pydantic import BaseModel

class CommentRequest(BaseModel):
    commentary: str