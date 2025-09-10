# 🍺 ANLEITUNG FÜR VÖLLIG BESOFFENE RADIOMODERATOREN 🎙️

## 🚨 WICHTIG: Erst Kaffee trinken, dann lesen! ☕

---

## 📋 TEIL 1: INSTALLATION (Für den IT-Menschen)

### 🔧 Was brauche ich?
- Einen Computer mit Internet
- Docker (das blaue Wal-Ding)
- 5 Minuten Zeit
- Keine Panik

### 🐳 Docker installieren (wenn nicht vorhanden)
**Windows/Mac:** 
1. Gehe zu: https://www.docker.com/products/docker-desktop
2. Lade runter, installiere, starte neu
3. Warte bis der Wal schwimmt

**Linux/Server:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
```

### 🚀 Installation - SO EINFACH WIE BIER ÖFFNEN

```bash
# 1. Code runterladen (auch für Betrunkene machbar)
git clone https://github.com/Lokke/imagescale.git
cd imagescale

# 2. EINEN BEFEHL - Das war's!
./docker-run.sh
```

**Für Windows-Opfer:**
```cmd
docker-run.bat
```

### 🎯 Fertig! 
Die App läuft jetzt auf: **http://localhost:8724**

---

## 🎵 TEIL 2: BENUTZUNG (Für besoffene Moderatoren)

### 🔍 Schritt 1: Website öffnen
- Gehe zu: **http://localhost:8724** (oder die URL die der IT-Mensch dir gibt)
- Du siehst: Eine lila Website mit einem Gitarren-Symbol 🎸

### 📁 Schritt 2: Band-Logo hochladen
**DREI WEGE (wähle einen, auch wenn du doppelt siehst):**

1. **DRAG & DROP** 🖱️
   - Ziehe das Logo-Bild einfach in das lila Feld
   - Wie beim Solitaire, nur einfacher

2. **KLICK-METHODE** 👆
   - Klicke auf das lila Feld
   - Wähle dein Bild aus (JPG, PNG, was auch immer)

3. **BESOFFENEN-SICHERE METHODE** 🍺
   - Klicke einfach überall rum bis ein Datei-Dialog aufgeht
   - Hauptsache du findest dein Band-Logo

### ⚙️ Schritt 3: Einstellungen (optional - für Perfektionisten)

**Ausgabegröße:**
- 300×300: Für die Website (Standard - lass es so!)
- 512×512: Wenn du denkst "größer ist besser"
- 1024×1024: Für Poster oder so
- 2048×2048: Wenn du völlig übertreibst

**Helligkeits-Schwelle:**
- Schieber zwischen 20 und 200
- 50 ist perfekt (lass es so, außer es sieht scheiße aus)
- Links = mehr wird transparent
- Rechts = weniger wird transparent

### 🎯 Schritt 4: MAGIE PASSIERT
- Klicke auf: **"🎵 Logo verarbeiten"**
- Warte 2 Sekunden (Zeit für einen Schluck)
- Bewundere das Ergebnis

### 💾 Schritt 5: Runterladen
Du bekommst **ZWEI VERSIONEN:**
1. **Normal** - Weißes Logo auf transparentem Hintergrund
2. **Invertiert** - Für dunkle Hintergründe

**Klicke auf:** "💾 Normal PNG" oder "💾 Invertiert PNG"

---

## 🆘 HILFE! ES FUNKTIONIERT NICHT!

### ❌ "Seite lädt nicht"
**Problem:** Docker läuft nicht
**Lösung:** 
```bash
# Starte den Container neu
docker run -d -p 8724:8724 --name imagescale-app band-logo-tool
```

### ❌ "Upload funktioniert nicht"
**Problem:** Du bist zu besoffen
**Lösung:** 
1. Trinke Wasser
2. Versuche es nochmal
3. Frage den IT-Menschen

### ❌ "Logo sieht scheiße aus"
**Problem:** Falsches Bild oder schlechte Einstellungen
**Lösung:**
1. Verwende ein Bild mit gutem Kontrast
2. Spiele mit der Helligkeits-Schwelle rum
3. Probiere verschiedene Größen

### ❌ "Ich verstehe nichts"
**Problem:** Du bist ein Radiomoderator, kein IT-Experte
**Lösung:**
1. Rufe den IT-Menschen an
2. Zeige ihm diese Anleitung
3. Lass ihn machen, gehe Bier trinken

---

## 🎪 PROFITIPPS FÜR FORTGESCHRITTENE BESOFFENE

### 📸 Beste Bilder für die Verarbeitung:
- **Gut:** Schwarzes Logo auf weißem Hintergrund
- **Auch gut:** Weißes Logo auf dunklem Hintergrund (dann "Invertiert" nutzen)
- **Schlecht:** Bunte Logos auf buntem Hintergrund
- **Völlig daneben:** Screenshots von WhatsApp

### 🎨 Wann welche Version nutzen:
- **Normal (weiß):** Für dunkle Website-Hintergründe
- **Invertiert (schwarz):** Für helle Website-Hintergründe
- **Bei Unsicherheit:** Nimm beide, entscheide später

### 🚀 Workflow für Profis:
1. Logo hochladen
2. Beide Versionen runterladen
3. An Webdesigner schicken mit Notiz: "Mach was Schönes draus"
4. Bier trinken

---

## 📞 SUPPORT HOTLINE

**Für technische Probleme:**
- Rufe deinen IT-Menschen an
- Zeige ihm diese Anleitung
- GitHub: https://github.com/Lokke/imagescale

**Für Bedienungsfragen:**
- Lese diese Anleitung nochmal
- Diesmal nüchtern
- Frage deine Kollegen

**Für existenzielle Fragen:**
- Warum verarbeitest du Band-Logos um 3 Uhr nachts?
- Vielleicht solltest du weniger trinken?
- Das Tool kann auch tagsüber verwendet werden!

---

## 🎵 FAZIT

**Du hast jetzt ein Tool, mit dem du:**
- Band-Logos in Sekunden aufbereitest
- Transparente Hintergründe erzeugst
- Professionell aussehende Ergebnisse bekommst
- Zeit für wichtigere Dinge hast (wie Bier trinken)

**Viel Spaß beim Logo-Verarbeiten! 🍻**

---

*Diese Anleitung wurde mit viel Liebe und Verständnis für die Bedürfnisse von Radiomoderatoren erstellt. Bei Beschwerden bitte an den nächstgelegenen IT-Support wenden.*
