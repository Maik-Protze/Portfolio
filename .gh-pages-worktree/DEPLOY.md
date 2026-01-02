DEPLOY: GitHub + Hosting (kostenfrei)

Ziel
----
Du willst die Seite mit GitHub verbinden, selbst aktualisieren können, dabei keine laufenden Kosten haben, GitHub-bezogene Kontaktdaten auf der Website verbergen und Besuchern die Seite (und optional den Quellcode zum Download) zeigen, ohne dass sie die Live-Site online editieren können.

Zwei empfohlene Optionen
-----------------------
A) GitHub Pages (einfach, komplett kostenlos)
   - Code liegt im GitHub-Repository (öffentlich sichtbar).
   - Live-Website wird per GitHub Pages kostenlos gehostet.
   - Besucher sehen die Website; nur du (mit GitHub-Zugang) kannst das Repo/Website aktualisieren.
   - Nachteil: das Repository ist public (Code sichtbar, kann geforkt werden).

B) GitHub (privates Repo) + Netlify (empfohlen wenn du GitHub-Daten nicht öffentlich zeigen willst)
   - Repo auf GitHub bleibt *privat* (anderer sehen dein Repo nicht).
   - Netlify (kostenloses Konto) kann deinen privaten Repo deployen, oder du verbindest Netlify manuell per Drag&Drop (ohne Konto) mit einem ZIP.
   - Live-Website ist öffentlich für Besucher, dein GitHub-Account/Repo bleibt privat.
   - Du kannst per `git push` arbeiten; Netlify führt automatische Deploys aus (wenn du es verbindest).

Welche Option passt? Kurz
- Willst du, dass der Quellcode für alle auf GitHub sichtbar ist? -> Option A (GitHub Pages)
- Willst du, dass die Website öffentlich ist, aber dein GitHub-Konto/Repo verborgen bleibt? -> Option B (GitHub privat + Netlify)

Vorbereitung - Wichtige Schritte (unbedingt vor dem Hochladen)
------------------------------------------------------------
1. Entferne alle sensiblen Dateien und `.git`-Metadaten aus dem Upload (du hast bereits `site-publish.zip` erstellt, gut).
2. Suche nach Tokens/API-Keys in Dateien und entferne sie oder ersetze sie durch Platzhalter.
3. Entferne sichtbare Links zu deinem GitHub-Profil auf der Webseite (bereits erledigt).
4. Optional: lege eine `README.md` und `LICENSE` an, falls du möchtest, dass andere deine Lizenzbedingungen sehen.

Installationen (lokal, optional aber empfohlen)
-----------------------------------------------
- Git:
  - Debian/Ubuntu:
    ```bash
    sudo apt update
    sudo apt install git
    ```
- Node.js + npm (nur wenn du Netlify CLI verwenden willst):
  - Beispiel (Node 18 LTS):
    ```bash
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
    ```
- Netlify CLI (optional):
    ```bash
    npm install -g netlify-cli
    ```
- `gh` (GitHub CLI, optional, erleichtert Repo-Erstellung):
  - Installationsanleitung: https://cli.github.com/

A) Schritt-für-Schritt: GitHub Pages (öffentliche Repo)
------------------------------------------------------
1. Lokales Git initialisieren (falls noch nicht):
   ```bash
   cd /home/dci-student/Portfolio
   git init
   git add .
   git commit -m "Initial commit: Portfolio site"
   ```
2. Auf GitHub ein neues Repository erstellen (Name z.B. `portfolio-maik`).
   - Entweder per Web (github.com → New repository) oder per GitHub CLI:
     ```bash
     gh repo create portfolio-maik --public --source=. --remote=origin --push
     ```
   - Falls du `gh` nicht verwendest: erstelle Repo im Browser und folge den "push an existing repository"-Anweisungen.
3. GitHub Pages aktivieren:
   - In den Repo‑Settings → "Pages" → Source: `main` branch (root) auswählen → Save.
   - Innerhalb weniger Minuten ist die Site unter `https://<username>.github.io/portfolio-maik/` erreichbar.
4. Aktualisieren:
   - Lokale Änderungen committen und `git push` ausführen. GitHub Pages aktualisiert automatisch.

B) Schritt-für-Schritt: Privates Repo + Netlify (empfohlen für Privatsphäre)
--------------------------------------------------------------------------
Variante 1 — Netlify per GitHub-Verbindung (automatische Deploys):
1. Erstelle privates Repo auf GitHub (über Web oder `gh repo create portfolio-maik --private`).
2. Push dein Code:
   ```bash
   git remote add origin git@github.com:YOUR_USERNAME/portfolio-maik.git
   git branch -M main
   git push -u origin main
   ```
3. Registriere ein kostenloses Netlify-Konto (https://www.netlify.com/).
4. In Netlify: "New site from Git" → wähle GitHub → erlaube Netlify Zugriff auf dein (privates) Repo → wähle Repo und Branch `main` → Deploy.
5. Netlify baut und deployed; künftige `git push`-Änderungen triggern Deploys.

Variante 2 — Netlify ohne GitHub-Verknüpfung (manuell, kein Konto nötig)
1. Erzeuge `site-publish.zip` (du hast das bereits gemacht).
2. Öffne https://app.netlify.com/drop und ziehe die ZIP hinein.
3. Netlify stellt die Seite bereit; Repo bleibt privat (oder gar nicht auf GitHub, wenn du es nicht pushst).
4. Aktualisieren: wiederhole das ZIP-Upload.

NovoResume Hinweise
-------------------
- NovoResume stellt oft einen öffentlichen Share‑Link bereit (wie der von dir genannte Link). Stelle sicher, dass du den Share‑Link in NovoResume auf "öffentlich" oder "freigeben" gesetzt hast, damit Besucher die Seite sehen können.
- Einbettung per `<iframe>` funktioniert nur, wenn NovoResume das Embedding erlaubt (keine X-Frame-Options: DENY). In `resume.html` ist sowohl ein Link als auch ein `<iframe>` eingefügt — wenn das `<iframe>` blockiert wird, wird der Link den Nutzern das Öffnen in einem neuen Tab erlauben.
- Wenn du möchtest, dass Besucher den PDF‑Export direkt herunterladen können, lade in NovoResume das PDF herunter und lege die Datei als `resume.pdf` in dein Projekt‑Verzeichnis (Root). Dann ist der Download‑Link in `resume.html` aktiv.
- Prüfe vor dem Deploy lokal:
   1. Öffne `resume.html` in deinem Browser (oder starte `python3 -m http.server 8000` und öffne `http://localhost:8000/resume.html`).
   2. Teste, ob der NovoResume‑Link funktioniert und ob das `<iframe>` angezeigt wird.

Privatsphäre & Sichtbarkeit
--------------------------
- Wenn du das NovoResume extern hostest (z. B. NovoResume selbst) und nur per Link verknüpfst, bleibt dein GitHub‑Repo und deine Quelldateien unabhängig davon privat (solange du das Repo privat machst oder nicht pusht).
- Wenn du die PDF in dein Repo packst, ist diese Datei für jeden sichtbar, der das Repo einsehen darf (bei privatem Repo nur für dich bzw. Berechtigte). Wenn du die PDF in das veröffentlichte Seitenpaket (`site-publish.zip`) legst, ist die herunterladbare PDF öffentlich für Besucher der Website.

Sicherheit & Sichtbarkeit erneut prüfen
--------------------------------------
- Wenn du ein privates Repo wählst: dein GitHub-Profil und Repos bleiben verborgen; die Website ist öffentlich.
- Wenn du ein öffentliches Repo wählst: Repo & Code sind sichtbar auf GitHub (kann geforkt werden).
- Besucher können die Live-Site nicht online editieren; nur du mit Repo oder Netlify‑Zugang kannst Deploys durchführen.

Konkrete nächste Schritte, die ich jetzt für dich erledigen kann
----------------------------------------------------------------
- Ich erstelle eine `DEPLOY.md` (fertig) mit diesen Anweisungen (done).
- Ich kann dir die exakten `git` und `gh` Befehle anpassen, wenn du mir deinen bevorzugten Weg nennst (public GitHub Pages vs. private + Netlify).
- Ich kann optional eine `.gitignore` hinzufügen und das Repo lokal für dich initialisieren (die Push‑Schritte musst du in deinem Terminal ausführen, weil GitHub Login interaktiv ist).

Wenn du mir sagst, welche Option du bevorzugst (A = GitHub Pages öffentlich, B = Privates Repo + Netlify), dann
- passe ich die `.gitignore` an,
- erstelle ein kurzes `push.sh` mit den Befehlen, die du nur noch ausführen musst, und
- markiere die To‑Dos als abgeschlossen.

