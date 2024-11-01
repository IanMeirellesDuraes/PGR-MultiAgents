import PyPDF2
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

class SimplePDFSearchTool(BaseTool):
    name: str = "Simple PDF Search Tool"
    description: str = "Search for specific terms in a PDF document and extract text containing those terms."
    pdf_path: str = Field(..., description="The path to the PDF file to search.")

    def _run(self, query: str) -> str:
        results = []
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_number, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if query.lower() in text.lower():
                        results.append(f"Page {page_number + 1}: {text}")
            return "\n\n".join(results) if results else "No matches found."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def run(self, query: str) -> str:
        return self._run(query)
    
