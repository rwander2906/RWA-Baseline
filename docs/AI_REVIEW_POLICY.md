# AI Review Policy

Die Policy ist eine eigene Schicht oberhalb der Provider-Adapter. Ein fachliches Review-Ergebnis (`PASS`, `WARN`, `BLOCK`) wird niemals mit technischer Provider-Verfügbarkeit vermischt.

## Modi

- `advisory` (Default): AI Review ergänzt die Qualitätssicherung. Ein Provider-Ausfall führt mit der Default-Ausfallregel `fail-open` zu `WARN`, nicht zu einem fachlichen `BLOCK`.
- `required`: mindestens ein abgeschlossenes Review ist erforderlich. Fehlt jedes Review, blockiert die Policy mit dem technischen Grund `required-review-missing`.

## Provider-Ausfall

- `fail-open` (Default): Entwicklung bleibt bei Provider-Störungen möglich; die Policy meldet `WARN`.
- `fail-closed`: ein technischer Ausfall blockiert das Gate mit dem Grund `provider-unavailable`. Er wird ausdrücklich nicht als Reviewer-`BLOCK` ausgegeben.

## Mehrere Reviewer

Alle normalisierten Ergebnisse können mit derselben Policy aggregiert werden. Ein `BLOCK` eines Reviewers bei gleichzeitigem `PASS` oder `WARN` eines anderen Reviewers ergibt standardmäßig `HUMAN_REQUIRED`. Damit entscheidet bei substantiellem Reviewer-Dissens ein Mensch. Projekte können diese Dissensregel explizit deaktivieren; dann gilt ein vorhandenes `BLOCK`.

Mehrere Adapter und Cross-Provider-Reviews benötigen keine Änderung des Review-Vertrags. Jeder Adapter erzeugt ein normales Review-Ergebnis; erst die Policy aggregiert diese Ergebnisse.

## Unabhängigkeit

Build, Tests, Linting, Packaging und Produktlaufzeit dürfen diese Policy nicht benötigen. Sie gehört ausschließlich zur zusätzlichen Review-/Merge-Schicht.
