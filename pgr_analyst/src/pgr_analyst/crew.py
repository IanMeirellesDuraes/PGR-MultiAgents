from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
from pgr_analyst.tools.custom_tool import SimplePDFSearchTool
#from crewai_tools import PDFSearchTool
#from crewai_tools import JSONSearchTool
from pydantic import BaseModel, Field

@CrewBase
class PgrAnalystCrew():
	"""PgrAnalyst crew"""

	@agent
	def GheDetector(self) -> Agent:
		pdf_search_tool = SimplePDFSearchTool(pdf_path="C:\Trabalho\PGR-MultiAgents\pgr_analyst\path\pgr.pdf", query="ghe")
		return Agent(
			config=self.agents_config['GheDetector'],
			tools=[pdf_search_tool],
			verbose=True
		)
	
	@agent
	def RiskAnalyst(self) -> Agent:
		pdf_search_tool = SimplePDFSearchTool(pdf_path="C:\\Trabalho\\PGR-MultiAgents\\pgr_analyst\\path\\pgr.pdf", query="risco")
		return Agent(
			config=self.agents_config['RiskAnalyst'],
			tools=[pdf_search_tool],
			verbose=True
		)
	
	@agent
	def RiskDescription(self) -> Agent:
		pdf_search_tool = SimplePDFSearchTool(pdf_path="C:\\Trabalho\\PGR-MultiAgents\\pgr_analyst\\path\\pgr.pdf", query="risco")
		return Agent(
			config=self.agents_config['RiskDescription'],
			tools=[pdf_search_tool],
			verbose=True
		)
	
	@agent 
	def PgrExpert(self) -> Agent:
		pdf_search_tool = SimplePDFSearchTool(pdf_path="C:\\Trabalho\\PGR-MultiAgents\\pgr_analyst\\path\\pgr.pdf", query="risco")
		return Agent(
			config=self.agents_config['PgrExpert'],
			tools=[pdf_search_tool],
			verbose=True,
		)
	
	@task
	def GheDetectorTask(self) -> Task:
		return Task(
			config=self.tasks_config['ghedetector_task'],
			output_file='output\\ghe.md'
		)
	
	@task
	def RiskAnalyst_Task(self) -> Task:
		return Task(
			config=self.tasks_config['riskanalyst_task'],
			output_file='output\\risk.md'
		)
	
	@task
	def RiskDescription_Task(self) -> Task:
		return Task(
			config=self.tasks_config['riskdescription_task'],
			output_file='output\\risk_description.md'
		)
	
	@task
	def PgrExpert_Task(self) -> Task:
		return Task(
			config=self.tasks_config['pgrexpert_task'],
			output_file='output\\pgr_expert.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PgrAnalyst crew"""
		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential, 
			verbose=True,
		)