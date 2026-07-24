#!/usr/bin/env python3
import sys, os, csv
from pathlib import Path
from fontTools.ttLib import TTFont

FONT_DIR = Path.home() / ".local/share/fonts"
OUTPUT = Path.home() / "fontit-metadata.csv"

NAME_IDS = {0: "copyright", 4: "full_name", 9: "designer", 13: "license", 14: "license_url"}

def get_name(table, name_id):
    try:
        record = table.getName(name_id, 3, 1, 0x0409) or \
                 table.getName(name_id, 1, 0, 0) or \
                 table.getName(name_id, 3, 1)
        if record:
            return record.toUnicode().replace("\n", " ").strip()
    except:
        pass
    return ""

def classify(license_text, copyright_text):
    combined = (license_text + " " + copyright_text).lower()
    if any(x in combined for x in ["sil open font", "open font license", "ofl"]):
        return "OFL"
    if "apache" in combined:
        return "Apache"
    if "public domain" in combined:
        return "PublicDomain"
    if "gnu general public" in combined or " gpl" in combined:
        return "GPL"
    if "creative commons" in combined:
        if "no deriv" in combined or "nd" in combined:
            return "CC-ND (rajoitettu)"
        if "noncommercial" in combined or "nc" in combined:
            return "CC-NC (ei kaupallinen)"
        return "CC"
    if any(x in combined for x in ["free for personal", "personal use only", "non-commercial", "noncommercial"]):
        return "Freeware-NC"
    if any(x in combined for x in ["freeware", "free to use", "free for any", "free for all", "no charge"]):
        return "Freeware"
    if any(x in combined for x in ["all rights reserved", "commercial license", "purchase", "license fee", "proprietary"]):
        return "Kaupallinen"
    if combined.strip():
        return "Tuntematon-metadata"
    return "Ei-metatietoa"

fonts = list(FONT_DIR.rglob("*.ttf")) + list(FONT_DIR.rglob("*.otf")) + \
        list(FONT_DIR.rglob("*.TTF")) + list(FONT_DIR.rglob("*.OTF"))

print(f"Käsitellään {len(fonts)} fonttia...", flush=True)

results = []
for i, path in enumerate(fonts):
    if i % 500 == 0:
        print(f"  {i}/{len(fonts)}...", flush=True)
    try:
        tt = TTFont(str(path), lazy=True)
        nt = tt["name"]
        full_name = get_name(nt, 4)
        copyright_ = get_name(nt, 0)
        designer = get_name(nt, 9)
        license_ = get_name(nt, 13)
        license_url = get_name(nt, 14)
        tt.close()
    except:
        full_name = copyright_ = designer = license_ = license_url = ""
    
    category = classify(license_, copyright_)
    results.append({
        "path": str(path.relative_to(FONT_DIR)),
        "full_name": full_name,
        "category": category,
        "copyright": copyright_[:120],
        "license": license_[:120],
        "license_url": license_url,
        "designer": designer,
    })

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["path","full_name","category","copyright","license","license_url","designer"])
    writer.writeheader()
    writer.writerows(results)

print(f"\nValmis! Kirjoitettu: {OUTPUT}")

from collections import Counter
cats = Counter(r["category"] for r in results)
print("\nLisenssikategoriat:")
for cat, count in cats.most_common():
    print(f"  {count:5d}  {cat}")
