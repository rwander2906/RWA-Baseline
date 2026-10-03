# Changelog

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
