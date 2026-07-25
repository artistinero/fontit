#!/usr/bin/env python3
"""Luo vapaat-kansio symlinkeillä vapaista fonteista ja fontconfig-sääntö."""
import csv
from pathlib import Path

FONTS_BASE = Path.home() / ".local/share/fonts"
CSV = Path.home() / "fontit-metadata.csv"
VAPAAT_DIR = FONTS_BASE / "vapaat"
FONTCONFIG_DIR = Path.home() / ".config/fontconfig/conf.d"
FONTCONFIG_FILE = FONTCONFIG_DIR / "99-vain-vapaat.conf"

VAPAAT_LISENSSIT = {"OFL", "Apache", "GPL", "PublicDomain", "Freeware"}

def main():
    VAPAAT_DIR.mkdir(parents=True, exist_ok=True)
    FONTCONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Poista vanhat symlinkit
    for f in VAPAAT_DIR.iterdir():
        if f.is_symlink():
            f.unlink()

    laskuri = {"ok": 0, "puuttuu": 0}
    with open(CSV, newline="", encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            if row["category"].strip() not in VAPAAT_LISENSSIT:
                continue
            lahde = FONTS_BASE / row["path"].strip()
            if not lahde.exists():
                laskuri["puuttuu"] += 1
                continue
            kohde = VAPAAT_DIR / lahde.name
            # Jos saman niminen tiedosto useammasta kansiosta, lisää etuliite
            if kohde.exists() or kohde.is_symlink():
                kohde = VAPAAT_DIR / f"{lahde.parent.name}_{lahde.name}"
            kohde.symlink_to(lahde)
            laskuri["ok"] += 1

    print(f"Symlinkit: {laskuri['ok']} luotu, {laskuri['puuttuu']} puuttuu levyltä")

    # Fontconfig-sääntö: hylkää Fonts/-kansio, vapaat/-kansio jää näkyviin
    fontconfig_xml = f"""<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <!-- Hylkää kaikki fontit suuresta kokoelmasta -->
  <selectfont>
    <rejectfont>
      <glob>{FONTS_BASE}/Fonts</glob>
    </rejectfont>
  </selectfont>
</fontconfig>
"""
    FONTCONFIG_FILE.write_text(fontconfig_xml)
    print(f"Fontconfig-sääntö: {FONTCONFIG_FILE}")
    print(f"\nValmis! Aja seuraavaksi: fc-cache -f")
    print(f"Vapaita fontteja näkyvissä: {laskuri['ok']}")

if __name__ == "__main__":
    main()
