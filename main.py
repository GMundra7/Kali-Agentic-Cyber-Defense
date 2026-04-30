from fastapi import FastAPI
from pydantic import BaseModel

from app.llm import plan_tasks, summarize_results
from app.validator import validate_plan
from app.executor import run_command
from app.zap import run_zap_scan

app = FastAPI()


# ===== REQUEST SCHEMA =====
class ScanRequest(BaseModel):
    input: str


@app.post("/scan")
def scan(req: ScanRequest):

    plan = plan_tasks(req.input)

    if isinstance(plan, dict) and "error" in plan:
        return {"error": plan}

    ok, msg = validate_plan(plan)
    if not ok:
        return {"error": msg, "plan": plan}

    results = {}

    for item in plan:
        tool = item["tool"]
        args = item["args"]

         if tool == "nmap":
            results["nmap"] = run_command(args)

        elif tool == "gobuster":
            results["gobuster"] = run_command(args)

        elif tool == "zap":
            results["zap"] = run_zap_scan(args)

    # ===== NORMALIZE ZAP OUTPUT =====
    zap_result = results.get("zap", [])
    if isinstance(zap_result, str):
        zap_result = [{"message": zap_result}]

    # ===== SUMMARY =====
    summary = summarize_results(
        nmap_output=results.get("nmap", ""),
        gobuster_output=results.get("gobuster", ""),
        zap_alerts=zap_result
    )

    return {
        "plan": plan,
        "results": results,
        "summary": summary
    }