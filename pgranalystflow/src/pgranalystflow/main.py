#!/usr/bin/env python
from pydantic import BaseModel, Field, RootModel
from typing import Dict, Optional, List, Set, Tuple
from crewai import Flow
from crewai.flow.flow import listen, start, and_, or_, router
from .crews.gheanalystcrew.gheanalystcrew_crew import GheAnalystCrew
from .crews.pgrorganizingcrew.pgrorganizingcrew_crew import PgrOrganizingCrew
from .crews.riskanalystcrew.riskanalystcrew_crew import RiskAnalystCrew

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

	@listen(LoadPdf)
	def RiskDescription(self):
		riskanalystcrew = RiskAnalystCrew()
		risk_analysis = riskanalystcrew.crew().kickoff()
		self.risk_analysis = risk_analysis
	
	@listen(and_(GheDetector, RiskDescription))
	def PgrDescription(self):
		pgrorganizingcrew = PgrOrganizingCrew()
		pgr_structure = pgrorganizingcrew.crew().kickoff(inputs={"ghes": self.ghes, "risk_analysis": self.risk_analysis})
		return pgr_structure


def kickoff():
    flow = PgrAnalystFlow()
    flow.kickoff()


def plot():
    flow = PgrAnalystFlow()
    flow.plot()


if __name__ == "__main__":
    kickoff()
