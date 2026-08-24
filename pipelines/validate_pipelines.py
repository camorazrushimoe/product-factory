#!/usr/bin/env python3
"""Pipeline gate validator — every post-intake stage must pass discovery-gate.

Usage: python3 validate_pipelines.py [pipelines_dir]

Checks, for each *.yaml pipeline:
  1. a `discovery-gate` stage exists with `human_gate: true` and `required: true`
  2. the gate depends on an intake root stage
  3. EVERY other stage (except the intake root) transitively depends on the
     gate — i.e. no execution path may skip the operator checkpoint.

Exit code 0 = all pipelines clean; 1 = violations found.
"""
import sys
import glob
import os

import yaml

GATE = "discovery-gate"
ROOTS = {"intake", "intake-and-frame"}


def gated(stages: dict, name: str, seen=frozenset()) -> bool:
    """True if stage `name` transitively depends on the gate."""
    if name == GATE:
        return True
    if name in seen:
        return False
    deps = stages[name].get("depends_on") or []
    if not deps:
        return False
    return all(gated(stages, d, seen | {name}) for d in deps)


def validate(path: str) -> list[str]:
    problems = []
    doc = yaml.safe_load(open(path))
    stages = {s["name"]: s for s in doc.get("stages", [])}

    gate = stages.get(GATE)
    if gate is None:
        return [f"{path}: no {GATE} stage"]
    if gate.get("human_gate") is not True:
        problems.append(f"{path}: {GATE} missing human_gate: true")
    if gate.get("required") is not True:
        problems.append(f"{path}: {GATE} missing required: true")
    if not any(d in ROOTS for d in (gate.get("depends_on") or [])):
        problems.append(f"{path}: {GATE} does not depend on an intake root")

    for name in stages:
        if name in ROOTS:
            continue
        if not gated(stages, name):
            problems.append(f"{path}: stage '{name}' can bypass {GATE}")
    return problems


def main() -> int:
    pipelines = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)))
    files = sorted(glob.glob(os.path.join(pipelines, "*.yaml")))
    if not files:
        print(f"no yaml pipelines found in {pipelines}")
        return 1
    all_problems = []
    for f in files:
        all_problems.extend(validate(f))
        print(f"checked: {f}")
    if all_problems:
        print("\nVIOLATIONS:")
        for p in all_problems:
            print(" -", p)
        return 1
    print("\nALL PIPELINES CLEAN: every stage is behind the discovery gate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
