import os
import uuid
import threading
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse

from crewai import Crew, Process
from agents import expert_analyst
from task import unified_financial_analysis
from database import save_result, update_status, get_result

app = FastAPI(title="Financial Document Analyzer")

def run_crew_logic(task_id: str, query: str, file_path: str):
    """Executes the CrewAI analysis logic in the background."""
    try:
        # Initialize the crew with the Single Expert agent for high reliability
        financial_crew = Crew(
            agents=[expert_analyst],
            tasks=[unified_financial_analysis],
            process=Process.sequential,
            verbose=True
        )

        # Kickoff the analysis
        # The path corresponds to variables in the task description
        result = financial_crew.kickoff(inputs={'query': query, 'path': file_path})
        
        # Save structured results to the database
        update_status(task_id, "COMPLETED", str(result))
        
    except Exception as e:
        error_msg = f"Task Failed: {str(e)}"
        print(error_msg)
        update_status(task_id, "FAILED", error_msg)

@app.get("/")
def read_root():
    return {"message": "Financial Document Analyzer API is running.", "endpoints": ["/analyze", "/status/{task_id}", "/results/{task_id}"]}

@app.post("/analyze")
async def analyze_document_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    query: str = Form(...)
):
    """Endpoint to upload a file and start the analysis queue."""
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Generate unique ID and file path
    file_id = str(uuid.uuid4())
    temp_file_path = os.path.join("data", f"{file_id}_{file.filename}")
    
    # Save uploaded file
    with open(temp_file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Register task in DB as PROCESSING
    save_result(file_id, query, file.filename, "PROCESSING", "")
    
    # Add to background worker
    background_tasks.add_task(run_crew_logic, file_id, query, temp_file_path)
    
    return {
        "status": "accepted",
        "task_id": file_id,
        "message": "Analysis started in background.",
        "poll_url": f"/status/{file_id}"
    }

@app.get("/analyze")
def get_analyze_info():
    return {
        "message": "To analyze a document, send a POST request to this endpoint with 'file' (Multipart) and 'query' (Form field).",
        "example_curl": "curl -X POST -F 'file=@your_file.pdf' -F 'query=Analyze this' http://localhost:8001/analyze"
    }

@app.get("/status/{task_id}")
def get_task_status(task_id: str):
    """Check the status of a specific task."""
    result = get_result(task_id)
    if result:
        return {
            "task_id": task_id,
            "status": result["status"],
            "created_at": result["created_at"]
        }
    return JSONResponse(status_code=404, content={"message": "Task ID not found."})

@app.get("/results/{task_id}")
def get_task_results(task_id: str):
    """Retrieve the results of a completed task."""
    result = get_result(task_id)
    if result:
        if result["status"] == "COMPLETED":
            return {
                "task_id": task_id,
                "status": "COMPLETED",
                "analysis": result["result"]
            }
        elif result["status"] == "FAILED":
           return {
                "task_id": task_id,
                "status": "FAILED",
                "error": result["result"] # Holds error message
            }
        else:
            return {
                "task_id": task_id,
                "status": result["status"],
                "message": "Results are not ready yet."
            }
    return JSONResponse(status_code=404, content={"message": "Task ID not found."})

if __name__ == "__main__":
    import uvicorn
    # Using 0.0.0.0 for visibility, but refer to it as localhost in the README
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)