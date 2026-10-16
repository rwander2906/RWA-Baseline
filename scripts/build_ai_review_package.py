#!/usr/bin/env python3
import argparse,json,re
from pathlib import Path

def issue_number_from_text(text):
    match=re.search(r"(?:Refs|Closes|Fixes)\s+#(\d+)",text or "",re.I); return int(match.group(1)) if match else None

def acceptance_criteria(body):
    result=[]; active=False
    for raw in (body or "").splitlines():
        line=raw.strip()
        if line.startswith("#"):
            active="akzept" in line.lower() or "acceptance" in line.lower(); continue
        if active and re.match(r"^[-*]\s+",line): result.append(re.sub(r"^[-*]\s+","",line))
    return result

def review_dialog(comments, limit=20):
    items=[]
    for comment in comments or []:
        body=comment.get("body") or ""
        author=(comment.get("user") or {}).get("login","")
        if not body.strip(): continue
        if author.endswith("[bot]") and "<!-- rwa-ai-review -->" not in body: continue
        items.append({"author":author,"body":body[:6000],"created_at":comment.get("created_at","")})
    return items[-limit:]

def build(event,issue,diff,rules,context,dialog=None):
    pr=event["pull_request"]
    return {"schema_version":"1.0","pull_request":{"number":pr["number"],"head_sha":pr["head"]["sha"],"base_ref":pr["base"]["ref"]},"issue":{"number":issue["number"],"title":issue["title"],"body":issue.get("body") or "","acceptance_criteria":acceptance_criteria(issue.get("body"))},"diff":diff,"baseline_rules":rules,"project_context":context,"review_dialog":review_dialog(dialog or [])}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--event",type=Path,required=True); p.add_argument("--issue",type=Path,required=True); p.add_argument("--diff",type=Path,required=True); p.add_argument("--rules",type=Path,required=True); p.add_argument("--context",type=Path,action="append",default=[]); p.add_argument("--dialog",type=Path); p.add_argument("--output",type=Path,required=True); a=p.parse_args()
    event=json.loads(a.event.read_text()); issue=json.loads(a.issue.read_text()); rules=json.loads(a.rules.read_text()); context=[{"path":str(x),"content":x.read_text(encoding="utf-8")} for x in a.context if x.exists()]; dialog=json.loads(a.dialog.read_text()) if a.dialog and a.dialog.exists() else []
    a.output.write_text(json.dumps(build(event,issue,a.diff.read_text(encoding="utf-8"),rules,context,dialog),indent=2)+"\n")
if __name__=="__main__": main()
