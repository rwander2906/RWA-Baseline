# Definition of Done

Eine Änderung ist abgeschlossen, wenn die jeweils relevanten Punkte erfüllt sind:

- Issue, Scope und Akzeptanzkriterien sind erfüllt
- Code ist verständlich strukturiert und folgt den Naming-Regeln
- fachlich relevante Code-Dokumentation ist vorhanden
- Tests wurden ergänzt oder angepasst
- Bugfixes besitzen einen Regressionstest
- Linting/statische Analyse ist grün
- Compile/Syntaxprüfung ist grün, soweit anwendbar
- Complexity-Gate bzw. dokumentiertes Ratchet ist grün
- Coverage-Gate bzw. dokumentiertes Ratchet ist grün
- Dependency-/Security-Prüfung ist grün
- Fehlerbehandlung wurde geprüft
- Logging, Datenschutz und Secret-Schutz wurden geprüft
- Dokumentation wurde angepasst
- notwendiges Build-, Betriebs-, Konfigurations- und Migrationswissen ist im Repository nachvollziehbar; kein kritischer Schritt existiert ausschließlich als Chat-, Prompt- oder persönliches Wissen
- die Änderung bleibt ohne KI-Dienst baubar, testbar, betreibbar und durch einen kompetenten Entwickler weiterentwickelbar
- CI ist vollständig grün
- erforderliche manuelle Smoke-/Staging-Tests wurden durchgeführt und dokumentiert
- keine unbegründete Baseline-Abweichung wurde eingeführt
- die Änderung wurde explizit nach `main` freigegeben und promotet
- erforderliches Release/Deployment war erfolgreich

Vor der Promotion kann eine Änderung auf `staging` technisch fertig und getestet sein, das zugehörige Issue bleibt jedoch offen.
