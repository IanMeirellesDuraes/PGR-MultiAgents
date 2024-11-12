#!/usr/bin/env python
import os
import json
from reportlab.lib.pagesizes import A4
from typing import Callable, Optional, Awaitable
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from crewai import Flow
from crewai.flow.flow import listen, start, and_, router
from crews.gheanalystcrew.gheanalystcrew_crew import GheAnalystCrew
from crews.agentmodelcrew.agentmodelcrew_crew import AgentmodelcrewCrew
from crews.gheextractcrew.gheextractcrew_crew import GheextractcrewCrew
from crews.jsonorganizercrew.jsonorganizercrew_crew import JsonorganizercrewCrew
from tools.custom_tool import SimplePDFSearchTool2

class PgrAnalystFlow(Flow):
    def __init__(
        self,
        pdf_path: str,
        key: str,
        on_success: Callable[[dict], Awaitable[None]],
    ):
        super().__init__()
        self.pdf_path = pdf_path
        self.key = key
        self.on_success = on_success

    @start()
    def ResetFlow(self):

        if not os.path.exists(f"tmp/{self.key}"):
            os.makedirs(f"tmp/{self.key}")

        paths = [f"tmp/{self.key}/results.txt"]
        if os.path.exists(paths[0]):
            os.remove(paths[0])
        print("Arquivos antigos removidos...")

    @listen(ResetFlow)
    def LoadPdf(self):
        tool = SimplePDFSearchTool2(pdf_path=self.pdf_path)
        self.pdf_ghe = tool._run(query="DESCRICAO DE ATIVIDADE")
        self.pdf_risks = tool._run(query="RECONHECIMENTO DOS RISCOS OCUPACIONAIS")

    @listen(LoadPdf)
    def CreatePDFRisk(self):
        c = canvas.Canvas(f"tmp/{self.key}/risks.pdf", pagesize=A4)
        largura, altura = A4
        margem_y = altura - 50
        margem_x = 50
        margem_inferior = 50
        largura_max = largura - 2 * margem_x
        c.setFont("Helvetica", 10)
        linhas = self.pdf_risks.split("\n")
        primeira_pagina = True
        for linha in linhas:
            if linha.startswith("Página"):
                if not primeira_pagina:  
                    c.showPage()
                    c.setFont("Helvetica", 10)
                primeira_pagina = False  
                margem_y = altura - 50 
            while stringWidth(linha, "Helvetica", 10) > largura_max:
                for i in range(len(linha), 0, -1):
                    if stringWidth(linha[:i], "Helvetica", 10) <= largura_max:
                        if margem_y < margem_inferior:
                            c.showPage()
                            c.setFont("Helvetica", 10)
                            margem_y = altura - 50
                        c.drawString(margem_x, margem_y, linha[:i].strip())
                        linha = linha[i:].strip()
                        margem_y -= 15
                        break
            if margem_y < margem_inferior:
                c.showPage()
                c.setFont("Helvetica", 10)
                margem_y = altura - 50
            c.drawString(margem_x, margem_y, linha)
            margem_y -= 15
        c.save()
        print("PDF de riscos criado com sucesso!")

    @listen(LoadPdf)
    def CreatePDFGhes(self):
        c = canvas.Canvas(f"tmp/{self.key}/ghes.pdf", pagesize=A4)
        largura, altura = A4
        margem_y = altura - 50
        margem_x = 50
        margem_inferior = 50
        largura_max = largura - 2 * margem_x
        c.setFont("Helvetica", 10)
        linhas = self.pdf_ghe.split("\n")
        primeira_pagina = True
        for linha in linhas:
            if linha.startswith("Página"):
                if not primeira_pagina:  
                    c.showPage()
                    c.setFont("Helvetica", 10)
                primeira_pagina = False  
                margem_y = altura - 50 
            while stringWidth(linha, "Helvetica", 10) > largura_max:
                for i in range(len(linha), 0, -1):
                    if stringWidth(linha[:i], "Helvetica", 10) <= largura_max:
                        if margem_y < margem_inferior:
                            c.showPage()
                            c.setFont("Helvetica", 10)
                            margem_y = altura - 50
                        c.drawString(margem_x, margem_y, linha[:i].strip())
                        linha = linha[i:].strip()
                        margem_y -= 15
                        break
            if margem_y < margem_inferior:
                c.showPage()
                c.setFont("Helvetica", 10)
                margem_y = altura - 50
            c.drawString(margem_x, margem_y, linha)
            margem_y -= 15
        c.save()
        print("PDF de ghes criado com sucesso!")

    @listen(and_(CreatePDFRisk, CreatePDFGhes))
    def CrewTrigger(self):
        return "Crew triggered!"

    @router(CrewTrigger)
    def GheDetector(self):
        gheanalystcrew = GheAnalystCrew(pdf_path=self.pdf_path)
        ghes = gheanalystcrew.crew().kickoff(inputs={"query": "DESCRICAO DE ATIVIDADE"})
        self.ghes = ghes
        if ghes["ghes"] != []:
            return "Ghes detected!"
        else:
            return "No Ghes detected!"

    @listen("Ghes detected!")
    async def ExtractGhes(self):
        results = []
        self.jsonlist = []
        for ghe in self.ghes["ghes"]:
            ghe_extract = (
                await GheextractcrewCrew(pdf_path=f"tmp/{self.key}/ghes.pdf")
                .crew()
                .kickoff_async(inputs={"query": f"{ghe}", "ghe": f"{ghe}"})
            )
            pgr_agent_result = (
                await AgentmodelcrewCrew(pdf_path=f"tmp/{self.key}/risks.pdf")
                .crew()
                .kickoff_async(inputs={"ghe": f"{ghe}", "query": f"{ghe}"})
            )
            json_organizer = (
                await JsonorganizercrewCrew()
                .crew()
                .kickoff_async(
                    inputs={
                        "ghe": f"{ghe_extract.raw}",
                        "agent": f"{pgr_agent_result.raw}",
                    }
                )
            )
            results.append(json.loads(json_organizer.raw))
            with open(f"tmp/{self.key}/results.txt", "a", encoding="utf-8") as md:
                md.write(f"{ghe_extract.raw}\n\n")
                md.write(f"{pgr_agent_result.raw}\n\n")
        self.pgr_result = results

    @listen("No Ghes detected!")
    async def NoGhes(self):
        await self.on_success({"data": []})

    @listen(ExtractGhes)
    async def JSONConverter(self):
        resultado = {"data": self.pgr_result}
        await self.on_success(resultado)


def kickoff():
    flow = PgrAnalystFlow(pdf_path="tmp/pgr-brmed2.pdf", key="pgr-brmed2", on_success=lambda x: print(x))
    flow.kickoff()


def plot():
    flow = PgrAnalystFlow()
    flow.plot()


if __name__ == "__main__":
    kickoff()
