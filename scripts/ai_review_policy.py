#!/usr/bin/env python3
import argparse,json
from pathlib import Path

VALID_MODES={"advisory","required"}
VALID_OUTAGE={"fail-open","fail-closed"}

def decide(executions,mode="advisory",outage="fail-open",human_on_disagreement=True):
    if mode not in VALID_MODES: raise ValueError("invalid review mode")
    if outage not in VALID_OUTAGE: raise ValueError("invalid outage policy")
    unavailable=[x for x in executions if x.get("status")!="REVIEWED"]
    reviewed=[x["result"] for x in executions if x.get("status")=="REVIEWED"]
    verdicts={x["verdict"] for x in reviewed}
    if unavailable and outage=="fail-closed":
        return {"decision":"BLOCK","reason":"provider-unavailable","human_required":False}
    if human_on_disagreement and "BLOCK" in verdicts and ("PASS" in verdicts or "WARN" in verdicts):
        return {"decision":"HUMAN_REQUIRED","reason":"reviewer-disagreement","human_required":True}
    if "BLOCK" in verdicts:
        return {"decision":"BLOCK","reason":"review-block","human_required":False}
    if mode=="required" and not reviewed:
        return {"decision":"BLOCK","reason":"required-review-missing","human_required":False}
    if "WARN" in verdicts:
        return {"decision":"WARN","reason":"review-warning","human_required":False}
    if unavailable:
        return {"decision":"WARN","reason":"provider-unavailable-fail-open","human_required":False}
    return {"decision":"PASS","reason":"reviews-passed","human_required":False}

def main():
    p=argparse.ArgumentParser(); p.add_argument("results",type=Path,nargs="+"); p.add_argument("--mode",choices=sorted(VALID_MODES),default="advisory"); p.add_argument("--outage",choices=sorted(VALID_OUTAGE),default="fail-open"); p.add_argument("--allow-disagreement",action="store_true"); p.add_argument("--output",type=Path,default=Path("ai-review-decision.json")); a=p.parse_args()
    executions=[json.loads(x.read_text()) for x in a.results]; result=decide(executions,a.mode,a.outage,not a.allow_disagreement); a.output.write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result)); return 1 if result["decision"] in {"BLOCK","HUMAN_REQUIRED"} else 0
if __name__=="__main__": raise SystemExit(main())
