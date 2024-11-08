from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pgranalystflow.tools.custom_tool import SimplePDFSearchTool
from pgranalystflow.tools.custom_tool import SimplePDFSearchTool2

@CrewBase
class AgentmodelcrewCrew():

	@agent
	def AgentModel(self) -> Agent:
		return Agent(
			config=self.agents_config['AgentModel'],
			tools=[SimplePDFSearchTool2(pdf_path="C:\\Trabalho\\PGR-MultiAgents\\pgranalystflow\\path\\pgr-brmed1.pdf")],
			verbose=True,
			cache = False
		)

	@task
	def agent_pgr_model_task(self) -> Task:
		return Task(
			config=self.tasks_config['agentpgrmodel_task'],
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks, 
			verbose=True
		)
	
#pgragents = AgentmodelcrewCrew()
#pgragents.crew().kickoff(inputs={"ghe": "GHE 03", "query": "GHE 03 - RECONHECIMENTO DOS RISCOS OCUPACIONAIS"})