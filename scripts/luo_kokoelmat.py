#!/usr/bin/env python3
"""Luo font-manager Collections.json lisenssikategorioittain."""
import csv, json
from pathlib import Path
from fontTools.ttLib import TTFont

CSV = Path.home() / "fontit-metadata.csv"
COLLECTIONS_JSON = Path.home() / ".config/font-manager/Collections.json"

def get_family(path_rel):
    full_path = Path.home() / ".local/share/fonts" / path_rel
    try:
        tt = TTFont(str(full_path), lazy=True)
        nt = tt["name"]
        for nid in [16, 1]:
            rec = nt.getName(nid, 3, 1, 0x0409) or nt.getName(nid, 1, 0, 0)
            if rec:
                name = rec.toUnicode().strip()
                tt.close()
                return name
        tt.close()
    except:
        pass
    return Path(path_rel).stem.replace("-", " ").replace("_", " ")

CATEGORY_LABELS = [
    ("OFL",                "Vapaa kaupallinen — OFL"),
    ("Apache",             "Vapaa kaupallinen — Apache"),
    ("GPL",                "Vapaa kaupallinen — GPL"),
    ("PublicDomain",       "Vapaa kaupallinen — Public Domain"),
    ("Freeware",           "Vapaa kaupallinen — Freeware"),
    ("Freeware-NC",        "Vain henkilokohtainen — Freeware NC"),
    ("Kaupallinen",        "Kaupallinen — ei vapaaseen kayttoon"),
    ("Tuntematon-metadata","Epaselva lisenssi — metadata olemassa"),
    ("Ei-metatietoa",      "Epaselva lisenssi — ei metatietoa"),
]

with open(CSV) as f:
    rows = list(csv.DictReader(f))

print(f"Luetaan perhenimet {len(rows)} fontille...")
cat_families = {cat: [] for cat, _ in CATEGORY_LABELS}

for i, row in enumerate(rows):
    if i % 500 == 0:
        print(f"  {i}/{len(rows)}...")
    cat = row["category"]
    if cat not in cat_families:
        continue
    family = get_family(row["path"])
    if family and family not in cat_families[cat]:
        cat_families[cat].append(family)

entries = {}
for idx, (cat, label) in enumerate(CATEGORY_LABELS):
    families = sorted(cat_families[cat])
    if not families:
        continue
    entries[label] = {
        "name": label,
        "icon": None,
        "comment": None,
        "index": idx,
        "requires-update": False,
        "active": True,
        "children": {},
        "families": families,
        "size": len(families),
    }
    print(f"  {label}: {len(families)} fonttiperhettä")

data = {"entries": entries}
COLLECTIONS_JSON.write_text(json.dumps(data, indent=4, ensure_ascii=False))
print(f"\nValmis! Kirjoitettu: {COLLECTIONS_JSON}")
print("Avaa font-manager — kokoelmat näkyvät Collections-osiossa.")
