#!/usr/bin/env python3
"""Lataa kuratoidut Google Fonts -fontit GitHub API:n kautta. Kaikki OFL/Apache = vapaat."""
import urllib.request, urllib.error, json, os, time
from pathlib import Path

TARGET = Path.home() / ".local/share/fonts/Fonts"
HEADERS = {"User-Agent": "font-downloader/1.0"}

# (hakemistonimi repossa, kuvaus)
FONTS = [
    # Stencil / military
    ("stardosstencil",       "Stardos Stencil — selkeä stencil"),
    ("sirinstencil",         "Sirin Stencil — koristeellinen stencil"),
    ("wallpoet",             "Wallpoet — graffiti/stencil"),
    ("squadaone",            "Squada One — tekninen/sotilas"),
    ("trochut",              "Trochut — art deco stencil"),
    # Gothic / blackletter / medieval
    ("unifrakturmaguntia",   "UnifrakturMaguntia — goottilainen fraktuura"),
    ("uncialantiqua",        "Uncial Antiqua — kelttiläinen"),
    ("cinzeldecorative",     "Cinzel Decorative — antiikin koristelu"),
    ("cinzel",               "Cinzel — roomalainen antiikki"),
    ("metalmania",           "Metal Mania — heavy metal"),
    ("newrocker",            "New Rocker — rock/goottilainen"),
    # Horror / dark / spooky
    ("creepster",            "Creepster — kauhuelokuvatyyli"),
    ("eater",                "Eater — kauhumainen"),
    ("vampiroone",           "Vampiro One — vampyyri"),
    ("pirataone",            "Pirata One — merirosvo"),
    # Comic / fun / cartoon
    ("bangers",              "Bangers — sarjakuva/comics"),
    ("boogaloo",             "Boogaloo — hauska pyöreä"),
    ("luckiestguy",          "Luckiest Guy — retro-mainosfontti"),
    ("titanone",             "Titan One — lihavoitu display"),
    ("comicneue",            "Comic Neue — parannettu Comic Sans"),
    ("kranky",               "Kranky — outo/epäsiisti"),
    ("slackey",              "Slackey — hauska lihavoitu"),
    ("chewy",                "Chewy — pyöreä ja pehmeä"),
    ("fredoka",              "Fredoka — ystävällinen pyöreä"),
    ("boogaloo",             ""),  # duplicate, skip
    # Weird / Rubik-erikoisversiot
    ("rubikbeastly",         "Rubik Beastly — hirviömäinen"),
    ("rubikburned",          "Rubik Burned — poltettu"),
    ("rubikdirt",            "Rubik Dirt — mudanmuotoinen"),
    ("rubikglitch",          "Rubik Glitch — glitch-efekti"),
    ("rubikmicrobe",         "Rubik Microbe — mikrobi-muoto"),
    ("rubikmoonrocks",       "Rubik Moonrocks — kuukivi"),
    ("rubikpuddles",         "Rubik Puddles — vesipisarat"),
    ("rubikscribble",        "Rubik Scribble — tahriintunut"),
    ("rubikwetpaint",        "Rubik Wet Paint — märkä maali"),
    # Retro / vintage / western
    ("rye",                  "Rye — villi länsi"),
    ("peralta",              "Peralta — western retro"),
    ("ranchers",             "Ranchers — karjanhoitaja"),
    ("sancreek",             "Sancreek — frontier/western"),
    ("tradewinds",           "Trade Winds — trooppinen/eksoottinen"),
    ("vt323",                "VT323 — retro terminaali/pikselit"),
    ("pressstart2p",         "Press Start 2P — retropeli pikselit"),
    ("specialelite",         "Special Elite — kirjoituskone vintage"),
    ("monoton",              "Monoton — retro neon"),
    ("bungee",               "Bungee — urbaani retro"),
    ("bungee shade",         ""),  # skip - space
    ("bungeeshade",          "Bungee Shade — varjostettu retro"),
    ("bungeeoutline",        "Bungee Outline — kontuuri retro"),
    # Artistic / decorative / display
    ("frederickathegreat",   "Fredericka the Great — koristeltu serif"),
    ("lobster",              "Lobster — bold script"),
    ("lobstertwo",           "Lobster Two — laajempi lobster"),
    ("poiretone",            "Poiret One — art deco"),
    ("risque",               "Risque — art nouveau"),
    ("spirax",               "Spirax — art nouveau"),
    ("novacut",              "Nova Cut — geometrinen koristelu"),
    ("novaflat",             "Nova Flat — litteä geometrinen"),
    ("novaoval",             "Nova Oval — ovaali"),
    ("novascript",           "Nova Script — koristekäsiala"),
    ("novamono",             "Nova Mono — geometrinen monospace"),
    ("novaround",            "Nova Round — pyöristetty"),
    ("novaslim",             "Nova Slim — ohut geometrinen"),
    ("novasquare",           "Nova Square — neliöllinen"),
    ("vastsha dow",          ""),  # skip - space in name
    ("cinzel",               ""),  # duplicate
    ("mysteryquest",         "Mystery Quest — mystinen"),
    ("lacquer",              "Lacquer — valuva maali"),
    ("seaweedscript",        "Seaweed Script — merilevy"),
    ("lilyscriptone",        "Lily Script One — tyylitelty"),
    ("righteous",            "Righteous — retro display"),
    ("abrilFatface",         ""),  # skip - bad case
    ("abrilfatface",         "Abril Fatface — lihavoitu display"),
    ("ultra",                "Ultra — erittäin lihavoitu"),
    ("gravitas one",         ""),  # skip
    ("gravitasone",          "Gravitas One — painava display"),
    ("bowlbyone",            "Bowlby One — bold comic"),
    ("bowlbyonesc",          "Bowlby One SC — small caps versio"),
    ("fugaz one",            ""),  # skip
    ("fugazone",             "Fugaz One — italic display"),
    ("limelight",            "Limelight — art deco 1920s"),
    ("diplomata",            "Diplomata — koristeltu serif"),
    ("diplomatesc",          "Diplomata SC — small caps"),
    # Handwriting / brush / ink
    ("permanentmarker",      "Permanent Marker — tussikynä"),
    ("rocksalt",             "Rock Salt — grunge käsiala"),
    ("kaushanscript",        "Kaushan Script — sivellinkäsiala"),
    ("satisfy",              "Satisfy — tyylikäs käsiala"),
    ("tangerine",            "Tangerine — kalligrafia ohut"),
    ("sacramento",           "Sacramento — kalligrafia"),
    ("gloriahallelujah",     "Gloria Hallelujah — lapsekas"),
    ("caveat",               "Caveat — pikakirjoitus"),
    ("pacifico",             "Pacifico — surffari/pyöreä"),
    ("architectsdaughter",   "Architects Daughter — käsinpiirretty"),
    ("homemadeapple",        "Homemade Apple — kotitekoinen"),
    ("reenie beanie",        ""),  # skip
    ("reeniebeanie",         "Reenie Beanie — epäsiisti käsiala"),
    ("waitingforthesunrise", "Waiting for the Sunrise — hauras käsiala"),
    ("swankyandmoomoo",      "Swanky and Moo Moo — leikkisä"),
    ("rockSalt",             ""),  # duplicate
    # Futuristic / sci-fi / tech
    ("orbitron",             "Orbitron — sci-fi futuristinen"),
    ("turretroad",           "Turret Road — tech/sotilas"),
    ("syncopate",            "Syncopate — geometrinen display"),
    ("iceland",              "Iceland — jäinen geometrinen"),
    ("audiowide",            "Audiowide — tekninen display"),
    ("blinkone",             "Blink One — futuristinen"),
    ("nexaalternate",        ""),  # probably not in GF
    # Grunge / rough / textured
    ("griffy",               "Griffy — rosoinen/karkea"),
    ("rubikdistressed",      "Rubik Distressed — kulunut"),
    # Miscellaneous fun
    ("zentokyozoo",          "Zen Tokyo Zoo — japanilainen eläinpuisto"),
    ("rubikgemstones",       "Rubik Gemstones — jalokivi"),
    ("rubikice",             "Rubik Ice — jäinen"),
    ("rubikstorm",           "Rubik Storm — myrskyinen"),
    ("rubikvinyl",           "Rubik Vinyl — vinyyli"),
    ("rubikspray paint",     ""),  # skip
    ("rubikspraypaint",      "Rubik Spray Paint — spraymaali"),
    ("stalinistone",         "Stalinist One — neuvostotyyli"),
    ("warnes",               "Warnes — retro display"),
    ("ribeye",               "Ribeye — rustiikki lihavoitu"),
    ("ribeyemarbled",        "Ribeye Marbled — marmorinen"),
    ("rum raisin",           ""),  # skip
    ("rumraisin",            "Rum Raisin — koristebold"),
    ("sonsieone",            "Sonsie One — funky display"),
    ("kavoon",               "Kavoon — leikkisä display"),
    ("skranji",              "Skranji — riimumainen"),
    ("paprika",              "Paprika — eksoottinen display"),
    ("fenix",                "Fenix — slab serif display"),
    ("artifika",             "Artifika — koristeltu serif"),
]

def api_list(fontdir):
    url = f"https://api.github.com/repos/google/fonts/contents/ofl/{fontdir}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except:
        return None

def download_file(raw_url, dest_path):
    req = urllib.request.Request(raw_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            dest_path.write_bytes(r.read())
        return True
    except Exception as e:
        return False

# Poista duplikaatit ja tyhjät kuvaukset
seen = set()
fonts_clean = []
for d, desc in FONTS:
    if desc and d not in seen:
        seen.add(d)
        fonts_clean.append((d, desc))

print(f"Ladataan {len(fonts_clean)} fonttiperhettä Google Fonts GitHub:sta...")
print("Kaikki fontit ovat OFL tai Apache-lisenssillä (vapaa kaupalliseen käyttöön)\n")

ok, skip_list, fail_list = [], [], []

for fontdir, desc in fonts_clean:
    files = api_list(fontdir)
    if not files or isinstance(files, dict):
        # Ei löydy OFL-hakemistosta, yritetään Apache-hakemistoa
        url2 = f"https://api.github.com/repos/google/fonts/contents/apache/{fontdir}"
        req = urllib.request.Request(url2, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                files = json.loads(r.read())
        except:
            files = None

    if not files:
        print(f"  --    {fontdir} (ei löydy reposta)")
        skip_list.append(fontdir)
        time.sleep(0.3)
        continue

    ttf_files = [f for f in files if isinstance(f, dict) and f.get("name","").endswith(".ttf")]
    if not ttf_files:
        print(f"  --    {fontdir} (ei TTF-tiedostoja)")
        skip_list.append(fontdir)
        continue

    letter = fontdir[0].upper()
    dest_dir = TARGET / letter
    dest_dir.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    for tf in ttf_files:
        dest = dest_dir / tf["name"]
        if dest.exists():
            downloaded += 1
            continue
        if download_file(tf["download_url"], dest):
            downloaded += 1
        time.sleep(0.15)

    print(f"  OK    {desc} ({downloaded} tiedostoa)")
    ok.append(fontdir)
    time.sleep(0.4)

print(f"\n=== VALMIS ===")
print(f"Ladattu onnistuneesti: {len(ok)} fonttiperhe")
print(f"Ei löytynyt reposta:   {len(skip_list)}")
if skip_list:
    print("  Ohitetut:", ", ".join(skip_list[:10]))
