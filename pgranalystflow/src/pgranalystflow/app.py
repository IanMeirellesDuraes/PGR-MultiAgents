from fastapi import FastAPI
from pydantic import BaseModel
from pgranalystflow.main import PgrAnalystFlow

app = FastAPI()

class Inputs(BaseModel):
    pdf_url: str
    
@app.post("/pgranalyst/")
async def pgr_analyst(req: Inputs):
    flow = PgrAnalystFlow(req.pdf_url)
    flow.kickoff()
    return "Flow executed successfully!"

if __name__ == "__main__":
    import uvicorn
    print(">>>>>> version 0.0.1")
    uvicorn.run(app, host="0.0.0.0", port=8000)