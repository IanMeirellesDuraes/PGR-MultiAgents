from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
from pgranalystflow.tools.custom_tool import SimplePDFSearchTool
from pydantic import BaseModel, Field, RootModel
from typing import Dict, Optional, List, Set, Tuple

#class GheInfo(BaseModel):
	#ghes: Dict[str, list] = Field(..., default_factory=dict, description="Ghes encontrados no documento, onde a chave é o ghe correspondente e o valor é os cargos associados ao respectivo ghe")
	#ghes_pages: List[int] = Field(..., description="Páginas em que os ghes foram encontrados")

@CrewBase
class GheAnalystCrew():
	@agent
	def GheDetector(self) -> Agent:
		pdf_search_tool = SimplePDFSearchTool(pdf_path="C:\\Trabalho\\PGR-MultiAgents\\pgranalystflow\\path\\pgr-brmed2.pdf", query="DESCRIÇÃO DE ATIVIDADE")
		return Agent(
			config=self.agents_config['GheDetector'],
			tools=[pdf_search_tool],
		)

	@task
	def ghe_detector_task(self) -> Task:
		return Task(
			config=self.tasks_config['ghedetector_task'],
			output_file='output\\ghe.md',
			#output_pydantic=GheInfo,
		)
	
	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			verbose=True,
		)