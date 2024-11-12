#!/usr/bin/env python
from pydantic import BaseModel, Field, RootModel
import asyncio
import PyPDF2
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from fastapi import FastAPI

from crewai import Flow
from crewai.flow.flow import listen, start, and_, or_, router
from .crews.gheanalystcrew.gheanalystcrew_crew import GheAnalystCrew
from .crews.agentmodelcrew.agentmodelcrew_crew import AgentmodelcrewCrew
from .crews.gheextractcrew.gheextractcrew_crew import GheextractcrewCrew
from .crews.jsonorganizercrew.jsonorganizercrew_crew import JsonorganizercrewCrew
from src.pgranalystflow.tools.custom_tool import SimplePDFSearchTool2

class PgrAnalystFlow(Flow):
	
	def __init__(self, pdf_url: str):
		super().__init__()
		self.pdf_url = pdf_url
		

	@start()
	def ResetFlow(self):
		import os
		paths = ["output/results.txt"]
		if os.path.exists(paths[0]):
			os.remove(paths[0])
		print("Arquivos antigos removidos...")
	
	@listen(ResetFlow)
	def LoadPdf(self):
		tool = SimplePDFSearchTool2(pdf_path=self.pdf_url)
		self.pdf_ghe = tool._run(query="DESCRICAO DE ATIVIDADE")
		self.pdf_risks = tool._run(query="RECONHECIMENTO DOS RISCOS OCUPACIONAIS")
		print(self.pdf_url)
		print(self.pdf_url)
		print(self.pdf_url)
		
	@listen(LoadPdf)
	def CreatePDFRisk(self):
		c = canvas.Canvas("output/risks.pdf", pagesize=A4)
		largura, altura = A4
		margem_y = altura - 50 
		margem_x = 50
		margem_inferior = 50
		largura_max = largura - 2 * margem_x
		c.setFont("Helvetica", 10)
		linhas = self.pdf_risks.split('\n')
		for linha in linhas:
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
		print("PDF criado com sucesso!")
	
	@listen(LoadPdf)
	def CreatePDFGhes(self):
		c = canvas.Canvas("output/ghes.pdf", pagesize=A4)
		largura, altura = A4
		margem_y = altura - 50 
		margem_x = 50
		margem_inferior = 50
		largura_max = largura - 2 * margem_x
		c.setFont("Helvetica", 10)
		linhas = self.pdf_ghe.split('\n')
		for linha in linhas:
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
		print("PDF criado com sucesso!")
	
	@listen(and_(CreatePDFRisk, CreatePDFGhes))
	def CrewTrigger(self):
		return "Crew triggered!"

	@router(CrewTrigger)
	def GheDetector(self):
		gheanalystcrew = GheAnalystCrew(pdf_path=self.pdf_url)
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
			ghe_extract = await GheextractcrewCrew(pdf_path="output/ghes.pdf").crew().kickoff_async(inputs={"query": f"{ghe}", "ghe": f"{ghe}"})
			pgr_agent_result = await AgentmodelcrewCrew(pdf_path="output/risks.pdf").crew().kickoff_async(inputs={"ghe": f"{ghe}", "query": f"{ghe}"})
			json_organizer = await JsonorganizercrewCrew().crew().kickoff_async(inputs={"ghe": f"{ghe_extract.raw}", "agent": f"{pgr_agent_result.raw}"})
			results.append(f"{json_organizer}\n")
			with open("output/results.txt", 'a', encoding='utf-8') as md:	
				md.write(f"{ghe_extract.raw}\n\n")
				md.write(f"{pgr_agent_result.raw}\n\n")
		self.pgr_result = results

	@listen("No Ghes detected!")
	def NoGhes(self):
		return {
			"data": ["Este arquivo não possui GHEs."]
		}

	@listen(ExtractGhes)
	def JSONConverter(self):
		import secrets
		resultado = {"data": [self.pgr_result]}
		resultado_formatado = json.dumps(resultado, indent=4, ensure_ascii=False)
		#resultado_formatado = resultado_formatado.replace("\n", "").replace("\ ", "")
		random_id = secrets.token_hex(3)
		with open(f"output/resposta-{random_id}.json", 'w', encoding='utf-8') as md:	
			md.write(f"{resultado_formatado}")
		return print(resultado_formatado)
		
def kickoff():
    flow = PgrAnalystFlow()
    flow.kickoff()


def plot():
    flow = PgrAnalystFlow()
    flow.plot()


if __name__ == "__main__":
    kickoff()




	#@listen(LoadPdf)
	#def RiskDescription(self):
		#riskanalystcrew = RiskAnalystCrew()
		#risk_analysis = riskanalystcrew.crew().kickoff()
		#self.risk_analysis = risk_analysis
	
	#@listen(and_(GheDetector, RiskDescription))
	#def VisionReview(self):
		#visionanalystcrew = VisionAnalystCrew()
		#vision_analysis = visionanalystcrew.crew().kickoff(inputs={image_path_url: f"C:\Trabalho\PGR-MultiAgents\pgr_analyst\imgs\pgr\pagina_{self.ghes}.png"})
	
	#@listen(and_(GheDetector, RiskDescription))
	#def PgrDescription(self):
		#pgrorganizingcrew = PgrOrganizingCrew()
		#pgr_structure = pgrorganizingcrew.crew().kickoff()
		#print(pgr_structure)

	#@listen(PgrDescription)
	#def VisionReview(self):
		#visionanalystcrew = VisioncrewCrew()
		#vision_analysis = visionanalystcrew.crew().kickoff(inputs={"image_path_url": f"C:\Trabalho\PGR-MultiAgents\pgranalystflow\path\pagina_135.png"})





#@listen(GheDetector)
	#async def ExtractAgents(self):
		#results = []
		#self.jsonlist = []
		#for ghe in self.ghes["ghes"]:
			#pgr_agent_result = await (AgentmodelcrewCrew().crew().kickoff_async(inputs={"ghe": f"{ghe} - RECONHECIMENTO DOS RISCOS OCUPACIONAIS", "query": f"{ghe} - RECONHECIMENTO DOS RISCOS OCUPACIONAIS"}))
			#results.append(f"{pgr_agent_result.raw}\n")
			#with open("output/results.txt", 'a', encoding='utf-8') as md:	
				#md.write(f"{pgr_agent_result.raw}\n\n")
			
			
		#self.pgr_agent_results = results
	
	#@listen(and_(ExtractGhes, ExtractAgents))
	#def JsonOrganizer(self):
		#jsonorganizercrew = JsonorganizercrewCrew()
		#json_organizer = jsonorganizercrew.crew().kickoff()
		#with open("output/saida.json", 'a', encoding='utf-8') as md:	
			#md.write(f"{json_organizer}\n")