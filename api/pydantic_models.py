from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

# Enum for supported model names used in the application.
class ModelName(str, Enum):
    LLAMA_70B = "llama-3.3-70b-versatile"
    LLAMA_8B = "llama-3.1-8b-instant"


# Pydantic model for validating user query input with session ID and selected model. 
class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.LLAMA_70B)


# Pydantic model for structuring the response containing the answer, session ID, and model used.
class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName


# Pydantic model for representing metadata of a stored document including ID, filename, and upload timestamp.
class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime


# Pydantic model for validating a file deletion request by file ID.
class DeleteFileRequest(BaseModel):
    file_id: int