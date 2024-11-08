from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
from pgranalystflow.tools.custom_tool import SimplePDFSearchTool

@CrewBase 
class PgrOrganizingCrew():
	@agent 
	def PgrExpert(self) -> Agent:
		pdf_search_tool = SimplePDFSearchTool(pdf_path="C:\\Trabalho\\PGR-MultiAgents\\pgranalystflow\\path\\pgr-brmed2.pdf", query="RECONHECIMENTO DOS RISCOS OCUPACIONAIS ")
		return Agent(
			config=self.agents_config['PgrExpert'],
			tools=[pdf_search_tool],
		)

	@task
	def pgr_expert_task(self) -> Task:
		return Task(
			config=self.tasks_config['pgrexpert_task'],
			output_file='output\\pgr_expert.md',
			#output_pydantic=EstruturaModel
		)
	
	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			verbose=True,
		)