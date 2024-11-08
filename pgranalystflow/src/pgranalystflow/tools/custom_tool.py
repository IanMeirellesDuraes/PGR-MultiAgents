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


import PyPDF2
from crewai_tools import BaseTool
from pydantic import Field

class SimplePDFSearchTool2(BaseTool):
    name: str = "Simple PDF Search Tool"
    description: str = "Busca por termos específicos em um documento PDF e extrai o texto que contém esses termos."
    pdf_path: str = Field(..., description="O caminho para o arquivo PDF que será pesquisado")  

    def _run(self, query: str) -> str:
        results = []
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_number, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if query.lower() in text.lower():
                        results.append(f"Página {page_number + 1}: {text}")
            return "\n\n".join(results) if results else "Nenhuma correspondência encontrada."
        except Exception as e:
            return f"Erro ao processar o PDF: {str(e)}"

