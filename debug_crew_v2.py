import os
from dotenv import load_dotenv
load_dotenv()

from agents import verifier, financial_analyst, investment_advisor, risk_assessor
from task import analyze_financial_document, investment_analysis, risk_assessment, verification
from crewai import Crew, Process

def debug_objects():
    agents = [verifier, financial_analyst, investment_advisor, risk_assessor]
    tasks = [verification, analyze_financial_document, investment_analysis, risk_assessment]
    
    print("--- Agents ---")
    for i, agent in enumerate(agents):
        print(f"Agent {i} ({agent.role if hasattr(agent, 'role') else 'N/A'}): {type(agent)}")
        if hasattr(agent, 'tools') and agent.tools:
            for tool in agent.tools:
                print(f"  Tool: {getattr(tool, 'name', 'N/A')} ({type(tool)})")
            
    print("\n--- Tasks ---")
    for i, task in enumerate(tasks):
        # Handle potential shadowing/function issues
        task_name = "N/A"
        try:
            if hasattr(task, 'description'):
                task_name = task.description[:30] + "..."
        except:
            pass
        print(f"Task {i} ({task_name}): {type(task)}")
        if hasattr(task, 'tools') and task.tools:
            for tool in task.tools:
                print(f"  Tool: {getattr(tool, 'name', 'N/A')} ({type(tool)})")

    print("\n--- Initializing Crew ---")
    try:
        crew = Crew(agents=agents, tasks=tasks, process=Process.sequential)
        print("Crew initialized successfully.")
    except Exception as e:
        print(f"Crew Initialization Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_objects()
