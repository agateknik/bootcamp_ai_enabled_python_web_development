from pydantic import BaseModel

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None
    
class CreateProductResponse(BaseModel):
    name: str
    price: float
    description: str | None = None
    
    