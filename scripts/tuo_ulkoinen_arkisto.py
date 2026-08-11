#!/usr/bin/env python3
"""Tuo ulkoisesta fonttiarkistosta (esim. vanha varmuuskopio) paikallisesta
kokoelmasta puuttuvat TTF/OTF-fontit oikeaan Fonts/<KIRJAIN>/-kansioon.

Vertailu tehdään pelkän tiedostonimen perusteella (Python set-erotuksella,
EI shellin comm-komennolla — comm antoi tässä käytössä vääriä positiivisia
LC_ALL=C-lokaalista huolimatta muutamalle täysin ASCII-nimiselle tiedostolle).

Aja tämän jälkeen: lue_lisenssit.py, luo_vapaat_symlinkit.py, fc-cache -f.
"""
import shutil
import sys
from pathlib import Path

LOCAL_FONTS = Path.home() / ".local/share/fonts/Fonts"


def kohdekansio(nimi: str) -> str:
    c = nimi[0].upper()
    return c if "A" <= c <= "Z" else "#"


def main(source_dir: Path):
    if not source_dir.is_dir():
        sys.exit(f"Lähdehakemistoa ei löydy: {source_dir}")

    lahde_polut = [
        p for p in source_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in (".ttf", ".otf")
    ]
    paikalliset_nimet = {
        p.name for p in LOCAL_FONTS.rglob("*")
        if p.is_file() and p.suffix.lower() in (".ttf", ".otf")
    }

    # nimi -> ensimmäinen löydetty lähdepolku (jos useita, ensimmäinen voittaa)
    by_name = {}
    for p in lahde_polut:
        by_name.setdefault(p.name, p)

    puuttuvat = set(by_name) - paikalliset_nimet

    kopioitu, ohitettu = 0, 0
    for nimi in sorted(puuttuvat):
        src = by_name[nimi]
        dest_dir = LOCAL_FONTS / kohdekansio(nimi)
        dest = dest_dir / nimi
        if dest.exists():
            ohitettu += 1
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        kopioitu += 1

    print(f"Lähteessä fontteja: {len(lahde_polut)}")
    print(f"Kopioitu uusia: {kopioitu}")
    print(f"Ohitettu (kohde oli jo olemassa): {ohitettu}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"Käyttö: {sys.argv[0]} <lähdehakemisto>")
    main(Path(sys.argv[1]))
