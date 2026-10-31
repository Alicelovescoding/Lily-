import json
import os
from flask import Flask, render_template, request, redirect, url_for
import webview

app = Flask(__name__)

DATEI_PFAD = "daten.json"

# Standarddaten, falls noch keine Datei existiert
STANDARD_DATEN = {
    "titel": "Lily",
    "aufgaben": ["Lernen", "Code schreiben"]
}

def daten_laden():
    """Liest die JSON-Datei. Falls sie fehlt, liefert sie Standardwerte."""
    if not os.path.exists(DATEI_PFAD):
        return STANDARD_DATEN
    with open(DATEI_PFAD, "r", encoding="utf-8") as f:
        return json.load(f)

def daten_speichern(daten):
    """Schreibt das Python-Dictionary formatiert in die JSON-Datei."""
    with open(DATEI_PFAD, "w", encoding="utf-8") as f:
        # indent=2 sorgt dafür, dass die Datei lesbar formatiert bleibt
        json.dump(daten, f, ensure_ascii=False, indent=2)

@app.route("/")
def home():
    daten = daten_laden()
    return render_template("index.html", titel=daten["titel"], aufgaben=daten["aufgaben"])

@app.route("/add", methods=["POST"])
def aufgabe_hinzufuegen():
    neuer_eintrag = request.form.get("neue_aufgabe", "").strip()
    
    if neuer_eintrag:
        # 1. Aktuellen Stand einlesen
        daten = daten_laden()
        # 2. Im Python-Objekt ergänzen
        daten["aufgaben"].append(neuer_eintrag)
        # 3. Datei überschreiben
        daten_speichern(daten)
        
    return redirect(url_for("home"))

@app.route("/delete/<int:index>", methods=["POST"])
def aufgabe_loeschen(index):
    daten = daten_laden()
    # Prüfen, ob der Index innerhalb der Liste liegt, um Fehler zu vermeiden
    if 0 <= index < len(daten["aufgaben"]):
        daten["aufgaben"].pop(index)
        daten_speichern(daten)
    return redirect(url_for("home"))


if __name__ == "__main__":
    # Startet das Programm direkt als Desktop-Fenster
    webview.create_window("Lily", app, width=900, height=650)
    webview.start()
