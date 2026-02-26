import os
from dotenv import load_dotenv
load_dotenv()

from main import run_crew_logic
import sqlite3
import time

def main():
    query = "Analyze Tesla's performance in Q2 2025"
    # Use the sample file that we know exists
    file_path = r"data\sample.pdf"
    
    if not os.path.exists(file_path):
        # Create a blank data directory if missing
        os.makedirs("data", exist_ok=True)
        print(f"File not found: {file_path}. Please place a PDF at this path.")
        return

    task_id = "cli_test_task"
    print(f"Running crew with query: {query}")
    try:
        # Run the logic (it will save to the database)
        run_crew_logic(task_id, query, file_path)
        
        # Fetch and print result from database
        from database import get_result
        res = get_result(task_id)
        if res:
            print("\n--- Analysis Result ---")
            print(res['result'])
            print("-----------------------")
        
    except Exception as e:
        import traceback
        print(f"Error caught in main: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    import os
    main()
