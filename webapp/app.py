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
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))
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
        str(VENV_PYTHON), "-m", "pk_pbpk_extractor.main",
        "--pdf", pdf_path,
        "--skip-colpali"
    ]

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

@app.route("/database")
def database_viewer():
    return render_template("database.html")

@app.route("/api/db/papers", methods=["GET"])
def db_list_papers():
    try:
        from pk_pbpk_extractor.storage.db_handler import _get_supabase
        sb = _get_supabase()
        res = sb.table("documents").select("paper_id, title, created_at").order("created_at", desc=True).execute()
        papers = res.data or []
        return jsonify({"papers": papers})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/db/parameters/<path:paper_id>", methods=["GET"])
def db_get_parameters(paper_id):
    try:
        from pk_pbpk_extractor.storage.db_handler import _get_supabase
        sb = _get_supabase()
        res_params = sb.table("pk_parameters").select("*").eq("paper_id", paper_id).execute()
        params = res_params.data or []
        
        res_doc = sb.table("documents").select("*").eq("paper_id", paper_id).limit(1).execute()
        doc = res_doc.data[0] if res_doc.data else None
        
        return jsonify({
            "document": doc,
            "parameters": params
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500




# ─── Model Staging & Generation Routes ────────────────────────────────────────

@app.route("/model-staging")
def model_staging():
    return render_template("model_staging.html")


@app.route("/api/model/stage", methods=["POST"])
def model_stage():
    """
    Pull all pk_parameters for a paper from Supabase, send them to the local
    Ollama LLM to assign PBPK model values, and return the staged JSON.
    """
    import json, re as _re
    data = request.get_json(force=True)
    paper_id = data.get("paper_id", "").strip()
    if not paper_id:
        return jsonify({"error": "paper_id is required"}), 400

    # ── 1. Fetch from Supabase ────────────────────────────────────────────────
    try:
        from pk_pbpk_extractor.storage.db_handler import _get_supabase
        sb = _get_supabase()
        res_params = sb.table("pk_parameters").select("*").eq("paper_id", paper_id).execute()
        res_doc    = sb.table("documents").select("*").eq("paper_id", paper_id).limit(1).execute()
        params_rows = res_params.data or []
        doc         = res_doc.data[0] if res_doc.data else {}
    except Exception as e:
        return jsonify({"error": f"Supabase fetch failed: {e}"}), 500

    if not params_rows:
        return jsonify({"error": "No parameters found for this paper in the database"}), 404

    # ── 2. Build parameter summary for LLM ───────────────────────────────────
    param_lines = []
    for p in params_rows:
        name = p.get("parameter_name", "?")
        canon_raw = p.get("canonical_name") or ""
        try:
            import json as _json2
            canon_data = _json2.loads(canon_raw) if str(canon_raw).startswith("{") else {}
            canon = canon_data.get("canonical_name", name)
            pbpko = canon_data.get("pbpko_id", "")
        except Exception:
            canon = canon_raw or name
            pbpko = ""

        val   = p.get("value", "?")
        unit  = p.get("unit", "")
        spec  = p.get("species", "")
        route = p.get("route", "")
        dose  = p.get("dose", "")
        param_lines.append(
            f"  - [{pbpko}] {name} (canonical: {canon}): {val} {unit}"
            + (f" | species: {spec}" if spec else "")
            + (f" | route: {route}" if route else "")
            + (f" | dose: {dose}" if dose else "")
        )

    paper_title = doc.get("title", paper_id)
    param_block = "\n".join(param_lines)

    # ── 3. Build LLM prompt ───────────────────────────────────────────────────
    prompt = f"""You are a PBPK (physiologically-based pharmacokinetic) modelling expert.
Given the following extracted pharmacokinetic parameters from a published paper, your job is to:
1. Assign values to each PBPK model input parameter listed below.
2. Choose the model type (1=Fractional %BW/%QCC, 2=Absolute L/L/h, 3=Mechanistic Peff/Rgut) based on available data.
3. For parameters not directly available, use standard physiological reference values.
4. Provide a source rationale for each parameter assignment.

PAPER: {paper_title}
PAPER_ID: {paper_id}

EXTRACTED PARAMETERS FROM DATABASE:
{param_block}

Return ONLY valid JSON matching EXACTLY this schema (no prose, no markdown fences):
{{
  "compound": "<drug name>",
  "species": "<human|rat|mouse>",
  "model_type": <1|2|3>,
  "model_description": "<brief description>",
  "route": "<oral|iv|sc>",
  "dose": <dose value as number mg/kg>,
  "t_end": <simulation end time in hours>,
  "parameters": {{
    "BW":       {{ "value": <number>, "unit": "kg",            "source": "<extracted|estimated|physiological_default>" }},
    "QCC":      {{ "value": <number>, "unit": "L/h/kg",        "source": "<...>" }},
    "Qliver":   {{ "value": <number>, "unit": "%",             "source": "<...>" }},
    "Vliver":   {{ "value": <number>, "unit": "%BW",           "source": "<...>" }},
    "V_plasma": {{ "value": <number>, "unit": "%BW",           "source": "<...>" }},
    "Kp_liver": {{ "value": <number>, "unit": "dimensionless", "source": "<...>" }},
    "CL_hep":   {{ "value": <number>, "unit": "L/h",           "source": "<...>" }},
    "k_a":      {{ "value": <number>, "unit": "1/h",           "source": "<...>" }}
  }},
  "assignment_notes": "<overall explanation of assignment choices>"
}}"""

    # ── 4. Call Ollama ────────────────────────────────────────────────────────
    staged = None
    llm_error = None
    ollama_model = os.environ.get("OLLAMA_MODEL_ID", "qwen2.5:1.5b")
    try:
        import ollama as _ollama
        ollama_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        client = _ollama.Client(host=ollama_url)
        resp = client.chat(
            model=ollama_model,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0.0, 
                "num_ctx": 4096,
                "chat_template_kwargs": {"enable_thinking": True, "reasoning_effort": "low"}
            },
            keep_alive="60m",
        )
        raw = resp["message"]["content"].strip()
        raw = _re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=_re.DOTALL).strip()
        json_match = _re.search(r"(\{.*\})", raw, flags=_re.DOTALL)
        if json_match:
            raw = json_match.group(1)
        staged = json.loads(raw)

        # Normalize parameters dict in case small LLM returned raw numbers
        default_units = {
            "BW": "kg", "QCC": "L/h/kg", "Qliver": "%", "Vliver": "%BW",
            "V_plasma": "%BW", "Kp_liver": "dimensionless", "CL_hep": "L/h", "k_a": "1/h"
        }
        if isinstance(staged.get("parameters"), dict):
            for k, val in list(staged["parameters"].items()):
                if isinstance(val, (int, float, str)):
                    try:
                        num_val = float(val)
                    except Exception:
                        num_val = 0.0
                    staged["parameters"][k] = {
                        "value": num_val,
                        "unit": default_units.get(k, ""),
                        "source": "llm_assigned"
                    }
    except Exception as e:
        llm_error = str(e)

    # ── 5. Deterministic fallback ─────────────────────────────────────────────
    if staged is None:
        staged = {
            "compound": "Unknown",
            "species":  "human",
            "model_type": 1,
            "model_description": "Fractional Scaling (%BW and %QCC) — using physiological defaults",
            "route": "oral",
            "dose": 50.0,
            "t_end": 24.0,
            "parameters": {
                "BW":       {"value": 70.0,  "unit": "kg",            "source": "physiological_default"},
                "QCC":      {"value": 15.0,  "unit": "L/h/kg",        "source": "physiological_default"},
                "Qliver":   {"value": 25.0,  "unit": "%",             "source": "physiological_default"},
                "Vliver":   {"value": 2.6,   "unit": "%BW",           "source": "physiological_default"},
                "V_plasma": {"value": 4.3,   "unit": "%BW",           "source": "physiological_default"},
                "Kp_liver": {"value": 1.2,   "unit": "dimensionless", "source": "physiological_default"},
                "CL_hep":   {"value": 45.0,  "unit": "L/h",           "source": "physiological_default"},
                "k_a":      {"value": 1.5,   "unit": "1/h",           "source": "physiological_default"},
            },
            "assignment_notes": "LLM assignment was unavailable. Standard human physiological defaults applied."
        }
        staged["llm_error"] = llm_error

    staged["paper_id"]    = paper_id
    staged["paper_title"] = paper_title
    staged["param_count"] = len(params_rows)

    # ── 6. Persist staged JSON ────────────────────────────────────────────────
    safe_slug    = _re.sub(r"[^a-zA-Z0-9_-]", "_", paper_id)[:60]
    staging_path = PIPELINE_OUTPUT / f"staging_{safe_slug}.json"
    with open(staging_path, "w") as f_out:
        json.dump(staged, f_out, indent=2)

    return jsonify({"success": True, "staged": staged, "staging_file": staging_path.name})


@app.route("/api/model/staging/<path:paper_id>", methods=["GET"])
def get_staging(paper_id):
    """Return the last saved staging config for a paper."""
    safe_slug    = __import__("re").sub(r"[^a-zA-Z0-9_-]", "_", paper_id)[:60]
    staging_path = PIPELINE_OUTPUT / f"staging_{safe_slug}.json"
    if not staging_path.exists():
        return jsonify({"error": "No staged config found. Please click Create R Model first."}), 404
    import json
    with open(staging_path) as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/api/model/execute", methods=["POST"])
def model_execute():
    """Execute the PBPK R simulation from staged (and possibly edited) parameters."""
    import json, base64, subprocess as _sp
    data   = request.get_json(force=True)
    staged = data.get("staged")
    if not staged:
        return jsonify({"error": "No staged parameters provided"}), 400

    paper_id  = staged.get("paper_id", "unknown")
    compound  = staged.get("compound", "Compound")
    safe_slug = __import__("re").sub(r"[^a-zA-Z0-9_-]", "_", paper_id)[:50]

    # Flatten parameters to numeric values for R solver
    flat_params = {}
    for k, v in staged.get("parameters", {}).items():
        flat_params[k] = v.get("value") if isinstance(v, dict) else v

    r_input = {
        "compound":          compound,
        "model_type":        staged.get("model_type", 1),
        "model_description": staged.get("model_description", ""),
        "dose":              staged.get("dose", 50.0),
        "route":             staged.get("route", "oral"),
        "t_end":             staged.get("t_end", 24.0),
        "parameters":        flat_params,
    }

    input_json_path = f"/tmp/pbpk_execute_{safe_slug}.json"
    output_prefix   = str(PIPELINE_OUTPUT / f"model_{safe_slug}")

    with open(input_json_path, "w") as f:
        json.dump(r_input, f, indent=2)

    r_script = PROJECT_ROOT / "pk_pbpk_extractor" / "pbpk_model_r" / "pbpk_solver.R"
    if not r_script.exists():
        return jsonify({"error": f"pbpk_solver.R not found at {r_script}"}), 500

    try:
        result = _sp.run(
            ["Rscript", str(r_script), input_json_path, output_prefix],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            return jsonify({
                "error":  "R simulation failed",
                "stderr": result.stderr[-3000:],
                "stdout": result.stdout[-2000:],
            }), 500
    except _sp.TimeoutExpired:
        return jsonify({"error": "R simulation timed out (>120 s)"}), 500
    except FileNotFoundError:
        return jsonify({"error": "Rscript not found — please install R on this machine"}), 500

    metrics  = {}
    plot_b64 = None

    metrics_path = output_prefix + "_metrics.json"
    if os.path.exists(metrics_path):
        with open(metrics_path) as f:
            metrics = json.load(f)

    plot_path = output_prefix + "_plot.png"
    if os.path.exists(plot_path):
        with open(plot_path, "rb") as f:
            plot_b64 = base64.b64encode(f.read()).decode("utf-8")

    r_code = (
        f"# PBPK Simulation — Generated by APEX-PBPK\n"
        f"# Paper: {staged.get('paper_title', paper_id)}\n"
        f"# Compound: {compound} | Route: {staged.get('route')} | Dose: {staged.get('dose')} mg/kg\n"
        f"# Model Type: {staged.get('model_type')} — {staged.get('model_description')}\n\n"
        f"library(deSolve); library(jsonlite); library(ggplot2)\n"
        f"# Run: Rscript pbpk_solver.R {input_json_path} {output_prefix}\n"
    )

    return jsonify({
        "success":  True,
        "metrics":  metrics,
        "plot_b64": plot_b64,
        "r_code":   r_code,
        "stdout":   result.stdout,
    })

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  APEX-PBPK Web Dashboard")
    print("  http://localhost:5000")
    print("=" * 60 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
