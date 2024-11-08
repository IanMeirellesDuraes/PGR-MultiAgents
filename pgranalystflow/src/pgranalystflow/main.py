#!/usr/bin/env python
from pydantic import BaseModel, Field, RootModel
from typing import Dict, Optional, List, Set, Tuple
from crewai import Flow
from crewai.flow.flow import listen, start, and_, or_, router
from .crews.gheanalystcrew.gheanalystcrew_crew import GheAnalystCrew
from .crews.agentmodelcrew.agentmodelcrew_crew import AgentmodelcrewCrew
#from .crews.writercrew.writercrew_crew import WritercrewCrew
#from .crews.pgrorganizingcrew.pgrorganizingcrew_crew import PgrOrganizingCrew
#from .crews.riskanalystcrew.riskanalystcrew_crew import RiskAnalystCrew
#from .crews.visioncrew.visioncrew_crew import VisioncrewCrew


class PgrAnalystFlow(Flow):
	@start()
	def LoadPdf(self):
		#self.state.pdf_path = "C:\\Trabalho\\PGR-MultiAgents\\pgr_analyst\\path\\pgr.pdf"
		print("Loading PDF file...")
	
	@listen(LoadPdf)
	def GheDetector(self):
		gheanalystcrew = GheAnalystCrew()
		ghes = gheanalystcrew.crew().kickoff()
		self.ghes = ghes

	@listen(GheDetector)
	def ExtractAgents(self):
		results = []
		for ghe in self.ghes["ghes"]:
			pgragents = AgentmodelcrewCrew()
			pgr_agent_result = pgragents.crew().kickoff(inputs={"ghe": ghe, "query": f"{ghe} - RECONHECIMENTO DOS RISCOS OCUPACIONAIS"})
			results.append(f"{pgr_agent_result.raw}\n")
			with open("output\\results.md", 'a', encoding='utf-8') as md:	
				md.write(f"{pgr_agent_result.raw}\n\n")
		self.pgr_agent_results = results

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
