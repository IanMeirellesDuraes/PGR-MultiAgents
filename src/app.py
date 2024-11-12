from src.config import AppConfig

AppConfig.load_env()
from fastapi import FastAPI
from src.pgranalystflow.main import PgrAnalystFlow
import requests
import os
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
import tempfile
from .dynadok import DynadokService
import json

app = FastAPI()


def download_file(url, filename):
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Could not download file from URL")
    tmp_filename = os.path.join(tempfile.gettempdir(), filename)
    with open(tmp_filename, "wb") as file:
        file.write(response.content)
    return tmp_filename


@app.post("/pgranalyst/")
async def pgr_analyst(
    document_id: str = Form(...),
    file: UploadFile = File(None),
    file_url: str = Form(default=""),
):
    if not file and not file_url:
        raise HTTPException(
            status_code=400, detail="Either file or file_url must be provided"
        )

    temp_dir = tempfile.TemporaryDirectory()
    file_path = ""

    if file:
        file_path = os.path.join(temp_dir.name, f"{document_id}.pdf")
        with open(file_path, "wb") as f:
            f.write(file.file.read())
    elif file_url:
        file_path = download_file(file_url, f"{document_id}.pdf")

    print(f"PDF salvo em {file_path}")

    async def on_success(content):
        # delete file
        os.remove(file_path)
        dynadokService = DynadokService()
        value = json.dumps(content["data"], ensure_ascii=False, indent=2)
        update = await dynadokService.update_computed_fields(
            document_id,
            {
                "computedFields": [
                    {
                        "label": "DYNADOK_GHES",
                        "value": value,
                        "type": "TEXT_AREA",
                    }
                ]
            },
        )
        print(update)

    flow = PgrAnalystFlow(file_path, document_id, on_success)
    results = await flow.kickoff_async()
    return results
