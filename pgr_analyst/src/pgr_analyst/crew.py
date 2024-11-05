from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
 
from pgr_analyst.tools.custom_tool import SimplePDFSearchTool
from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Set, Tuple


class GheInfo(BaseModel):
	ghes: Dict[str] = Field(..., description="Ghes encontrados no documento, onde a chave é o nome do ghe e o valor é os cargos associados ao respectivo ghe")
	ghes_count: int = Field(..., description="Quantidade de ghes encontrados no documento")
	ghes_pages: List[int] = Field(..., description="Páginas em que os ghes foram encontrados")

class RiskAnalysis(BaseModel):
	risk: Dict[str] = Field(..., description="Grupos de riscos encontrados no documento, onde a chave é o nome do risco e o valor é os tipos de riscos associados ao respectivo grupo")
	risk_levels: List[str] = Field(..., description="Níveis de riscos encontrados no documento")
	risk_count: int = Field(..., description="Quantidade de riscos encontrados no documento")
	risk_pages: List[int] = Field(..., description="Páginas em que os riscos foram encontrados")	


class RiscoModel(BaseModel):
    tipo_do_risco: str = Field(..., description="Tipo do respectivo risco")
    nivel_do_risco: str = Field(..., description="Nível do respectivo risco")

class GrupoDeRiscoModel(BaseModel):
    nome_grupo: Dict[str, RiscoModel] = Field(..., description="Nome do grupo de risco como chave e os riscos associados ao grupo como valor")

class GheModel(BaseModel):
    cargos: str = Field(..., description="Cargos associados ao ghe")
    grupos_de_risco: Dict[str, GrupoDeRiscoModel] = Field(..., description="Grupos de risco associados ao ghe especificado")

class EstruturaModel(BaseModel):
    __root__: Dict[str, GheModel] = Field(..., description="Estrutura de ghes e riscos associados, sendo o nome do ghe a chave e os riscos associados ao ghe como valor")

@CrewBase
class PgrAnalystCrew():
	"""PgrAnalyst crew"""

	@agent
	def GheDetector(self) -> Agent:
		pdf_search_tool = SimplePDFSearchTool(pdf_path="C:\Trabalho\PGR-MultiAgents\pgr_analyst\path\pgr.pdf", query="ghe")
		return Agent(
			config=self.agents_config['GheDetector'],
			tools=[pdf_search_tool],
		)
	
	#@agent
	#def RiskAnalyst(self) -> Agent:
		#pdf_search_tool = SimplePDFSearchTool(pdf_path="C:\\Trabalho\\PGR-MultiAgents\\pgr_analyst\\path\\pgr.pdf", query="risco")
		#return Agent(
			#config=self.agents_config['RiskAnalyst'],
			#tools=[pdf_search_tool],
		#)
	
	@agent
	def RiskDescription(self) -> Agent:
		pdf_search_tool = SimplePDFSearchTool(pdf_path="C:\\Trabalho\\PGR-MultiAgents\\pgr_analyst\\path\\pgr.pdf", query="risco")
		return Agent(
			config=self.agents_config['RiskDescription'],
			tools=[pdf_search_tool],
		)
	
	@agent 
	def PgrExpert(self) -> Agent:
		pdf_search_tool = SimplePDFSearchTool(pdf_path="C:\\Trabalho\\PGR-MultiAgents\\pgr_analyst\\path\\pgr.pdf", query="risco")
		return Agent(
			config=self.agents_config['PgrExpert'],
			tools=[pdf_search_tool],
		)
	
	@task
	def ghe_detector_task(self) -> Task:
		return Task(
			config=self.tasks_config['ghedetector_task'],
			output_file='output\\ghe.md'
		)
	
	#@task
	#def risk_analyst_task(self) -> Task:
		#return Task(
			#config=self.tasks_config['riskanalyst_task'],
			#output_file='output\\risk.md'
		#)
	
	@task
	def risk_description_task(self) -> Task:
		return Task(
			config=self.tasks_config['riskdescription_task'],
			output_file='output\\risk_description.md'
		)
	
	@task
	def pgr_expert_task(self) -> Task:
		return Task(
			config=self.tasks_config['pgrexpert_task'],
			context=[ghe_detector_task, risk_analyst_task, risk_description_task],
			output_file='output\\pgr_expert.md',
			output_pydantic=EstruturaModel
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PgrAnalyst crew"""
		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			verbose=True,
		)

from crewai import Flow
from crewai.flow.flow import listen, start

class PgrAnalystFlow(Flow):
	@start()
	def