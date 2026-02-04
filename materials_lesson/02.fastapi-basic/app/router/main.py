from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.utils.serializer import ProductResponse, CreateProductResponse

app = FastAPI(
    docs_url= None,
    redoc_url= None
)

@app.get("/products", tags=["products"])
def list_products():
    return {"products": [] }

@app.get("/products/{id}", tags=["products"], response_model = ProductResponse)
def get_product(id:int):
    return ProductResponse(id=id, name=f"product {id}", price= 100.0 * id, description= f"description {id}" )

@app.post("/products",tags=["products"] )
def create_product(body: CreateProductResponse):
    new_id = 1
    return {"product": {"id": new_id, "name": body.name, "price": body.price , "description": body.description}}

@app.patch("/products/{id}", tags=["products"])
def update_product():
    return {"product": []}

@app.delete("/products/{id}", tags=["products"])
def delete_product():
    return {"product": None}


@app.get("/scalar")
def scalar_doc():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url, 
        title="My API Docs"
    )
