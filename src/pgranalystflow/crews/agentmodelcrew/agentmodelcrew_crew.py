from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.custom_tool import SimplePDFSearchTool2


@CrewBase
class AgentmodelcrewCrew:

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    @agent
    def AgentModel(self) -> Agent:
        simple_pdf_tool = SimplePDFSearchTool2(pdf_path=self.pdf_path)
        return Agent(
            config=self.agents_config["AgentModel"],
            tools=[simple_pdf_tool],
            verbose=True,
            cache=False,
        )

    @task
    def agent_pgr_model_task(self) -> Task:
        return Task(config=self.tasks_config["agentpgrmodel_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, verbose=True)


# pgragents = AgentmodelcrewCrew()
# pgragents.crew().kickoff(inputs={"ghe": "GHE 17 - RECONHECIMENTO DOS RISCOS OCUPACIONAIS", "query": "GHE 17 - RECONHECIMENTO DOS RISCOS OCUPACIONAIS"})
