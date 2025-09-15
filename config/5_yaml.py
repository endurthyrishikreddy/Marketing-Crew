from Scripts.pywin32_postinstall import verbose
from crewai import Agent , Task , Crew , Process
from crewai.project import CrewBase, agent, crew , task

from crewai_tools import SerperDevTool, ScrapeWebsiteTool, DirectoryReadTool

from dotenv import load_dotenv
load_dotenv()

import os
os.environ["RICH_NO_COLOR"] = "1"
@CrewBase
class BlogCrew():
    agent_config= "config/agent.yaml"
    task_config = "config/task.yaml"

    @agent
    def researcher(self)-> Agent:
        return Agent(
            config=self.agent_config['research_agent'], # type: ignore[index]
            tools= [SerperDevTool(),ScrapeWebsiteTool(),DirectoryReadTool()],
            verbose=False,
        )
    @agent
    def writer(self)-> Agent:
        return Agent(
            config=self.agent_config['writer_agent'], # type: ignore[index]
            verbose=False,
        )

    @task
    def research_task(self)-> Task:
        return Task(
            config=self.task_config['research_task'], # type: ignore[index]
            agent=self.researcher(),
        )

    @task
    def writer_task(self)-> Task:
        return Task(
            config=self.task_config['writer_task'], # type: ignore[index]
            agent=self.writer(),
        )

    @crew
    def crew(self)-> Crew:
        return Crew(
            agents=[self.researcher(), self.writer()],
            tasks=[self.research_task(), self.writer_task()],
            verbose=False,
        )

if __name__ == '__main__':
    blog_crew = BlogCrew()
    # Change this line
    blog_crew.crew().kickoff(inputs={"Topic":"Future of the electrical vehicles"})