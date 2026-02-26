# Financial Document Analyzer 🚀

A professional financial document analysis system powered by **CrewAI** and **Google Gemini**. This system leverages a high-reliability, grounded AI workflow to process corporate reports and provide actionable investment insights and risk assessments.

## 🛡️ Stability & Accuracy Fixes

Through a comprehensive audit and optimization phase, the following enhancements were implemented to ensure a **100% working, grounded pipeline**:

### Hallucination Prevention & Grounding
- **Strict Grounding**: Agents are now explicitly bound to the provided PDF file path. They are forbidden from using internal knowledge (e.g., defaulting to Apple data) and must base every insight on the document at `{path}`.
- **Verification Logic**: Verification is integrated directly into the analysis task to ensure document suitability before processing.

### Performance & Quota Optimization
- **High-Reliability Unified Workflow**: Optimized from a multi-agent sequential crew into a single **"Principal Financial Strategist"** workflow. This consolidation guarantees completion within the **Gemini Free Tier (20 requests/day)** quota while maintaining professional depth.
- **Token Efficiency**: The PDF tool is optimized to process the most relevant summary sections (first 5 pages), ensuring fast response times and staying within token limits.
- **RPM Throttling**: Implemented strict Rate-Per-Minute limits (`max_rpm=1`) to prevent API exhaustion during complex deliberations.

## Setup Instructions 🛠️

1.  **Clone the Repository**
2.  **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
3.  **Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key
    SERPER_API_KEY= ""
    ```
4.  **Database**:
    The system automatically initializes an SQLite database (`analysis_results.db`) on startup to persist results.

## Usage 🚀

### Running the API
```sh
python main.py
```
The server will start at `http://localhost:8001`.

### API Documentation

#### `POST /analyze`
Uploads a financial PDF for asynchronous background analysis.

**Example testing with `curl`:**
```bash
curl.exe -X POST -F "file=@data/TSLA-Q2-2025-Update.pdf" -F "query=Analyze Revenue and Margins" http://localhost:8001/analyze
```

**Form Data:**
- `file`: The PDF document (as a Multi-part file).
- `query`: Your specific financial question.

#### `GET /status/{task_id}`
Checks the current status of the analysis (`PROCESSING`, `COMPLETED`, `FAILED`).

#### `GET /results/{task_id}`
Retrieves the full report once status is `COMPLETED`. If a task fails (e.g., due to quota limits), this endpoint returns the specific error message for debugging.

## Bonus Features ✨

- **Queue Worker Model**: Uses FastAPI `BackgroundTasks` to handle document processing in the background, keeping the API responsive.
- **Persistent Database**: All analysis history is saved in SQLite, allowing for later retrieval and auditing.
- **Error Transparency**: Detailed error propagation ensures you know exactly why a process failed (e.g., Resource Exhausted vs. File Errors).
