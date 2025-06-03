# FastAPI app entrypoint
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from backend.main import langgraph

app = FastAPI()

@app.get('/')
def root():
    return {"message": "Hello from GenAI backend!"}

@app.post('/execute')
async def execute(request: Request):
    data = await request.json()
    user_input = data.get("input")
    if not user_input:
        return JSONResponse({"error": "Missing 'input' in request body"}, status_code=400)
    try:
        result = langgraph(user_input)
        return {"result": result}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)