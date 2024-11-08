import PyPDF2
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

class SimplePDFSearchTool(BaseTool):
    name: str = "PDF tool Simples"
    description: str = "Ferramenta simples para pesquisar querys em arquivos PDF e extrair pedaços que correspondem."
    pdf_path: str = Field(..., description="Caminho do arquivo PDF a ser pesquisado.")
    query: str = Field(..., description="Query a ser pesquisada no arquivo PDF.")

    def _run(self):
        results = []
        try:
            print(f"Searching for '{self.query}' in '{self.pdf_path}'...")
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_number, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if self.query.lower() in text.lower():
                        results.append(f"Page {page_number + 1}: {text}")
            return "\n\n".join(results) if results else "No matches found."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    #def run(self, query: str) -> str:
        #return self.self._run(query)
    
#print(SimplePDFSearchTool(pdf_path="C:\ian\Trabalho\Analista-PGR\pgr_analyst\path\pgr2.pdf", query="ian").run())



from typing import Type, List
import openai

class ImageAnalysisTool(BaseTool):
    name: str = "Multi-Image Focused Analysis Tool"
    description: str = (
        "This tool analyzes multiple images using OpenAI's Vision API, focusing on a specific aspect or object. "
        "It takes in a list of image paths and a focus parameter to guide the analysis (e.g., 'detect objects', "
        "'analyze lighting conditions', 'identify people')."
    )

    def _run(self, image_paths: List[str], focus: str) -> str:
        results = []
        for img_path in image_paths:
            try:
                analysis = self._analyze_image(img_path, focus)
                results.append(analysis)
            except Exception as e:
                results.append(f"Error analyzing {img_path}: {str(e)}")
        return results

    def _analyze_image(self, image_path: str, focus: str) -> dict:
        with open(image_path, "rb") as image_file:
            response = openai.Vision.create(file=image_file, query=focus)
        return response.get("data", {})


