from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
from pgr_analyst.tools.custom_tool import SimplePDFSearchTool
from pydantic import BaseModel, Field

@CrewBase
class PgrAnalystCrew():
	"""PgrAnalyst crew"""

	@agent
	def PgrExpert(self) -> Agent:
		pdf_search_tool = SimplePDFSearchTool(pdf_path="pgr_analyst/path/pgr.pdf")
		#pdf_search = pdf_search_tool.run("risco, inventário de risco, nível de risco, agente causador, ghe, grupos homogêneos de exposição, função, cargo, descrição do agente, médio, baixo")
		return Agent(
			config=self.agents_config['PgrExpert'],
			tools=[pdf_search_tool],
			verbose=True
		)

	@task
	def select_task(self) -> Task:
		return Task(
			config=self.tasks_config['select_task'],
			output_file='select.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PgrAnalyst crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential, # Default process
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)