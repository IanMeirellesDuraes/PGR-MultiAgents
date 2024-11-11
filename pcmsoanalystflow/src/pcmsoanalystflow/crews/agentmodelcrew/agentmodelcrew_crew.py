from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.pgranalystflow.tools.custom_tool import SimplePDFSearchTool
from src.pgranalystflow.tools.custom_tool import SimplePDFSearchTool2

@CrewBase
class AgentmodelcrewCrew():

	@agent
	def AgentModel(self) -> Agent:
		return Agent(
			config=self.agents_config['AgentModel'],
			tools=[SimplePDFSearchTool2(pdf_path="C:\\ian\\Trabalho\\PGR-MultiAgents\\pgranalystflow\\path\\pgr-brmed2.pdf")],
			verbose=True,
			cache = False
		)

	@task
	def agent_pgr_model_task(self) -> Task:
		return Task(
			config=self.tasks_config['agentpgrmodel_task'],
			async_execution=True
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks, 
			verbose=True
		)
	
#pgragents = AgentmodelcrewCrew()
#pgragents.crew().kickoff(inputs={"ghe": "GHE 17 - RECONHECIMENTO DOS RISCOS OCUPACIONAIS", "query": "GHE 17 - RECONHECIMENTO DOS RISCOS OCUPACIONAIS"})