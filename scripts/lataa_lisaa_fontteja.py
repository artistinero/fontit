#!/usr/bin/env python3
"""Lataa lisää vapaita Google Fonts -fontteja. Kaikki OFL/Apache = vapaa käyttää."""
import urllib.request, urllib.error, json, os, time
from pathlib import Path

TARGET = Path.home() / ".local/share/fonts/Fonts"
HEADERS = {"User-Agent": "font-downloader/1.0"}

FONTS = [
    # === AIEMMIN EPÄONNISTUNEET — korjatut nimet ===
    ("pressstart2p",         "Press Start 2P — retropeli pikselit"),
    ("specialelite",         "Special Elite — kirjoituskone vintage"),
    ("bungee",               "Bungee — urbaani retro paksunauha"),
    ("bungeehairline",       "Bungee Hairline — ohut versio"),
    ("bungeeinline",         "Bungee Inline — sisäkontuuri"),
    ("bungeeshade",          "Bungee Shade — varjostettu"),
    ("lobster",              "Lobster — bold script"),
    ("lobstertwo",           "Lobster Two — kevyempi versio"),
    ("monoton",              "Monoton — neon retro kaksoisviiva"),
    ("frederickathegreat",   "Fredericka the Great — koristeltu serif"),
    ("poiretone",            "Poiret One — art deco geometrinen"),
    ("risque",               "Risque — art nouveau feminiininen"),
    ("spirax",               "Spirax — koristeellinen art nouveau"),
    ("novacut",              "Nova Cut — geometrinen leikkaus"),
    ("novaflat",             "Nova Flat — litteä geometrinen"),
    ("novaoval",             "Nova Oval — ovaalimuoto"),
    ("diplomatesc",          "Diplomata SC — small caps koristeltu"),
    ("ribeyemarbled",        "Ribeye Marbled — marmorinen lihavoitu"),
    ("rumraisin",            "Rum Raisin — koristebold"),
    ("sonsieone",            "Sonsie One — funky pyöreä display"),
    ("kavoon",               "Kavoon — leikkisä display"),
    ("skranji",              "Skranji — riimumainen"),
    ("paprika",              "Paprika — eksoottinen lohkottu"),
    ("fenix",                "Fenix — tyylikäs slab serif"),
    ("artifika",             "Artifika — koristeltu serif"),
    # === PIXEL / RETRO GAME ===
    ("silkscreen",           "Silkscreen — bitmap pixel fontti"),
    ("pixelifysans",         "Pixelify Sans — moderni pixel"),
    ("tiny5",                "Tiny5 — minimaalinen pixel"),
    ("micro5",               "Micro 5 — erittäin pieni pixel"),
    ("dotgothic16",          "DotGothic16 — japanilainen bitmap gothic"),
    # === LISÄÄ GOOTTILAISIA / BLACKLETTER ===
    ("almendra",             "Almendra — eleganttimedievaalinen"),
    ("almendrasc",           "Almendra SC — small caps versio"),
    ("almendradisplay",      "Almendra Display — display-koko"),
    ("imfellenglish",        "IM Fell English — vanha englantilainen"),
    ("imfelldoublepica",     "IM Fell Double Pica — historiallinen"),
    ("imfelldwpica",         "IM Fell DW Pica — historiallinen"),
    ("imfellfrenchcanon",    "IM Fell French Canon — historiallinen"),
    ("imfellgreatprimer",    "IM Fell Great Primer — historiallinen"),
    ("jollylodger",          "Jolly Lodger — komiikkakirjain"),
    ("emilyscandy",          "Emilys Candy — söpö gothic"),
    # === LISÄÄ HORROR / DARK ===
    ("hennypen",             "Henny Penny — vanha kauhufontti"),
    ("hennypenny",           "Henny Penny — kauhufontti (alt)"),
    ("soulieone",            ""),  # kokeilu
    ("caesar dressing",      ""),  # skip
    ("caesardressing",       "Caesar Dressing — teatraalinen"),
    # === LISÄÄ KOKEELLISIA / OUTOJA ===
    ("boogaloofont",         ""),  # skip
    ("rubikiso",             "Rubik Iso — isometrinen 3D"),
    ("rubik80sfade",         "Rubik 80s Fade — 80s haalistuma"),
    ("rubikdoodleshadow",    "Rubik Doodle Shadow — piirretty"),
    ("rubikdoodletriangles", "Rubik Doodle Triangles — kolmiot"),
    ("rubiklines",           "Rubik Lines — viivat"),
    ("rubikmaps",            "Rubik Maps — karttakuvio"),
    ("rubiksuperpowers",     "Rubik Superpowers — supervoimat"),
    ("rubikpixels",          "Rubik Pixels — pikselit"),
    # === KALLIGRAFIA / KÄSIALA ===
    ("pinyonscript",         "Pinyon Script — klassinen kalligrafia"),
    ("italianno",            "Italianno — italialainen käsiala"),
    ("alexbrush",            "Alex Brush — sivellin script"),
    ("greatvibes",           "Great Vibes — suuret eleet"),
    ("rougescript",          "Rouge Script — punainen script"),
    ("zeyada",               "Zeyada — henkilökohtainen käsiala"),
    ("hurricane",            "Hurricane — myrskyinen script"),
    ("qwitchergrypen",       "Qwitcher Grypen — epäsiisti käsiala"),
    ("lavishly yours",       ""),  # skip space
    ("lavishly-yours",       ""),  # kokeilu
    ("ephesis",              "Ephesis — kaunokirjoitus"),
    ("stylescript",          "Style Script — tyylikäs script"),
    ("waterfall",            "Waterfall — putoava script"),
    ("imperial script",      ""),  # skip
    ("imperialscript",       "Imperial Script — keisarillinen"),
    ("adineue prive",        ""),  # skip
    ("ruthie",               "Ruthie — hauras käsiala"),
    ("league script",        ""),  # skip
    ("leaguescript",         "League Script — kalligrafia"),
    ("mr de haviland",       ""),  # skip
    ("mrde haviland",        ""),  # skip
    ("mrdehaviland",         "Mr De Haviland — tyylikäs script"),
    ("niconne",              "Niconne — käsiala display"),
    ("romanesco",            "Romanesco — kalligrafinen"),
    ("herr von muellerhoff", ""),  # skip
    ("herrvonmuellerhoff",   "Herr Von Muellerhoff — saksalainen käsiala"),
    ("petit formal script",  ""),  # skip
    ("petitformalscript",    "Petit Formal Script — pieni formaali"),
    ("princess sofia",       ""),  # skip
    ("princesssofia",        "Princess Sofia — prinsessafontti"),
    ("sleepingbeauty",       ""),  # kokeilu
    # === SCI-FI / TECH ===
    ("aldrich",              "Aldrich — geometrinen futuristinen"),
    ("michroma",             "Michroma — tekninen geometrinen"),
    ("rationale",            "Rationale — rationaalinen tech"),
    ("exo",                  "Exo — moderni tech sans"),
    ("exo2",                 "Exo 2 — parannettu Exo"),
    ("electrolize",          "Electrolize — elektroninen"),
    ("quantico",             "Quantico — militaarinen tech"),
    ("rajdhani",             "Rajdhani — intialainen tech"),
    ("josefin sans",         ""),  # skip
    ("josefinsans",          "Josefin Sans — geometrinen retro"),
    ("josefinslab",          "Josefin Slab — slab-versio"),
    ("offside",              "Offside — viisto sci-fi"),
    # === DISPLAY / TAIDE ===
    ("emblemaone",           "Emblema One — koristeellinen"),
    ("cevicheone",           "Ceviche One — latialainen display"),
    ("changaone",            "Changa One — lihavoitu italic"),
    ("patuaone",             "Patua One — slab display"),
    ("passionone",           "Passion One — intohimoinen display"),
    ("paytonone",            "Paytone One — paksu pyöreä"),
    ("alfaslabone",          "Alfa Slab One — massiiivinen slab"),
    ("carterone",            "Carter One — vahva display"),
    ("lilitaone",            "Lilita One — lihavoitu leikkisä"),
    ("acme",                 "Acme — nopea sans display"),
    ("modak",                "Modak — intialainen massiivinen"),
    ("shrikhand",            "Shrikhand — intialainen display"),
    ("bubblegum sans",       ""),  # skip
    ("bubblegumsans",        "Bubblegum Sans — kupla-hauska"),
    ("lilyscriptone",        ""),  # jo ladattu
    ("monotonsans",          ""),  # kokeilu
    ("fasterone",            "Faster One — nopea italic"),
    ("smokum",               "Smokum — western hauska"),
    ("galada",               "Galada — bengalilainen display"),
    ("vidaloka",             "Vidaloka — tyylikäs display serif"),
    ("simonetta",            "Simonetta — eleganttirenessanssi"),
    ("oldenburg",            "Oldenburg — medieval display"),
    ("underdog",             "Underdog — epävirallinen"),
    ("raleway dots",         ""),  # skip
    ("ralewaydots",          "Raleway Dots — pisteytetty Raleway"),
    ("sail",                 "Sail — purjehdus display"),
    ("salsa",                "Salsa — latinalainen"),
    ("sancreekalt",          ""),  # kokeilu
    ("sevillana",            "Sevillana — flamenco"),
    ("snowburstyone",        "Snowburst One — luminen"),
    ("sofadione",            "Sofadi One — display"),
    ("spicyrice",            "Spicy Rice — mausteinen bold"),
    ("tulpenone",            "Tulpen One — pyöreä quirky"),
    ("warnes",               ""),  # jo ladattu
    ("wellfleet",            "Wellfleet — coastal display"),
    ("wendyone",             "Wendy One — pehmeä display"),
    ("wireone",              "Wire One — ultra-ohut"),
    # === VÄRIVIRTA / PSYKEDEELINEN ===
    ("inknutantiqua",        "Inknut Antiqua — tinttimusteinen"),
    ("plaster",              "Plaster — laasteri koristeellinen"),
    ("ewert",                "Ewert — koristeltu retro-slab"),
    ("flamenco",             "Flamenco — flamenco-tyyli"),
    ("gildadisplay",         "Gilda Display — tyylikäs display"),
    ("cormorant",            "Cormorant — eleganttikormoraani"),
    ("cormorantgaramond",    "Cormorant Garamond — klassinen eleganssi"),
    ("cormorantinfant",      "Cormorant Infant — lapsekas eleganssi"),
    ("cormorantsc",          "Cormorant SC — small caps"),
    ("cormorantunicase",     "Cormorant Unicase — yhdistetty"),
    ("cinzeldecorative",     ""),  # jo ladattu
    ("medievalsharp",        ""),  # ei GF:ssä
    ("aclonica",             "Aclonica — hauska sans"),
    ("angkor",               "Angkor — khmeriläinen"),
    ("bayon",                "Bayon — khmeriläinen display"),
    ("kavivanar",            "Kavivanar — tamilinkielinen"),
    ("keania one",           ""),  # skip
    ("keaniaone",            "Keania One — tropical display"),
    ("kenia",                "Kenia — quirky display"),
    ("kranky",               ""),  # jo ladattu
    ("lancelot",             "Lancelot — keskiaikainen eleganssi"),
    ("langar",               "Langar — punjabilainen"),
    # === OUTO JA ERILAINEN — erikoisimmat ===
    ("moiraione",            "Moirai One — mystinen/arvoituksellinen"),
    ("kablammo",             "Kablammo — räjähdysmäinen"),
    ("nabla",                "Nabla — 3D syvyysvaikutelma"),
    ("fuggles",              "Fuggles — outo medievaalinen"),
    ("wavefont",             "Wavefont — aaltoileva"),
    ("delagothicone",        "Dela Gothic One — massiivinen japanilainen"),
    ("zentokyozoo",          ""),  # jo ladattu
    ("bungee spice",         ""),  # skip
    ("bungeespice",          "Bungee Spice — värikäs/multicolor"),
    ("taprom",               "Taprom — khmeriläinen outo"),
    ("bigshouldersdisplay",  "Big Shoulders Display — erittäin kondensoitu"),
    ("bigshoulderstencil",   "Big Shoulders Stencil — kondensoitu stencil"),
    ("bigshouldersinline",   "Big Shoulders Inline — inline stencil"),
    ("bigshoulderstext",     "Big Shoulders Text — teksti-versio"),
    ("zcoolkuaile",          "ZCOOL KuaiLe — kiinalainen hauska"),
    ("zcoolqingkehuangyou",  "ZCOOL QingKe HuangYou — kiinalainen"),
    ("notocoloremoji",       ""),  # liian iso, skip
    ("rubikbubbles",         "Rubik Bubbles — kuplat"),
    ("rubikpixels",          "Rubik Pixels — pixelimuoto"),
    ("rubikiso",             ""),  # kokeilu uudelleen
    ("rubik80sfade",         "Rubik 80s Fade — 80-luku haalistuu"),
    ("rubikdoodleshadow",    "Rubik Doodle Shadow — piirretty varjo"),
    ("rubiksuperpowers",     "Rubik Superpowers — supersankari"),
    ("rubiklines",           "Rubik Lines — viivarakenne"),
    ("yarndings",            "Yarndings — lankasilmukka-ikonit"),
    ("narnoor",              "Narnoor — devanagari outo"),
    ("geostar",              "Geostar — geometrinen tähtimuoto"),
    ("geostarfill",          "Geostar Fill — täytetty versio"),
    ("nova mono",            ""),  # jo ladattu
    ("atomic age",           ""),  # skip
    ("atomicage",            "Atomic Age — 50-luvun atomityyli"),
    ("vt323",                ""),  # jo ladattu
    ("�⿺辶⿳穴亻工",        ""),  # skip, bad chars
    ("galindo",              "Galindo — lohkokirjain"),
    ("rammetto one",         ""),  # skip
    ("ramettoone",           ""),  # kokeilu
    ("rammetto",             "Rammetto One — pyöreä kontti"),
    ("potta one",            ""),  # skip
    ("pottaone",             "Potta One — intialainen massiivinen"),
    ("tourney",              "Tourney — turnauskondensoitu"),
    ("teko",                 "Teko — kondensoitu urbaani"),
    ("baumans",              "Baumans — geometrinen tekninen"),
    ("plaster",              ""),  # jo listassa
    ("gorditas",             "Gorditas — lihava hauska"),
    ("keyfontone",           ""),  # kokeilu
    ("nosifer",              "Nosifer — kauhea/verinen"),
    ("hanalei",              "Hanalei — havaijilaiset kuviot"),
    ("hanaleifill",          "Hanalei Fill — täytetty havaiji"),
    ("chokokutai",           "Chokokutai — japanilainen käsinkirjoitettu"),
]

def api_list(fontdir, base="ofl"):
    url = f"https://api.github.com/repos/google/fonts/contents/{base}/{fontdir}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            if isinstance(data, list):
                return data
    except:
        pass
    return None

def download_file(raw_url, dest_path):
    req = urllib.request.Request(raw_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            dest_path.write_bytes(r.read())
        return True
    except:
        return False

# Poista duplikaatit ja tyhjät
seen = set()
fonts_clean = []
for d, desc in FONTS:
    if desc and d not in seen:
        seen.add(d)
        fonts_clean.append((d, desc))

print(f"Ladataan {len(fonts_clean)} fonttiperhettä...\n")
ok, skipped = [], []

for fontdir, desc in fonts_clean:
    files = api_list(fontdir, "ofl") or api_list(fontdir, "apache")
    if not files:
        print(f"  --    {fontdir}")
        skipped.append(fontdir)
        time.sleep(0.25)
        continue

    ttf_files = [f for f in files if isinstance(f, dict) and f.get("name","").endswith(".ttf")]
    if not ttf_files:
        skipped.append(fontdir)
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
        time.sleep(0.1)

    print(f"  OK    {desc} ({downloaded} tiedostoa)")
    ok.append(fontdir)
    time.sleep(0.3)

print(f"\n=== VALMIS ===")
print(f"Ladattu: {len(ok)} fonttiperhe")
print(f"Ei löytynyt: {len(skipped)}")
