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


## Persistenter Integrationsbranch bei Auto-Delete

`Delete branch on merge` bleibt aktiviert, damit kurzlebige Issue- und Feature-Branches nach dem Merge automatisch entfernt werden.

Da GitHub diese Einstellung repositoryweit anwendet, kann auch der persistente Integrationsbranch `staging` nach einer Promotion `staging -> main` gelöscht werden. Baseline-Projekte enthalten deshalb den Workflow `.github/workflows/preserve-staging.yml`.

Der Workflow:

- reagiert ausschließlich auf erfolgreich gemergte Pull Requests von `staging` nach `main`
- prüft zuerst, ob `staging` noch existiert
- legt `staging` nur bei Bedarf am gerade nach `main` promoteten Commit neu an
- verändert das Auto-Delete-Verhalten für Issue- und Feature-Branches nicht

Der Bootstrap übernimmt diesen Workflow automatisch in neue Projekte. Dafür benötigt der Workflow `contents: write`; alle übrigen Baseline-Workflows behalten ihre minimal erforderlichen Berechtigungen.


## Persistenter Integrationsbranch (Issue #15)

`staging` ist ein dauerhafter Integrationsbranch und darf bei Promotionen
`staging -> main` nicht automatisch gelöscht werden. Die GitHub-Einstellung
**Automatically delete head branches** gilt repositoryweit: sie ist deshalb
für das zweistufige Branchmodell zu deaktivieren, solange keine unabhängig
validierte Schutz-/Wiederherstellungslösung aktiv ist. Feature-Branches sind
in diesem Fall nach dem Merge gezielt zu löschen.

Vor jeder Promotion: Sicherstellen, dass `staging` existiert, Branch-Schutz
aktiv ist und keine noch nicht promoteten Änderungen verloren gehen.
Nach der Promotion: Existenz und Commit-Stand von `staging` prüfen.
Falls `staging` gelöscht wurde, ihn **nur nach vorheriger Prüfung offener PRs**
aus `main` wiederherstellen und bestehende Arbeitsbranches unangetastet lassen.
Die Wiederherstellung ist keine automatische Konfliktlösung.

Diese Einstellung wird in GitHub unter **Settings → General → Pull Requests**
vorgenommen; die GitHub-Anbindung kann diese Repository-Einstellung derzeit
nicht unmittelbar verändern. Vor einem Release ist die Konfiguration deshalb
manuell zu verifizieren.
