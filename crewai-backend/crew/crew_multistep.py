# crew/crew_multistep.py
import os, sys, json
from typing import Any, Dict
from crewai import Agent, Task, Crew, Process

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from .multi_tools import (
    ExpandQueriesTool,
    SearchCollectTool,
    SummarizeDocsTool,
    IdeateVenturesTool,
    EstimateMarketsTool,
    ScoreAndFilterTool,
    GenerateInsightsTool,
    WhiteSpaceTool,
)

def _build_llm():
    # CrewAI reads LiteLLM provider via env (OPENAI_API_KEY, MISTRAL_API_KEY, etc.)
    # Return None to use defaults; our tools are LLM-free so we’re safe from 429s.
    return None

def build_multi_crew() -> Crew:
    llm = _build_llm()

    # instantiate tools
    t_expand = ExpandQueriesTool()
    t_search = SearchCollectTool()
    t_summarize = SummarizeDocsTool()
    t_ideate = IdeateVenturesTool()
    t_est = EstimateMarketsTool()
    t_score = ScoreAndFilterTool()
    t_insights = GenerateInsightsTool()
    t_white = WhiteSpaceTool()

    researcher = Agent(role="Researcher", goal="Expand queries.", backstory="Frames market queries.",
                       allow_delegation=False, llm=llm, tools=[t_expand], verbose=True)

    collector = Agent(role="Collector", goal="Search the web and collect sources.",
                      backstory="Finds the most relevant sources via SerpAPI and fetches pages.",
                      allow_delegation=False, llm=llm, tools=[t_search], verbose=True)

    summarizer = Agent(role="Summarizer", goal="Summarize docs to Title/Summary/URL.",
                       backstory="Condenses content faithfully.", allow_delegation=False,
                       llm=llm, tools=[t_summarize], verbose=True)

    ideator = Agent(role="Venture Ideator", goal="Generate venture ideas from summaries.",
                    backstory="Creates concise ideas and maps to source URLs.",
                    allow_delegation=False, llm=llm, tools=[t_ideate], verbose=True)

    analyst = Agent(role="Market Analyst", goal="Estimate TAM/SAM/SOM/CAGR/fit.",
                    backstory="Provides credible market approximations.", allow_delegation=False,
                    llm=llm, tools=[t_est], verbose=True)

    scorer = Agent(role="Venture Scorer", goal="Score and filter to top ideas.",
                   backstory="Applies feasibility and growth criteria.",
                   allow_delegation=False, llm=llm, tools=[t_score], verbose=True)

    strategist = Agent(role="Strategist", goal="Expand solution insights (GTM, differentiation).",
                       backstory="Turns scored ventures into proposals.",
                       allow_delegation=False, llm=llm, tools=[t_insights], verbose=True)

    gapfinder = Agent(role="Gap Finder", goal="White-space analysis and company fit.",
                      backstory="Compares against competitors; aligns with company.",
                      allow_delegation=False, llm=llm, tools=[t_white], verbose=True)

    task_expand = Task(description="Expand queries for focus_area JSON.", agent=researcher,
                       expected_output="JSON with queries", tools=[t_expand])
    task_collect = Task(description="Collect sources from queries_json.", agent=collector,
                        expected_output="JSON with docs", tools=[t_search])
    task_summarize = Task(description="Summarize docs_json to summaries JSON.", agent=summarizer,
                          expected_output="JSON with summaries", tools=[t_summarize])
    task_ideate = Task(description="Generate venture ideas from summaries_json.", agent=ideator,
                       expected_output="JSON with ideas and idea_source", tools=[t_ideate])
    task_estimate = Task(description="Estimate markets from ideas_json.", agent=analyst,
                         expected_output="JSON with estimates", tools=[t_est])
    task_score = Task(description="Score and filter from estimates_json with top_k and min_score.",
                      agent=scorer, expected_output="JSON with scored", tools=[t_score])
    task_insights = Task(description="Generate insights from scored_json and ideas_or_mapping_json.",
                         agent=strategist, expected_output="JSON with finals", tools=[t_insights])
    task_white = Task(description="White-space from finals_json and company.", agent=gapfinder,
                      expected_output="JSON with ventures and timestamp", tools=[t_white])

    crew = Crew(
        agents=[researcher, collector, summarizer, ideator, analyst, scorer, strategist, gapfinder],
        tasks=[task_expand, task_collect, task_summarize, task_ideate, task_estimate, task_score, task_insights, task_white],
        process=Process.sequential,
        verbose=True,
    )
    return crew


def run_with_multi_crew(focus_area: str, company: str, num_ideas: int = 5) -> Dict[str, Any]:
    crew = build_multi_crew()

    t_expand = crew.tasks[0].tools[0]
    t_search = crew.tasks[1].tools[0]
    t_summarize = crew.tasks[2].tools[0]
    t_ideate = crew.tasks[3].tools[0]
    t_est = crew.tasks[4].tools[0]
    t_score = crew.tasks[5].tools[0]
    t_insights = crew.tasks[6].tools[0]
    t_white = crew.tasks[7].tools[0]

    q_json = t_expand.run(focus_area=focus_area)
    docs_json = t_search.run(queries_json=q_json)
    sums_json = t_summarize.run(docs_json=docs_json)
    ideas_json = t_ideate.run(summaries_json=sums_json)
    est_json = t_est.run(ideas_json=ideas_json)
    scored_json = t_score.run(estimates_json=est_json, top_k=max(1, int(num_ideas)), min_score=7.0)
    finals_json = t_insights.run(scored_json=scored_json, ideas_or_mapping_json=ideas_json)
    ventures_json = t_white.run(finals_json=finals_json, company=company)

    return json.loads(ventures_json)
