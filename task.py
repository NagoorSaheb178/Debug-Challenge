from crewai import Task
from agents import expert_analyst
from tools import read_data_tool, analyze_investment_tool, create_risk_assessment_tool

## Unified Financial Analysis Task
# This single task handles everything to ensure completion within the 20-request free tier quota.
unified_financial_analysis = Task(
    description=(
        "1. Read the document at {path} using 'read_data_tool'.\n"
        "2. Analyze the data to answer: {query}.\n"
        "3. Provide strategic investment insights (use 'analyze_investment_tool').\n"
        "4. Identify potential risks (use 'create_risk_assessment_tool').\n"
        "CRITICAL: Base every insight ONLY on the data from the provided file. Accuracy is mandatory."
    ),
    expected_output="A comprehensive, grounded financial report including analysis, strategy, and risk assessment.",
    agent=expert_analyst,
    tools=[read_data_tool, analyze_investment_tool, create_risk_assessment_tool]
)