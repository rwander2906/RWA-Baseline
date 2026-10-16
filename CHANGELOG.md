# Changelog

## 1.2.0 - 2026-10-16

### Added
- API-basierter Review-Vertrag, Review-Harness und dokumentierte Issue-Review-Historie (vorerst mit Fake-Provider, echter AI-Provider noch nicht abgenommen).
- Anwenderdokumentations-Gate und Windows-Desktop-Release-Vorlagen.
- Artifact-Lifecycle-Policy mit CI-Prüfung gegen unnötige/lang gespeicherte Actions-Artefakte.
- Sicherung des persistenten staging-Branches durch Recovery-Workflow.
- Human-Maintainability-Anforderungen und Dokumentationshilfen als kompatible Engineering-Erweiterungen.

### Changed
- Dependabot zielt auf staging; Production-Promotion bleibt freigabepflichtig.
- Temporäre Windows-Artefakte nur bei manuell angeforderter Diagnose, Retention 1 Tag.

### Migration
- Machine-readable migration manifest: `migrations/1.2.0.json`.
- Projektspezifische Anpassungen für Dokumentations-Gates, Actions-Uploads und staging-Branch-Sicherung prüfen.
- AI-Review bleibt ohne echten Provider ein optionales/advisory Gate, nicht als produktive KI-Prüfung ausgeben.


## 1.1.0 - 2026-10-05

### Added
- Dependabot-PRs werden automatisch als verknüpfte GitHub-Issues dokumentiert.
- Baseline-Regel `workflow.dependabot.issue-tracker`.
- Dependabot-Konfiguration als verpflichtender Bestandteil aktiv gepflegter Projekte.
- Bootstrap übernimmt Dependabot-Konfiguration und Issue-Tracking-Workflow.
- Compliance-Check wählt den Regelkatalog passend zur adoptierten Baseline-Version.

### Migration
- Machine-readable migration manifest: `migrations/1.1.0.json`
- Dependabot-Konfiguration ergänzen.
- Dependabot-Issue-Tracker-Workflow ergänzen.
- bestehende Dependabot-PRs können bei Bedarf manuell als Issues nachdokumentiert werden.

## 1.0.0 - 2026-10-03

### Added
- Source-of-Truth-Hierarchie für Issue, PR, dauerhafte Dokumentation und Changelog
- verbindliches Issue-Lifecycle-Modell: Arbeits-PR nach `staging` referenziert, Promotion nach `main` schließt
- Coverage-, Complexity- und Warning-Ratchets für Legacy-Projekte
- Least-Privilege-Vorgaben für CI
- Dependency-/Security-Prüfung als CI-Mindestbestandteil
- Runtime-/Persistenztrennung zwischen `staging` und `production` für zustandsbehaftete Anwendungen
- verbindlichere Release-/Artefaktregeln
- Migrationsleitfaden für Baseline 1.0

### Changed
- Coverage-Zielmodell präzisiert: 80 % Minimum für neue Projekte, 90 % Zielwert, Legacy-Adoption über dokumentierte Ratchets
- Definition of Done umfasst nun explizit Promotion nach `main` und erforderliches Release/Deployment
- Logging-Regeln um Exception-Schutz, Datenschutz und Supply-Chain-Aspekte erweitert
- Baseline-Ausnahmen sollen langfristig über stabile Regel-IDs adressiert werden

### Migration
- Machine-readable migration manifest: `migrations/1.0.0.json`
- bestehende Projekte erhalten `.rwa-baseline.yml`
- Issues bleiben bis zur Promotion nach `main` offen
- CI um Dependency-/Security-Prüfung und Least-Privilege prüfen
- Legacy-Coverage/Complexity/Warnungen als Ratchet dokumentieren
- Stage-/Production-Zustände prüfen und Shared State explizit begründen
- projektspezifische Guidelines auf Ergänzungen reduzieren

## 0.1.0 - 2026-10-03

### Added
- initiale RWA Engineering Baseline
- issue-driven Entwicklungsmodell
- staging/main Promotion-Modell mit expliziter Freigabe
- Qualitäts-, Test-, Coverage-, Complexity-, Logging-, Security- und Dokumentationsregeln
- Definition of Done
- Adoption- und Refactoring-Checklisten
- GitHub PR- und Issue-Templates
- Profile für Node/JavaScript und Python

### Migration
- bestehende Projekte erhalten `.rwa-baseline.yml`
- Abweichungsanalyse gegen Baseline durchführen
- projektspezifische Guidelines auf Ergänzungen reduzieren
