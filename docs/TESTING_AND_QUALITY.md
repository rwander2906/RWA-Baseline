# Testing & Quality

## Testpflicht

Jede fachlich relevante Funktion oder Komponente wird angemessen automatisch getestet. Relevante Verzweigungen berücksichtigen Normalfall, Fehler-/Negativfall und relevante Grenzwerte.

Jeder Bugfix erhält einen Regressionstest, der den ursprünglichen Fehler reproduziert.

Unit-Tests sind deterministisch und dürfen nicht von realen externen Diensten, produktiven Credentials oder zufälligem Verhalten ohne kontrollierten Seed/Mock abhängen.

## Coverage

Baseline für neue Projekte:

- Mindestwert Gesamt-Coverage: **80 %**
- Zielwert: **90 %**
- neue oder wesentlich geänderte Kernlogik: möglichst **≥ 90 %**
- sicherheits- oder geschäftskritische Kernlogik: **100 % anzustreben**

Coverage ist ein Sicherheitsnetz und kein Selbstzweck. Tests ohne fachlichen Wert nur zur Erhöhung einer Kennzahl sind zu vermeiden.

### Legacy-Projekte und Ratchet-Prinzip

Bestehende Projekte dürfen bei Adoption unter 80 % starten, wenn:

1. der gemessene Istwert dokumentiert ist,
2. ein CI-Gate vorhanden ist,
3. die Schwelle nicht ohne dokumentierte Ausnahme abgesenkt wird,
4. neue/geänderte Logik angemessen getestet wird,
5. Verbesserungen schrittweise in eine höhere Baseline überführt werden.

Ein Projekt darf damit besser werden, ohne vor der Baseline-Adoption erst künstlich auf 80 % gebracht werden zu müssen.

## Complexity

Cyclomatic/structural complexity wird automatisiert geprüft. Empfohlener maximaler Richtwert pro Funktion ist **12**.

Für Legacy-Hotspots darf ein dokumentiertes Ratchet verwendet werden: bestehende Überschreitungen bleiben zunächst sichtbar, neue oder verschlechterte Überschreitungen blockieren die CI. Verbesserungen verkleinern die Baseline.

## Warnings

Zielzustand ist **0 Warnings** in Linter, Compiler und statischer Analyse.

Bei Legacy-Projekten gilt ebenfalls ein Ratchet: keine neuen Warnings, bestehende Warnings sichtbar dokumentieren und planmäßig abbauen.

## CI-Mindestumfang

Die CI prüft mindestens:

- reproduzierbare Dependency-Installation
- Linting / statische Analyse
- Syntax/Compile, soweit anwendbar
- automatische Tests
- Coverage-Gate
- Complexity-Gate
- Dependency-/Security-Prüfung mit einer projektspezifisch begründeten Blockierschwelle

CI-Jobs erhalten nur die erforderlichen Berechtigungen; `contents: read` ist der bevorzugte Default.

Projektspezifische Build-, Packaging-, Container- und Smoke-Tests kommen hinzu.

## Manuelle Tests

Manuelle Smoke- oder Staging-Tests ergänzen automatische Tests dort, wo reale UI-, Runtime-, Deployment- oder Integrationspfade sinnvoll geprüft werden müssen. Sie ersetzen keine automatisierbaren Regressionstests.
