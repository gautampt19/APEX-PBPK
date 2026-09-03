"""
APEX-PBPK Web Dashboard — Flask Backend

Routes:
  GET  /                          → Serve the SPA
  POST /api/upload                → Accept PDF upload
  POST /api/run                   → Trigger pipeline (async)
  GET  /api/status/<job_id>       → SSE pipeline progress stream
  GET  /api/results/<paper_name>  → Return extracted JSON + metadata
  GET  /api/colpali-pages/<paper>/<file> → Serve ColPali page images
  GET  /api/papers                → List uploaded papers
"""

import os
import sys
import json
import sqlite3
import uuid
import subprocess
import threading
import time
from pathlib import Path
from flask import (
    Flask, render_template, request, jsonify, Response,
    send_from_directory, stream_with_context
)

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = PROJECT_ROOT / "papers"
PIPELINE_OUTPUT = PROJECT_ROOT / "pipeline_output"
COLPALI_PAGES = PIPELINE_OUTPUT / "colpali_pages"
VENV_PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"

PAPERS_DIR.mkdir(exist_ok=True)
PIPELINE_OUTPUT.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB max upload

# ── Job tracking ─────────────────────────────────────────────────────────────
jobs = {}  # job_id -> { status, progress, log_lines, paper_name, result }


def _run_pipeline(job_id: str, pdf_path: str, use_colpali: bool,
                  model: str, top_k: int, backend: str, run_step: str = "all"):
    """Run the pipeline in a background thread, streaming output to the job."""
    paper_name = Path(pdf_path).stem
    jobs[job_id]["paper_name"] = paper_name
    jobs[job_id]["status"] = "running"

    cmd = [
        str(VENV_PYTHON), str(PROJECT_ROOT / "run_pipeline.py"),
        "--pdf", pdf_path,
        "--backend", backend,
        "--model-extract", model,
        "--model-generate", model,
        "--output-dir", str(PIPELINE_OUTPUT),
        "--run-step", run_step,
        "--non-interactive"
    ]
    if use_colpali:
        cmd.extend(["--use-colpali", "--colpali-top-k", str(top_k)])

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(PROJECT_ROOT),
            bufsize=1,
        )

        for line in iter(proc.stdout.readline, ""):
            line = line.rstrip("\n")
            jobs[job_id]["log_lines"].append(line)

            # Parse progress from step markers
            if line.startswith("STEP:"):
                jobs[job_id]["current_step"] = line[5:].strip()
            elif "✅" in line:
                jobs[job_id]["progress"] = min(
                    jobs[job_id]["progress"] + 20, 95
                )

        proc.wait()

        if proc.returncode == 0:
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["progress"] = 100
        else:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = "Pipeline exited with non-zero code"

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/papers", methods=["GET"])
def list_papers():
    """List all uploaded PDFs."""
    pdfs = sorted([f.name for f in PAPERS_DIR.glob("*.pdf")])
    return jsonify({"papers": pdfs})


@app.route("/api/upload", methods=["POST"])
def upload_pdf():
    """Handle PDF file upload."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    f = request.files["file"]
    if not f.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are accepted"}), 400

    save_path = PAPERS_DIR / f.filename
    f.save(str(save_path))
    
    # Delete old results if this file was processed previously
    paper_name = Path(f.filename).stem
    for ext in ["_params.json", "_cleaned.md", "_pbpk_model.R", "_review.json", "_pbpk_model_fallback.R", "_pbpk_model_retry1.R", "_pbpk_model_retry2.R"]:
        old_file = PIPELINE_OUTPUT / f"{paper_name}{ext}"
        if old_file.exists():
            old_file.unlink()
            
    return jsonify({
        "message": f"Uploaded {f.filename}",
        "filename": f.filename,
        "paper_name": paper_name,
    })


@app.route("/api/run", methods=["POST"])
def run_pipeline():
    """Start the pipeline as a background job."""
    data = request.get_json(force=True)
    filename = data.get("filename")
    if not filename:
        return jsonify({"error": "Missing filename"}), 400

    pdf_path = str(PAPERS_DIR / filename)
    if not os.path.exists(pdf_path):
        return jsonify({"error": f"File not found: {filename}"}), 404

    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {
        "status": "starting",
        "progress": 0,
        "log_lines": [],
        "paper_name": Path(filename).stem,
        "current_step": "",
        "error": None,
    }

    use_colpali = data.get("use_colpali", True)
    model = data.get("model", "qwen3.8:latest")
    top_k = data.get("top_k", 5)
    backend = data.get("backend", "ollama")
    run_step = data.get("run_step", "all")

    t = threading.Thread(
        target=_run_pipeline,
        args=(job_id, pdf_path, use_colpali, model, top_k, backend, run_step),
        daemon=True,
    )
    t.start()

    return jsonify({"job_id": job_id, "message": "Pipeline started"})



@app.route("/api/save-params", methods=["POST"])
def save_params():
    """Save edited parameters from UI."""
    data = request.get_json(force=True)
    paper_name = data.get("paper_name")
    params = data.get("parameters")
    
    if not paper_name or not params:
        return jsonify({"error": "Missing paper_name or parameters"}), 400
        
    params_file = PIPELINE_OUTPUT / f"{paper_name}_params.json"
    
    try:
        with open(params_file, "w") as f:
            json.dump(params, f, indent=4)
        return jsonify({"message": "Parameters saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/status/<job_id>")
def job_status(job_id):
    """SSE endpoint for real-time pipeline progress."""
    if job_id not in jobs:
        return jsonify({"error": "Job not found"}), 404

    def generate():
        last_line_count = 0
        while True:
            job = jobs.get(job_id)
            if not job:
                break

            new_lines = job["log_lines"][last_line_count:]
            last_line_count = len(job["log_lines"])

            event_data = {
                "status": job["status"],
                "progress": job["progress"],
                "current_step": job.get("current_step", ""),
                "new_lines": new_lines,
                "error": job.get("error"),
            }
            yield f"data: {json.dumps(event_data)}\n\n"

            if job["status"] in ("completed", "failed"):
                break

            time.sleep(1)

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/api/results/<paper_name>")
def get_results(paper_name):
    """Return extracted parameters and metadata for a processed paper."""
    params_file = PIPELINE_OUTPUT / f"{paper_name}_params.json"
    r_script = PIPELINE_OUTPUT / f"{paper_name}_pbpk_model.R"
    colpali_dir = PIPELINE_OUTPUT / "colpali_pages"

    if not params_file.exists():
        return jsonify({"error": "No results found for this paper"}), 404

    with open(params_file, "r") as f:
        params = json.load(f)

    r_code = ""
    if r_script.exists():
        with open(r_script, "r") as f:
            r_code = f.read()
    # Also check for fallback / retry R scripts
    if not r_code:
        for suffix in ["_pbpk_model_fallback.R", "_pbpk_model_retry1.R", "_pbpk_model_retry2.R"]:
            alt = PIPELINE_OUTPUT / f"{paper_name}{suffix}"
            if alt.exists():
                with open(alt, "r") as f:
                    r_code = f.read()
                break

    colpali_images = []
    if colpali_dir.exists():
        colpali_images = sorted([
            f.name for f in colpali_dir.glob("*.png")
        ])

    # Load LLM review if available
    review = None
    review_file = PIPELINE_OUTPUT / f"{paper_name}_review.json"
    if review_file.exists():
        with open(review_file, "r") as f:
            review = json.load(f)

    return jsonify({
        "paper_name": paper_name,
        "parameters": params,
        "r_code": r_code,
        "colpali_pages": colpali_images,
        "review": review,
    })


@app.route("/api/colpali-pages/<filename>")
def serve_colpali_page(filename):
    """Serve a ColPali-retrieved page image."""
    return send_from_directory(str(COLPALI_PAGES), filename)


# ── Main ─────────────────────────────────────────────────────────────────────


# ── Database Viewer Routes ──────────────────────────────────────────────────

def get_db_connection():
    db_path = PROJECT_ROOT / "pk_parameters.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/database")
def database_viewer():
    return render_template("database.html")

@app.route("/api/db/papers", methods=["GET"])
def db_list_papers():
    try:
        conn = get_db_connection()
        papers = conn.execute("SELECT paper_id, title, created_at FROM documents ORDER BY created_at DESC").fetchall()
        conn.close()
        return jsonify({"papers": [dict(p) for p in papers]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/db/parameters/<path:paper_id>", methods=["GET"])
def db_get_parameters(paper_id):
    try:
        conn = get_db_connection()
        params = conn.execute("SELECT * FROM pk_parameters WHERE paper_id = ? ORDER BY table_id, id", (paper_id,)).fetchall()
        doc = conn.execute("SELECT * FROM documents WHERE paper_id = ?", (paper_id,)).fetchone()
        conn.close()
        return jsonify({
            "document": dict(doc) if doc else None,
            "parameters": [dict(p) for p in params]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  APEX-PBPK Web Dashboard")
    print("  http://localhost:5000")
    print("=" * 60 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
