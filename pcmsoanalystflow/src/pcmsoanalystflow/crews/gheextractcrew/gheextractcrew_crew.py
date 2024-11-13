from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.custom_tool import SimplePDFSearchTool2

@CrewBase
class GheextractcrewCrew():
	@agent
	def GheExtractor(self) -> Agent:
		return Agent(
			config=self.agents_config['GheExtractor'],
			tools=[SimplePDFSearchTool2(pdf_path="C:\\ian\\Trabalho\\PGR-MultiAgents\\pgranalystflow\\path\\pgr-brmed2.pdf")], 
			verbose=True
		)
	
	@task
	def ghe_extractor_task(self) -> Task:
		return Task(
			config=self.tasks_config['gheextractor_task'],
			async_execution=True
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
#pgragents.crew().kickoff(inputs={"ghe": "GHE 03"})