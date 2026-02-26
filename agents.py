from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import read_data_tool, analyze_investment_tool, create_risk_assessment_tool

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")

# Single Expert Agent to handle the entire pipeline within quota limits
expert_analyst = Agent(
    role="Principal Financial Strategist",
    goal="Perform a comprehensive analysis, investment strategy, and risk assessment for: {query}",
    verbose=True,
    backstory=(
        "You are an elite financial consultant. You must use 'read_data_tool' to access the file at {path}. "
        "Your task is to provide a unified report covering: 1) Fact-based analysis of the document, "
        "2) Strategic investment recommendations, and 3) Potential risk factors. "
        "CRITICAL: Base every single detail ONLY on the provided document. If you cannot find data, say so."
    ),
    tools=[read_data_tool, analyze_investment_tool, create_risk_assessment_tool],
    llm=llm,
    max_iter=2,
    max_rpm=2,
    allow_delegation=False
)
