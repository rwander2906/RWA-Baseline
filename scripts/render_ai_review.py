#!/usr/bin/env python3
import argparse,json
from pathlib import Path

def render(wrapper):
    status=wrapper["status"]
    if status!="REVIEWED": return "## AI Code Review\n\n**Status:** "+status+"\n"
    r=wrapper["result"]; lines=["## AI Code Review","",f"**Verdict:** {r['verdict']}","",r["summary"],""]
    for finding in r["findings"]:
        loc=finding["location"]; where=loc["path"]+(f":{loc['line']}" if loc.get("line") else "")
        lines.append(f"- **{finding['severity']}** `{where}` — {finding['message']}")
    return "\n".join(lines)+"\n"

def main():
    p=argparse.ArgumentParser(); p.add_argument("result",type=Path); p.add_argument("--summary",type=Path); a=p.parse_args(); wrapper=json.loads(a.result.read_text()); output=render(wrapper); print(output)
    if a.summary: a.summary.write_text(output)
    return 1 if wrapper.get("status")=="REVIEWED" and wrapper.get("result",{}).get("verdict")=="BLOCK" else 0
if __name__=="__main__": raise SystemExit(main())
