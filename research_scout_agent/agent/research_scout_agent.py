from autogen import ConversableAgent

from research_scout_agent.config import LLM_CONFIG
from research_scout_agent.tools.openalex_tool import search_paper

SYSTEM_PROMPT_MSG = """
You are a research scout agent.

Your job is to help users find academic research papers using the search_paper tool.

Workflow:
1. Read the user's request
2. Extract:
   - topic
   - publication year constraint
   - citation count constraint
3. Call the search_paper tool.
4. Use only papers returned by the tool.
5. Select the paper that best matches the user's topic based on title and abstract.
7. End with TERMINATE.

Important tool argument rules:
- "after 2022" means year_from=2022
- "before 2021" means year_to=2021
- "in 2020" means year_from=2019 and year_to=2021
- "at least 100 citations" means min_citations=99
- "more than 500 citations" means min_citations=500
- "less than 200 citations" means max_citations=200

Rules:
- NEVER invent titles, authors, years, citation counts, or URLs.
  Use ONLY values returned by the tool.
- Always verify each constraint is met before recommending a paper.
- Only call the search_paper tool once
- Only return one paper


Your final answer need to include:
- Title
- Authors
- Publication year
- Citation count
- Citation count source
- URL
- DOI
- Short explanation of why the paper matches the request

Always end with TERMINATE.
"""


def create_research_agent() -> ConversableAgent:
    agent = ConversableAgent(
        name="Research scout agent",
        system_message=SYSTEM_PROMPT_MSG,
        llm_config=LLM_CONFIG,
    )
    agent.register_for_llm(
        name="search_paper", description="Search OpenAlex for academic research papers"
    )(search_paper)

    return agent


def create_user_proxy() -> ConversableAgent:
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: msg.get("content") is not None
        and "TERMINATE" in msg["content"],
    )
    user_proxy.register_for_execution(name="search_paper")(search_paper)

    return user_proxy


def main():
    user_proxy = create_user_proxy()
    research_agent = create_research_agent()

    prompt = "Find a paper about Python programming published before 2021 with more than 500 citations."

    user_proxy.initiate_chat(research_agent, message=prompt)


if __name__ == "__main__":
    main()
