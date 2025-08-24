from pydantic import BaseModel
from uuid import UUID

class SearchFilterDto(BaseModel):
    search_filter_id: UUID
    name: str
    filter_value: str
    search_id: UUID

    class Config:
        from_attributes = True