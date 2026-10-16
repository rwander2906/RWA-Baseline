# GitHub AI Code Review Gate

Der AI-Code-Review-Workflow läuft unabhängig von der normalen CI für Pull Requests nach `staging` und `main`.

Ein PR referenziert sein Arbeits-Issue mit `Refs #N`, `Closes #N` oder `Fixes #N`. Das Gate sammelt PR-Diff, Issue und Akzeptanzkriterien, Baseline-Regeln sowie vorhandene Projekt-Guidelines und Architekturinformationen in das providerneutrale Review-Paket.

Das normalisierte Ergebnis wird in der GitHub Job Summary mit Verdict und Fundstellen dargestellt. `PASS` und `WARN` lassen den Review-Job erfolgreich enden; `BLOCK` lässt ausschließlich den AI-Code-Review-Job fehlschlagen und kann als Required Check konfiguriert werden. Build, Tests, Linting und Packaging bleiben separat.

Für die Baseline ist der deterministische Provider `fake` Standard. Projekte konfigurieren Provider und Modell über Repository Variables. Secrets gehören ausschließlich in GitHub Secrets.
