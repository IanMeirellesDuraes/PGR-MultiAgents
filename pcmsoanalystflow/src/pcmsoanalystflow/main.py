#!/usr/bin/env python
from pydantic import BaseModel
import re
import pdfplumber

from crewai.flow.flow import Flow, listen, start

from crews.agentmodelcrew.agentmodelcrew_crew import AgentmodelcrewCrew
from crews.examextractcrew.examextractcrew_crew import ExamextractcrewCrew
from crews.gheextractcrew.gheextractcrew_crew import GheextractcrewCrew
from tools.custom_tool import SimplePDFSearchTool2

class PcmsoAnalyst(Flow):

    @start()
    def LoadPDF(self):
        texto = ""
        with pdfplumber.open("path/pcmso-brmed2.pdf") as pdf:
            for pagina in pdf.pages:
                texto += pagina.extract_text() 
        self.pdf_text = texto
        
    @listen(LoadPDF)
    def FilterGhes(self):
        padrao = r'(GHE \d+)'
        matches = list(re.finditer(padrao, self.pdf_text))
        resultado = {}
    
        for i in range(len(matches)):
            inicio = matches[i].start()
            ghe_atual = matches[i].group(1) 
            if i + 1 < len(matches):
                fim = matches[i + 1].start()
            else:
                fim = len(self.pdf_text)  
            resultado[ghe_atual] = self.pdf_text[inicio:fim]
        seções = resultado

        for ghe, texto in seções.items():
            with open(f"output/seção_{ghe}.txt", "w", encoding='utf-8') as arquivo:
                arquivo.write(f"Seção {ghe}:\n{texto}\n")

    @listen(FilterGhes)
    def ExtractGhes(self):
        gheextractcrew = GheextractcrewCrew()
        



def kickoff():
    flow = PcmsoAnalyst()
    flow.kickoff()


def plot():
    flow = PcmsoAnalyst()
    flow.plot()


if __name__ == "__main__":
    kickoff()
