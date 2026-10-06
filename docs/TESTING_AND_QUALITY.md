# Testing & Quality

## Leitprinzip: Verhalten vor Kennzahl

Tests sichern beobachtbares, fachlich relevantes Verhalten. Coverage zeigt, welcher Code ausgeführt wurde; sie beweist weder sinnvolle Assertions noch vollständige Fachlichkeit. Ein grünes Coverage-Gate ersetzt deshalb niemals die Prüfung, ob die relevanten Verhaltensweisen abgesichert sind.

## Testpflicht

Jede fachlich relevante Funktion oder Komponente wird angemessen automatisch getestet. Für jede geänderte fachliche Verhaltensweise werden die tatsächlich relevanten Testklassen betrachtet:

- Normalfall / erwarteter erfolgreicher Ablauf
- Fehler- und Negativfälle
- relevante Grenzwerte und Zustandsübergänge

Nicht jede Änderung braucht künstlich genau drei Tests. Entscheidend ist, dass fachlich unterschiedliche Ergebnisse, Fehlerpfade und Grenzen abgesichert sind.

Jeder Bugfix erhält einen Regressionstest, der den ursprünglichen Fehler vor dem Fix reproduzieren würde und nach dem Fix dauerhaft absichert.

Tests sind deterministisch. Unit- und Komponententests dürfen nicht von produktiven externen Diensten, produktiven Credentials, aktueller Uhrzeit, unkontrolliertem Zufall oder veränderlichen Netzdaten abhängen. Solche Abhängigkeiten werden durch Fakes, Mocks, Fixtures, kontrollierte Seeds/Uhren oder klar getrennte Integrationstests beherrscht.

## Coverage

### Neue Projekte

Baseline für neue Projekte:

- Mindestwert Gesamt-Coverage: **80 %**
- Zielwert: **90 %**
- neue oder wesentlich geänderte Kernlogik: möglichst **≥ 90 %**
- sicherheits- oder geschäftskritische Kernlogik: **100 % anzustreben**

Der projektspezifische Mindestwert wird in `.rwa-baseline.yml` unter `quality.coverage_minimum` dokumentiert und muss durch ein CI-Gate erzwungen werden.

Coverage ist ein Sicherheitsnetz und kein Selbstzweck. Tests ohne fachlichen Wert nur zur Erhöhung einer Kennzahl sind zu vermeiden. Ein hoher Gesamtwert rechtfertigt keine ungetestete neue Kernlogik.

### Legacy-Adoption und Ratchet

Bestehende Projekte dürfen bei Adoption unter 80 % starten, wenn:

1. der gemessene Istwert als `quality.coverage_minimum` dokumentiert ist,
2. das CI-Gate mindestens diesen Wert erzwingt,
3. die Schwelle nicht ohne dokumentierte Ausnahme und Begründung abgesenkt wird,
4. neue/geänderte Kernlogik angemessen und möglichst deutlich stärker als der Legacy-Bestand getestet wird,
5. Verbesserungen schrittweise in eine höhere Baseline überführt werden.

Das Ratchet verhindert Verschlechterung, ohne vor einer Baseline-Adoption künstliche Coverage-Tests zu erzwingen.

## Testvertrag im Review

PR und DoD prüfen nicht nur „Tests vorhanden“, sondern:

- welches fachliche Verhalten geändert wurde,
- welche Normal-, Fehler-/Negativ- und Grenzfälle relevant sind,
- ob ein Bugfix einen Regressionstest besitzt,
- ob neue/geänderte Kernlogik angemessen abgesichert ist,
- ob Tests deterministisch und von produktiven Diensten/Credentials unabhängig sind,
- ob Coverage-Gate oder dokumentiertes Legacy-Ratchet grün ist.

Diese fachliche Review-Entscheidung bleibt bewusst menschlich. Die Compliance-Prüfung erzwingt die dafür nötige Guideline und CI-Infrastruktur, behauptet aber nicht, Testqualität vollständig statisch beurteilen zu können.

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
- projektspezifisches Coverage-Gate
- Complexity-Gate
- Dependency-/Security-Prüfung mit einer projektspezifisch begründeten Blockierschwelle

CI-Jobs erhalten nur die erforderlichen Berechtigungen; `contents: read` ist der bevorzugte Default.

Projektspezifische Build-, Packaging-, Container- und Smoke-Tests kommen hinzu.

## Manuelle Tests

Manuelle Smoke- oder Staging-Tests ergänzen automatische Tests dort, wo reale UI-, Runtime-, Deployment- oder Integrationspfade sinnvoll geprüft werden müssen. Sie ersetzen keine automatisierbaren Regressionstests.
