from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
#from crewai_tools import FileReadTool


@CrewBase
class JsonorganizercrewCrew():

	@agent
	def JsonOrganizerAgent(self) -> Agent:
		return Agent(
			config=self.agents_config['JsonOrganizerAgent'],
			#tools=[FileReadTool(file_path="C:/Trabalho/PGR-MultiAgents/pgranalystflow/output/structed.txt")],
			verbose=True
		)

	@task
	def json_organizer_task(self) -> Task:
		return Task(
			config=self.tasks_config['jsonorganizer_task'],
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)

#jsoncrew = JsonorganizercrewCrew()
#jsoncrew.crew().kickoff()