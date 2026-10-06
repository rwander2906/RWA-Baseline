#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

class ProviderUnavailable(RuntimeError):
    pass

class ReviewProvider:
    def review(self, package, model):
        raise NotImplementedError

class FakeProvider(ReviewProvider):
    def review(self, package, model):
        return {"schema_version":"1.0","verdict":"PASS","summary":"Fake review passed.","findings":[],"reviewer":{"adapter":"fake","model":model,"provider_review_id":None}}

def create_provider(name):
    if name == "fake":
        return FakeProvider()
    raise ValueError(f"unknown AI review provider: {name}")

def run(package, provider_name, model):
    try:
        result = create_provider(provider_name).review(package, model)
    except ProviderUnavailable as exc:
        return "UNAVAILABLE", {"error": str(exc)}
    return "REVIEWED", result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("package",type=Path)
    parser.add_argument("--provider",required=True)
    parser.add_argument("--model",required=True)
    parser.add_argument("--output",type=Path,default=Path("ai-review-result.json"))
    args=parser.parse_args()
    status,result=run(json.loads(args.package.read_text(encoding="utf-8")),args.provider,args.model)
    args.output.write_text(json.dumps({"status":status,"result":result},indent=2)+"\n",encoding="utf-8")
    return 0 if status=="REVIEWED" else 3

if __name__=="__main__":
    raise SystemExit(main())
