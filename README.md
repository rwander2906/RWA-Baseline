# RWA Baseline

Zentraler Engineering-Standard für Softwareprojekte von RWA.

Die Baseline bündelt wiederverwendbare Regeln für Entwicklungsprozess, Qualität, Tests, Dokumentation, Security, Logging, Releases und Refactoring. Projektspezifische Repositories referenzieren eine konkrete Baseline-Version und dokumentieren nur Ergänzungen oder begründete Abweichungen.

## Leitprinzipien

- issue-driven development
- Entwicklung über Branch und Pull Request
- `staging` als Integrationsstand, `main` als freigegebener Produktions-/Release-Stand
- explizite Freigabe vor Promotion nach `main`
- grüne CI als Merge-Voraussetzung
- Tests und Regressionstests als Teil der Änderung
- messbare Coverage- und Complexity-Gates
- keine neuen Warnings
- zentrale Logging- und Secret-Regeln
- Dokumentation und Definition of Done sind Bestandteil der Entwicklung
- technische Schulden werden als Issues sichtbar gemacht
- Baseline-Abweichungen werden explizit dokumentiert, nicht stillschweigend gelebt

## Versionierung

Die Baseline folgt Semantic Versioning:

- PATCH: Klarstellungen und kompatible Detailverbesserungen
- MINOR: neue oder verschärfte Regeln, die Adoption-Arbeit erzeugen können
- MAJOR: grundlegende Änderungen am Entwicklungsmodell

Aktueller Entwurfsstand: **0.1.0**. Ziel: **1.0.0** nach Review der aus INES und SLA-Report-Gen abgeleiteten Regeln.

## Nutzung in Projekten

Jedes Projekt erhält eine `.rwa-baseline.yml`, z. B.:

```yaml
baseline:
  version: "1.0.0"
  adopted: "2026-10-03"

profile:
  language: "python"

exceptions: []
```

Abweichungen müssen begründet, möglichst mit Issue versehen und regelmäßig überprüft werden.

## Struktur

- `docs/` – verbindliches Regelwerk
- `checklists/` – operative Checklisten
- `templates/` – wiederverwendbare GitHub-/Workflow-Vorlagen
- `profiles/` – sprach- bzw. stackbezogene Ergänzungen
- `scripts/` – spätere Prüf- und Bootstrap-Werkzeuge

## Herkunft

Baseline 0.1 wurde aus den praktischen Erfahrungen und Qualitätsregeln von INES und SLA-Report-Gen abgeleitet. Projektspezifische Regeln wurden bewusst vom allgemeinen Standard getrennt.
