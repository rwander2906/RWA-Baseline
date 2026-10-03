# Repository Settings

Die Baseline selbst und daraus gestartete Projekte sollen die folgenden Repository-Einstellungen verwenden.

## Verbindlich

- Default Branch: `main`
- Integrationsbranch: `staging`
- Delete branch on merge: aktiviert
- Pull Requests für fachliche Änderungen
- direkte fachliche Änderungen auf `main` und `staging` vermeiden
- Promotion nach `main` nur mit bestandenem Promotion-Gate
- GitHub Actions mit minimal erforderlichen Berechtigungen

## Empfohlene Branch-/Ruleset-Regeln

### main

- Pull Request erforderlich
- Status Checks erforderlich:
  - Baseline/Projekt-CI
  - Promotion Gate
- kein Force Push
- kein Löschen
- direkte Pushes nur für ausdrücklich begründete Automatisierung
- Promotion-PR kommt regulär von `staging`

### staging

- Pull Request erforderlich
- Projekt-CI muss grün sein
- kein Force Push
- Arbeitsbranches werden nach Merge gelöscht

## Technische Einschränkung dieser Einrichtung

Die derzeit verfügbare GitHub-Integration kann Repository-Dateien, Branches, Issues und Pull Requests bearbeiten, aber keine Repository-Settings oder Rulesets schreiben.

Darum werden die Sollwerte hier versioniert und zusätzlich im Bootstrap-/Compliance-Werkzeug berücksichtigt. Die erstmalige Aktivierung von `delete_branch_on_merge` und Rulesets muss derzeit über GitHub selbst oder später über ein Bootstrap-Werkzeug mit GitHub API/CLI erfolgen.
