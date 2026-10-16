# AI Code Review

## Zweck

Das AI Code Review ist eine zusätzliche, providerneutrale Qualitätsschicht für substantielle Pull Requests. Build, Tests, Linting, Packaging und Produktlaufzeit bleiben unabhängig von einem AI-Provider.

## Vertrag

Der Kern kennt zwei versionierte JSON-Verträge:

- `schemas/ai-review-package-v1.schema.json`: Eingabe für einen Reviewer.
- `schemas/ai-review-result-v1.schema.json`: normalisiertes Review-Ergebnis.

Das Review-Paket enthält PR-Identität und Diff, Issue samt Akzeptanzkriterien, relevante Baseline-Regeln und explizit ausgewählten Projektkontext. Provider-Adapter dürfen diesen Vertrag transportieren oder in providerspezifische Requests übersetzen, verändern aber nicht seine Semantik.

## Ergebnis

`PASS` bedeutet keine blockierenden oder warnenden Findings. `WARN` verlangt Aufmerksamkeit, blockiert aber nicht automatisch. `BLOCK` enthält mindestens ein blockierendes Finding und kann als GitHub Quality Gate einen Merge verhindern.

Jedes Finding besitzt Schweregrad, Nachricht und eine nachvollziehbare Fundstelle; optional kann eine Baseline-Regel referenziert werden.

## Trennung von Review und Verfügbarkeit

Ein nicht erreichbarer Provider ist **kein** `BLOCK`-Review. Provider-Verfügbarkeit und deren Gate-Policy werden separat modelliert. Dadurch kann ein technischer Ausfall nicht als fachliches Review-Ergebnis erscheinen.

## Erweiterbarkeit

Reviewer-Metadaten nennen Adapter und Modell, ohne providerspezifische Felder im Kernschema vorauszusetzen. Mehrere Adapter oder Cross-Provider-Reviews können deshalb später auf demselben Paket und Ergebnisvertrag aufsetzen.
