#!/usr/bin/env python3
import sys
import json
import csv

def clean_json(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    seen = set()
    cleaned = []
    for row in data:
        key = json.dumps(row, sort_keys=True)
        if key in seen or not row:
            continue
        seen.add(key)
        cleaned.append(row)
    out = path.replace(".json", ".clean.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print(f"{len(data)} -> {len(cleaned)} lignes. Écrit dans {out}")

def clean_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    header, body = rows[0], rows[1:]
    seen = set()
    cleaned = []
    for row in body:
        key = tuple(row)
        if key in seen or not any(cell.strip() for cell in row):
            continue
        seen.add(key)
        cleaned.append(row)
    out = path.replace(".csv", ".clean.csv")
    with open(out, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(cleaned)
    print(f"{len(body)} -> {len(cleaned)} lignes. Écrit dans {out}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python clean.py <fichier.json|.csv>")
    path = sys.argv[1]
    if path.endswith(".json"):
        clean_json(path)
    elif path.endswith(".csv"):
        clean_csv(path)
    else:
        sys.exit("Format non supporté (attendu: .json ou .csv)")
