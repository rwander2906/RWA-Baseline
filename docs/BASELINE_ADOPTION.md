# Baseline Adoption & Upgrade

Jedes Projekt dokumentiert die verwendete RWA-Baseline-Version in `.rwa-baseline.yml`.

## Erstmalige Adoption

1. aktuelle Projektregeln, CI und Repository-Einstellungen erfassen
2. gegen die Zielversion der Baseline vergleichen
3. Lücken und Abweichungen klassifizieren
4. sofort umsetzbare Punkte übernehmen
5. größere technische Schulden als Issues erfassen
6. begründete Ausnahmen in `.rwa-baseline.yml` dokumentieren
7. Baseline-Version als adoptiert markieren

Eine Adoption verlangt nicht, dass ein Legacy-Projekt sofort jeden Zielwert erfüllt. Sie verlangt, dass jede Abweichung entweder behoben, als technische Schuld erfasst oder ausdrücklich begründet ist.

## Upgrade auf neue Baseline-Version

Bei neuer Minor-/Major-Version:

1. Changelog/Migrationshinweise seit der bisher adoptierten Version lesen
2. Diff zur Zielversion bestimmen
3. Upgrade-Issue anlegen
4. notwendige Änderungen umsetzen
5. Ausnahmen neu bewerten und aktualisieren
6. `.rwa-baseline.yml` auf neue Version setzen
7. Compliance-Check ausführen

Patch-Versionen sollen ohne größere Migrationsarbeit adoptierbar sein.

## Ausnahmen

Eine Ausnahme enthält mindestens:

- stabile Regel-ID
- abweichenden Wert oder Zustand
- Begründung
- verantwortliches Projekt/Profil, falls nötig
- Issue, wenn die Ausnahme abgebaut werden soll

Ausnahmen sind keine dauerhafte Parallel-Norm. Sie werden bei jedem Baseline-Upgrade erneut geprüft.

## Regel-IDs

Verbindliche oder maschinenprüfbare Regeln sollen langfristig stabile IDs erhalten, damit Compliance-Checks und Ausnahmen nicht an Dateinamen oder Textformulierungen gekoppelt sind.
