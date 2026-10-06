## Zugehöriges Issue

Refs #

## Änderung

-

## Prüfung

- [ ] Akzeptanzkriterien erfüllt
- [ ] fachlich geändertes Verhalten inkl. relevanter Normal-, Fehler-/Negativ- und Grenzfälle getestet
- [ ] neue/geänderte Kernlogik angemessen abgesichert
- [ ] Tests deterministisch und unabhängig von produktiven Diensten/Credentials
- [ ] Regressionstest bei Bugfix oder nicht erforderlich
- [ ] Lint/statische Analyse grün
- [ ] Compile/Syntax grün oder nicht anwendbar
- [ ] Complexity/Ratchet grün
- [ ] Coverage/Ratchet grün
- [ ] Dependency-/Security-Prüfung grün
- [ ] Dokumentation geprüft
- [ ] Logging/Datenschutz/Secrets geprüft
- [ ] Smoke-/Staging-Test durchgeführt oder nicht erforderlich

## Baseline

- [ ] keine neue unbegründete Abweichung von der RWA Baseline

## Promotion nach main

Nur für PRs `staging -> main`:

- [ ] ausdrückliche Freigabe für diese Promotion liegt vor
- [ ] Label `promotion-approved` gesetzt
- [ ] Release-/Deployment-Auswirkungen geprüft

Arbeits-PRs nach `staging` verwenden `Refs #N`. Das Issue wird erst mit der Promotion nach `main` geschlossen.
