from fastapi import FastAPI

from app.routers import auth, categories, prices, products, stores

app = FastAPI(title="Bayong Grocery Price Comparison API")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(stores.router)
app.include_router(products.router)
app.include_router(prices.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
