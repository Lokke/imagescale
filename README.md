# 🎵 Band-Logo Skalierung für Radio

Diese Web-Anwendung ermöglicht es Radiomoderatoren, Band-Logos hochzuladen und automatisch für die Website aufzubereiten. Das Logo wird zentriert, skaliert und der Hintergrund transparent gemacht.

## ✨ Features

- 🎸 **Upload** von Band-Logos über Web-Interface (Drag & Drop)
- 🎯 **Automatische Verarbeitung**: Hintergrund-Entfernung und Zentrierung  
- 📐 **Flexible Größen**: 300×300, 512×512, 1024×1024, 2048×2048 px
- 🔄 **Zwei Versionen**: Normal und invertiert
- 💾 **PNG Download** mit Transparenz
- 🇩🇪 **Deutsche Oberfläche** für Radiomoderatoren
- 🚀 **High-Quality Processing** für pixelfreie große Ausgaben

## 🐳 Schnellstart mit Docker

```bash
# Build und Start mit Docker
docker build -t band-logo-tool .
docker run -p 8724:8724 band-logo-tool

# Zugriff über http://localhost:8724
```

## 🔧 Manuelle Installation

1. **Python 3.12+** installieren
2. **Abhängigkeiten installieren**: `pip install -r requirements.txt`
3. **Backend starten**: `python backend/app.py`
4. **Browser öffnen**: <http://localhost:8724>

## 📁 Projektstruktur

```
imagescale/
├── backend/           # Flask Backend und Bildverarbeitung
│   └── app.py        # Hauptanwendung mit Pillow
├── frontend/         # HTML/JS Frontend
│   └── index.html    # Deutsche Benutzeroberfläche  
├── static/           # Statische Dateien
├── Dockerfile        # Container-Konfiguration
└── requirements.txt  # Python-Dependencies
```

## 🚀 Produktive Features

- **Gunicorn** Production WSGI Server (4 Worker)
- **High-Resolution Processing** für beste Qualität
- **CORS** aktiviert für API-Zugriff
- **Docker Ready** für einfaches Deployment
- **Port 8724** für Production-Einsatz
- **Non-Root Container** für Sicherheit

## 📱 Verwendung

1. 🎵 **Band-Logo hochladen** (Drag & Drop oder Dateiauswahl)
2. 📏 **Ausgabegröße wählen** (300px bis 2048px)
3. ⚙️ **Helligkeits-Schwelle anpassen** falls nötig
4. 🎯 **"Logo verarbeiten"** klicken
5. 💾 **Beide Versionen herunterladen** (Normal + Invertiert)

## 🎨 Bildverarbeitung

- **Intelligente Skalierung**: Hochauflösende Zwischenverarbeitung
- **Automatisches Cropping**: Tight Crop um Logo-Inhalt
- **Transparenz-Mapping**: Dunkle Bereiche werden transparent
- **Quadratisches Format**: Automatische Zentrierung
- **Kantenglättung**: LANCZOS-Resampling für beste Qualität

---
