# Baseline Adoption & Upgrade

Jedes Projekt dokumentiert die verwendete RWA-Baseline-Version in `.rwa-baseline.yml`.

## Erstmalige Adoption

1. aktuelle Projektregeln und CI erfassen
2. gegen Baseline vergleichen
3. Lücken und Abweichungen klassifizieren
4. sofort umsetzbare Punkte übernehmen
5. größere technische Schulden als Issues erfassen
6. begründete Ausnahmen in `.rwa-baseline.yml` dokumentieren
7. Baseline-Version als adoptiert markieren

## Upgrade auf neue Baseline-Version

Bei neuer Minor-/Major-Version:

1. Changelog/Migrationshinweise lesen
2. Diff zur bisher adoptierten Version bestimmen
3. Upgrade-Issue anlegen
4. notwendige Änderungen umsetzen
5. Ausnahmen aktualisieren
6. `.rwa-baseline.yml` auf neue Version setzen

## Ausnahmen

Eine Ausnahme enthält mindestens Regel, abweichenden Wert/Zustand, Begründung und – wenn die Ausnahme abgebaut werden soll – ein Issue.
