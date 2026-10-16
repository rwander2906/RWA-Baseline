#!/usr/bin/env python3
import argparse,json
from pathlib import Path
MARKER="<!-- rwa-ai-review -->"

def render(result,decision,run_url,sha):
    lines=[MARKER,"## AI Code Review",f"- Run: {run_url}",f"- Commit: `{sha}`"]
    if result.get("status")=="REVIEWED":
        review=result["result"]; reviewer=review.get("reviewer",{})
        lines += [f"- Reviewer: `{reviewer.get('adapter','?')}` / `{reviewer.get('model','?')}`",f"- Verdict: **{review.get('verdict')}**",f"- Policy: **{decision.get('decision')}** — {decision.get('reason')}","",review.get("summary",""),"","### Findings"]
        findings=review.get("findings",[])
        if not findings: lines.append("- Keine Findings.")
        for finding in findings:
            loc=finding.get("location",{}); where=loc.get("path","?")+(f":{loc['line']}" if loc.get("line") else "")
            lines.append(f"- **{finding.get('severity')}** `{where}` — {finding.get('message')}")
    else:
        lines += [f"- Review-Status: **{result.get('status','UNKNOWN')}**",f"- Policy: **{decision.get('decision')}** — {decision.get('reason')}"]
    return "\n".join(lines)+"\n"

def main():
    p=argparse.ArgumentParser(); p.add_argument("--result",type=Path,required=True); p.add_argument("--decision",type=Path,required=True); p.add_argument("--run-url",required=True); p.add_argument("--sha",required=True); p.add_argument("--output",type=Path,required=True); a=p.parse_args()
    a.output.write_text(render(json.loads(a.result.read_text()),json.loads(a.decision.read_text()),a.run_url,a.sha),encoding="utf-8")
if __name__=="__main__": main()
