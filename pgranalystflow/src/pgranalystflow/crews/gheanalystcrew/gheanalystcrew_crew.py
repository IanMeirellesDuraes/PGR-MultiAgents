from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
from pgranalystflow.tools.custom_tool import SimplePDFSearchTool2
from pydantic import BaseModel, Field, RootModel
from typing import Dict, Optional, List, Set, Tuple

class GheInfo(BaseModel):
	ghes: List[str] = Field(..., description="Lista de TODOS os GHE encontrados no pdf")

@CrewBase
class GheAnalystCrew():
	
	def __init__(self, pdf_path: str):
		self.pdf_path = pdf_path

	@agent
	def GheDetector(self) -> Agent:
		simple_pdf_tool = SimplePDFSearchTool2(pdf_path=self.pdf_path)
		return Agent(
			config=self.agents_config['GheDetector'],
			tools=[simple_pdf_tool],
		)

	@task
	def ghe_detector_task(self) -> Task:
		return Task(
			config=self.tasks_config['ghedetector_task'],
			output_pydantic=GheInfo,
		)
	
	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			verbose=True,
			process=Process.sequential
		)
	
#crew = GheAnalystCrew()
#ghes = crew.crew().kickoff()