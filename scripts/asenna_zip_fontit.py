#!/usr/bin/env python3
"""Pura ja asenna fonts/-kansion ZIP-paketit pääkokoelmaan lisenssianalyysin jälkeen."""
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from fontTools.ttLib import TTFont

FONTS_DIR = Path(__file__).parent.parent / "fonts"
INSTALL_BASE = Path.home() / ".local/share/fonts/Fonts"

RANDOM_SUFFIX_RE = re.compile(r"-[A-Za-z0-9]{4,8}(?=\.(ttf|otf)$)", re.IGNORECASE)


def info_txt_license(zf):
    try:
        data = zf.read("info.txt").decode("utf-8-sig", errors="replace")
        for line in data.splitlines():
            if line.lower().startswith("license:"):
                return line.split(":", 1)[1].strip()
    except KeyError:
        pass
    return ""


def font_metadata_license(font_path):
    try:
        tt = TTFont(str(font_path), lazy=True)
        nt = tt["name"]

        def get(nid):
            r = (nt.getName(nid, 3, 1, 0x0409) or
                 nt.getName(nid, 1, 0, 0) or
                 nt.getName(nid, 3, 1))
            return r.toUnicode().strip() if r else ""

        lic = get(13)
        copy = get(0)
        tt.close()
        return lic, copy
    except Exception:
        return "", ""


def classify_from_info(info_lic):
    s = info_lic.lower()
    if "non-commercial" in s or "noncommercial" in s or "personal" in s or "demo" in s:
        return "Freeware-NC"
    if "donation" in s:
        return "Freeware-NC"
    if "freeware" in s or "free" in s:
        return "Freeware"
    return ""


def classify_from_metadata(lic, copy):
    combined = (lic + " " + copy).lower()
    if any(x in combined for x in ["sil open font", "open font license", "ofl"]):
        return "OFL"
    if "apache" in combined:
        return "Apache"
    if "public domain" in combined:
        return "PublicDomain"
    if "gnu general public" in combined or " gpl" in combined:
        return "GPL"
    if any(x in combined for x in ["free for personal", "personal use only",
                                    "non-commercial", "noncommercial"]):
        return "Freeware-NC"
    if any(x in combined for x in ["freeware", "free to use", "free for any",
                                    "free for all", "no charge"]):
        return "Freeware"
    if any(x in combined for x in ["all rights reserved", "commercial license",
                                    "purchase", "license fee", "proprietary"]):
        return "Kaupallinen"
    if combined.strip():
        return "Tuntematon-metadata"
    return "Ei-metatietoa"


def clean_name(filename):
    return RANDOM_SUFFIX_RE.sub("", filename)


def target_dir(clean_filename):
    first = clean_filename[0].upper()
    if first.isalpha():
        return INSTALL_BASE / first
    return INSTALL_BASE / "#"


def main():
    zips = sorted(FONTS_DIR.glob("*.zip"))
    if not zips:
        print("Ei ZIP-tiedostoja fonts/-kansiossa.")
        return

    installed = []
    skipped = []

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        for zp in zips:
            with zipfile.ZipFile(zp) as zf:
                info_lic = info_txt_license(zf)
                font_names = [n for n in zf.namelist()
                              if n.lower().endswith((".ttf", ".otf"))]

                for font_name in font_names:
                    zf.extract(font_name, tmp)
                    font_path = tmp / font_name

                    meta_lic, meta_copy = font_metadata_license(font_path)

                    # Lisenssi: info.txt on luotettavampi lähde tälle kokoelmalle
                    category = classify_from_info(info_lic)
                    if not category:
                        category = classify_from_metadata(meta_lic, meta_copy)

                    clean = clean_name(Path(font_name).name)
                    dest_dir = target_dir(clean)
                    dest = dest_dir / clean

                    if dest.exists():
                        skipped.append((zp.name, font_name, "tiedosto jo olemassa"))
                        continue

                    dest_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(font_path, dest)

                    installed.append({
                        "zip": zp.name,
                        "file": clean,
                        "dest": dest,
                        "category": category,
                        "info_lic": info_lic,
                        "meta_lic": meta_lic[:60] if meta_lic else "(tyhjä)",
                        "meta_copy": meta_copy[:60] if meta_copy else "(tyhjä)",
                    })

    print(f"\n{'='*60}")
    print(f"ASENNETTU ({len(installed)} fonttia):")
    print(f"{'='*60}")
    for r in installed:
        print(f"  [{r['category']:15}] {r['file']}")
        print(f"    info.txt: {r['info_lic']}")
        print(f"    metadata: {r['meta_lic'] or '(tyhjä)'}")

    if skipped:
        print(f"\nOHITETTU ({len(skipped)}):")
        for zip_name, font_name, reason in skipped:
            print(f"  {font_name} ({zip_name}): {reason}")

    from collections import Counter
    cats = Counter(r["category"] for r in installed)
    print(f"\nLisenssijakauma:")
    for cat, count in cats.most_common():
        print(f"  {count:3d}  {cat}")

    # Poista ZIP-tiedostot
    print(f"\nPoistetaan {len(zips)} ZIP-tiedostoa fonts/-kansiosta...")
    for zp in zips:
        zp.unlink()
    print("ZIP-tiedostot poistettu.")

    print(f"\nSeuraavat vaiheet:")
    print(f"  python3 scripts/lue_lisenssit.py      # päivitä metadata CSV")
    print(f"  python3 scripts/luo_vapaat_symlinkit.py  # päivitä vapaat-symlinkit")
    print(f"  fc-cache -f                            # päivitä fontconfig-välimuisti")


if __name__ == "__main__":
    main()
