from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.pgranalystflow.tools.custom_tool import SimplePDFSearchTool
from src.pgranalystflow.tools.custom_tool import SimplePDFSearchTool2

@CrewBase
class GheextractcrewCrew():
	@agent
	def GheExtractor(self) -> Agent:
		return Agent(
			config=self.agents_config['GheExtractor'],
			tools=[SimplePDFSearchTool2(pdf_path="C:/Trabalho/PGR-MultiAgents/pgranalystflow/output/ghes.pdf")], 
			verbose=True
		)
	
	@task
	def ghe_extractor_task(self) -> Task:
		return Task(
			config=self.tasks_config['gheextractor_task'],
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True,
		)
	
#pgragents = GheextractcrewCrew()
#pgragents.crew().kickoff(inputs={"ghe": "GHE 03 - DESCRICAO DE ATIVIDADE"})