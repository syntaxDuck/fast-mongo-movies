uvicorn api.main:app --reload &
uvicorn frontend.main:app --reload --port 8080 &