from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# importing static files
from fastapi.staticfiles import StaticFiles

# importing models
from models.user_model import User
from models.order_model import Order, OrderItem
from models.product_model import Product, ProductImage

# importing database
from database.connection import Base, engine, get_db

# importing routes
from routes.user_route import router as user_router
from routes.product_route import router as product_router
from routes.order_route import router as order_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Create all tables in the database
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def on_startup():
    get_db()


@app.on_event("shutdown")
def on_shutdown():
    get_db().close()


# origins:
# origins = ["http://localhost:3000", "http://localhost:8000"]

# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)


@app.get("/")
async def root():
    return {"message": "Hello Huda"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
