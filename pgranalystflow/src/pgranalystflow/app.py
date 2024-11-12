from fastapi import FastAPI
from pydantic import BaseModel
from pgranalystflow.main import PgrAnalystFlow
import requests
import os

app = FastAPI()

class Inputs(BaseModel):
    pdf_url: str

@app.post("/pgranalyst/")
async def pgr_analyst(req: Inputs):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
    }
    resposta = requests.get(req.pdf_url, headers=headers, stream=True)
    output_dir = ".\\output"
    file_path = os.path.join(output_dir, os.path.basename(req.pdf_url))
    print(file_path)
    with open(file_path, 'wb') as f:
        f.write(resposta.content)
        print(f"PDF salvo em {file_path}")

    flow = PgrAnalystFlow(pdf_url=file_path)
    results = await flow.kickoff_async() 
    return results
    

if __name__ == "__main__":
    import uvicorn
    print(">>>>>> version 0.0.1")
    uvicorn.run(app, host="0.0.0.0", port=8000)