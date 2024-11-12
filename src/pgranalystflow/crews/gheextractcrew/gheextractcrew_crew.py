from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.custom_tool import SimplePDFSearchTool2

@CrewBase
class GheextractcrewCrew():

	def __init__(self, pdf_path: str):
		self.pdf_path = pdf_path

	@agent
	def GheExtractor(self) -> Agent:
		simple_pdf_tool = SimplePDFSearchTool2(pdf_path=self.pdf_path)
		return Agent(
			config=self.agents_config['GheExtractor'],
			tools=[simple_pdf_tool], 
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