# Fonttikokoelman hallintaskriptit

Skriptit `~/.local/share/fonts/` -kokoelman hallintaan.

## Skriptit

### `scripts/lue_lisenssit.py`
Lukee jokaisen TTF/OTF-fontin sisäisen metadatan (fonttools) ja luokittelee lisenssikategorioihin.
Kirjoittaa tuloksen `~/fontit-metadata.csv`:hen.

```bash
python3 scripts/lue_lisenssit.py
```

### `scripts/luo_kokoelmat.py`
Lukee `~/fontit-metadata.csv`:n ja luo font-manager-kokoelmat lisenssikategorioittain
(`~/.config/font-manager/Collections.json`). Sulje font-manager ennen ajoa.

```bash
python3 scripts/luo_kokoelmat.py
```

### `scripts/lataa_google_fonts.py`
Lataa kuratoidun valikoiman Google Fonts -fontteja GitHub API:n kautta.
Kaikki OFL tai Apache-lisenssillä — vapaa kaupalliseen käyttöön.

```bash
python3 scripts/lataa_google_fonts.py
```

### `scripts/lataa_lisaa_fontteja.py`
Toinen kierros Google Fonts -latauksista, enemmän erikoisia fontteja.

```bash
python3 scripts/lataa_lisaa_fontteja.py
```

## Kokoelman rakenne

```
~/.local/share/fonts/
├── Fonts/
│   ├── A/ ... Z/   ← TTF/OTF aakkosjärjestyksessä (~9100+ fonttia)
│   └── #/          ← numerolla alkavat
└── Misc files/     ← vanhat PS Type 1 -fontit + readme-tiedostot
```

## Font-manager-kokoelmat

| Kokoelma | Kuvaus |
|---|---|
| Vapaa kaupallinen — OFL/Apache/GPL/Public Domain/Freeware | Vapaa myös kaupalliseen käyttöön |
| Vain henkilokohtainen — Freeware NC | Ei kaupalliseen käyttöön |
| Kaupallinen — ei vapaaseen kayttoon | Vältä tai tarkista ennen käyttöä |
| Epaselva lisenssi | Harmaa alue — tarkista tarvittaessa |

## Vaatimukset

```bash
sudo apt install python3-fonttools font-manager fdupes
```
