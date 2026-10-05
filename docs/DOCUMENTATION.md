# Documentation Standard

Dokumentation ist Teil des Produkts und Teil der Definition of Done.

## Developer Handover

Die Dokumentation muss einem kompetenten Entwickler ohne Projektvorgeschichte ermöglichen, das Projekt aus einem frischen Clone zu verstehen und arbeitsfähig zu bekommen. Kritische Schritte dürfen nicht nur in Chatverläufen, Prompts, persönlichen Notizen oder implizitem Teamwissen existieren.

## Mindestbestand eines Projekts

- README mit Zweck, Voraussetzungen, Installation, Konfiguration, Start, Tests und reproduzierbarem Build
- Coding-/Projekt-Guidelines oder Verweis auf die RWA Baseline
- Entwicklungsworkflow
- relevante Architekturübersicht
- Changelog für ausgelieferte Änderungen
- projektspezifische Betriebs-/Build-/Release-Hinweise, soweit erforderlich

## Code-Dokumentation

Öffentliche und fachlich relevante Funktionen, Klassen und Module erhalten die für den Stack übliche strukturierte Dokumentation (z. B. JSDoc oder Docstrings).

Kommentare erklären primär **warum**, nicht das Offensichtliche.

## Architekturentscheidungen

Wesentliche, langfristig wirksame Architekturentscheidungen werden als ADR oder vergleichbar nachvollziehbar dokumentiert. Ein ADR ist insbesondere sinnvoll, wenn ein späterer Entwickler die Entscheidung und ihre Begründung nicht zuverlässig aus Code und aktueller Dokumentation ableiten könnte. Routine-Implementierungsdetails benötigen kein ADR.
