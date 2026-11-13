# HEROPRINT Website

Mobile-first Landingpage für HEROPRINT – 3D-Druck, CAD, Einzelteile und Kleinserien.

## GitHub Pages
1. Inhalt dieses Ordners in ein GitHub-Repository hochladen.
2. In GitHub: **Settings → Pages**.
3. Unter **Build and deployment**: `Deploy from a branch` wählen.
4. Branch `main`, Ordner `/ (root)` auswählen und speichern.

Die Seite benötigt keinen Build-Prozess und keine npm-Abhängigkeiten. GSAP wird über jsDelivr geladen.

## Review-Vorschau (getrennt von der Live-Seite)

- Quellbranch: `fix/review-preview`; `main` und dessen Pages-Einstellungen bleiben unverändert.
- Pushes auf den Review-Branch führen `.github/workflows/review.yml` aus: Syntaxprüfung, statischer Preview-Build, Chromium-Regressionstests und herunterladbares Build-Artefakt.
- Die öffentlich erreichbare Vorschau liegt im separaten Repository `heroprint/heroprint-page-preview` unter https://heroprint.github.io/heroprint-page-preview/.
- Zum Aktualisieren dort unter **Actions → Build and deploy isolated preview → Run workflow** den vollständigen Commit-SHA des Quellbranches als `source_sha` angeben. Die Vorschau wird bewusst manuell ausgelöst, nicht zeitgesteuert. Sie baut und testet genau diesen Commit vor dem Deployment.
- `version.json` auf der Vorschauseite nennt den gebauten Quellcommit; der Preview-Build setzt `noindex,nofollow` und lässt `assets/old` weg. Die Vorschau ist öffentlich, nicht zugriffsgeschützt.
- Lokal: `python -m pip install playwright==1.65.1`, `python -m playwright install chromium`, dann `python -m http.server 8765 --bind 127.0.0.1`. In einem zweiten Terminal: `python -m unittest discover -s tests -p '*_test.py' -v`.
- Tests gegen eine gebaute/entfernte Vorschau: `PREVIEW_URL` setzen. Bei vorhandenem Chrome kann `CHROME_PATH` auf dessen ausführbare Datei zeigen.

## Vor Livegang anpassen
- Kontaktformular an einen echten Formular-Endpunkt oder eine E-Mail-Lösung anbinden.
- Etsy-Shop-Link ergänzen, sobald der Shop online ist.
- Impressum und Datenschutzerklärung ergänzen.
- Eigene echte Projektfotos können jederzeit in `assets/` ersetzt werden.
