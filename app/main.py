from fastapi import FastAPI


app = FastAPI(title="Car Price Prediction API", version="1.0")

@app.on_event("startup")
def startup_event():
    load_artifacts()