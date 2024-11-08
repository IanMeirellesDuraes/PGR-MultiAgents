from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import VisionTool
#from pgranalystflow.tools.custom_tool import ImageAnalysisTool

@CrewBase
class VisioncrewCrew():
	@agent
	def VisionAnalyst(self) -> Agent:
		return Agent(
			config=self.agents_config['VisionAnalyst'],
			tools=[VisionTool()],
		)

	@task
	def vision_analyst_task(self) -> Task:
		return Task(
			config=self.tasks_config['visionanalyst_task'],
			output_file='output\\visionreport.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Visioncrew crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks, 
			verbose=True,
		)
	
crew = VisioncrewCrew()
crew.crew().kickoff(inputs={"image_paths_url": ["\\C:\\Trabalho\\PGR-MultiAgents\\pgranalystflow\\imgs\\pagina_135.png\\", "\\C:\\Trabalho\\PGR-MultiAgents\\pgranalystflow\\imgs\\pagina_136.png\\"]})
