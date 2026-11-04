#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json

total = 0.0
count = 0
lts   = {}

with open("payments.jsonl") as f:
    for line in f:
        try:
           event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or not event.get("txn_id"):
            continue
        txn = event["txn_id"]
        if txn not in lts or event["ts"] >= lts[txn]["ts"]:
            lts[txn] = event

for event in lts.values():
    if event["status"] == "success":
        total += float(str(event["amount"]).replace(",", ""))
        count += 1

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
