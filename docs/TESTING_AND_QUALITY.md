# Testing & Quality

## Testpflicht

Jede fachlich relevante Funktion oder Komponente wird angemessen automatisch getestet. Relevante Verzweigungen berücksichtigen Normalfall, Fehler-/Negativfall und relevante Grenzwerte.

Jeder Bugfix erhält einen Regressionstest, der den ursprünglichen Fehler reproduziert.

Unit-Tests sind deterministisch und dürfen nicht von realen externen Diensten, produktiven Credentials oder zufälligem Verhalten ohne kontrollierten Seed/Mock abhängen.

## Coverage

Empfohlene Baseline für neue Projekte:

- Mindestwert Gesamt-Coverage: 80 %
- Zielwert: 90 %
- neue oder wesentlich geänderte Kernlogik: möglichst ≥ 90 %
- sicherheits- oder geschäftskritische Kernlogik: 100 % anzustreben

Für Legacy-Projekte darf die anfängliche Schwelle niedriger liegen, wenn der Istwert dokumentiert wird und die Baseline schrittweise steigt. Coverage darf nicht durch sinnlose Tests künstlich optimiert werden.

## Complexity

Cyclomatic/structural complexity wird automatisiert geprüft. Empfohlener maximaler Richtwert pro Funktion: 12. Abweichungen müssen nachvollziehbar sein.

## Warnings

Zielzustand: 0 neue Lint-, Compiler- und statische Analyse-Warnings. Bestehende Warnings werden sichtbar dokumentiert und planmäßig abgebaut.

## CI-Mindestumfang

Die CI prüft mindestens:
- Dependency-Installation
- Linting / statische Analyse
- Syntax/Compile, soweit anwendbar
- automatische Tests
- Coverage-Gate
- Complexity-Gate

Projektspezifische Build- und Smoke-Tests kommen hinzu.
