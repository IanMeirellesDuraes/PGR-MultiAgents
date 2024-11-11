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
from typing import Any, Optional, Type
import unicodedata
import re


class SimplePDFSearchToolSchema(BaseModel):
    """Schema para a entrada de SimplePDFSearchTool2."""
    query: str = Field(
        ..., description="A consulta obrigatória que você quer usar para pesquisar o conteúdo do PDF"
    )

class SimplePDFSearchTool2(BaseTool):
    name: str = "Simple PDF Search Tool"
    description: str = "Busca por termos específicos em um documento PDF e extrai o texto que contém esses termos."
    pdf_path: str = Field(..., description="O caminho para o arquivo PDF que será pesquisado")  
    args_schema: Type[BaseModel] = SimplePDFSearchToolSchema

    def _normalize_text(self, text: str) -> str:
        numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65"]
        text = unicodedata.normalize("NFD", text)
        text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
        text = re.sub(r"[–—―]", "-", text)  
        for numero in numeros:
            if int(numero) < 10:
                text = text.replace(f"GHE 0{numero}-", f"GHE 0{numero} -")
            else:
                text = text.replace(f"GHE {numero}-", f"GHE {numero} -")
        return text

    def _run(self, query: str, **kwargs: Any) -> str:
        results = []
        query = self._normalize_text(query)
        try:
            print(f"Searching for '{query}' in '{self.pdf_path}'...")
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_number, page in enumerate(reader.pages):
                    text = page.extract_text()
                    normalized_text = self._normalize_text(text)
                    if query in normalized_text:
                        results.append(f"Página {page_number + 1}: {normalized_text}")
            return "\n\n".join(results) if results else "Nenhuma correspondência encontrada."
        except Exception as e:
            return f"Erro ao processar o PDF: {str(e)}"
        
#tool = SimplePDFSearchTool2(pdf_path="C:\\ian\\Trabalho\\PGR-MultiAgents\\pgranalystflow\\path\\pgr-brmed1.pdf")
#print(tool.run(query="GHE 05 - RECONHECIMENTO DOS RISCOS OCUPACIONAIS"))

