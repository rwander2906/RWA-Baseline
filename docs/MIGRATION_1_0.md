# Migration auf RWA Baseline 1.0

Diese Checkliste ist für bestehende Projekte gedacht, die auf die erste stabile RWA Baseline adoptiert werden.

## 1. Projektdeklaration

- [ ] `.rwa-baseline.yml` anlegen
- [ ] Zielversion `1.0.0` eintragen
- [ ] Technologieprofil festlegen
- [ ] Abweichungen explizit dokumentieren

## 2. Entwicklungsworkflow

- [ ] offene Arbeit wird über GitHub Issues geführt
- [ ] Arbeitsbranch wird von `staging` erstellt
- [ ] Arbeits-PR zielt auf `staging`
- [ ] Arbeits-PR verwendet `Refs #N` statt automatischem Schließen
- [ ] Issue wird erst mit Promotion nach `main` geschlossen
- [ ] Promotion nach `main` benötigt ausdrückliche Freigabe
- [ ] maschinelles Promotion-Gate vorhanden
- [ ] gemergte Arbeitsbranches werden gelöscht

## 3. CI und Qualität

- [ ] reproduzierbare Dependency-Installation
- [ ] Linting/statische Analyse als Gate
- [ ] Syntax/Compile-Prüfung, soweit anwendbar
- [ ] automatisierte Tests
- [ ] Coverage-Gate
- [ ] Complexity-Gate
- [ ] Dependency-/Security-Prüfung
- [ ] CI-Berechtigungen nach Least Privilege
- [ ] keine neuen Warnings

### Legacy-Projekte

Wenn Zielwerte noch nicht erreicht werden:

- [ ] Istwert dokumentieren
- [ ] Baseline/Ratchet in CI festlegen
- [ ] Verschlechterungen blockieren
- [ ] Verbesserungen in die Baseline übernehmen
- [ ] technische Schulden als Issues erfassen

## 4. Security, Logging und Datenschutz

- [ ] zentraler Logging-Pfad
- [ ] keine Secrets im Repository oder Log
- [ ] keine unnötigen Rohdaten/Freitexte im Log
- [ ] Exceptiontexte externer Systeme nicht ungeprüft loggen
- [ ] Security-relevante Änderungen explizit testen
- [ ] automatisierte Dependency-Updates einrichten

## 5. Architektur und Persistenz

- [ ] Fachlogik von UI, Netzwerk, Persistenz und externen Diensten trennen
- [ ] persistente Dateischreibvorgänge atomar ausführen
- [ ] Staging- und Production-Zustände standardmäßig trennen
- [ ] Shared State dokumentieren und begründen
- [ ] Breaking Changes dokumentieren und migrationsfähig gestalten

## 6. Dokumentation

- [ ] README vollständig
- [ ] Architekturübersicht vorhanden
- [ ] projektspezifische Guidelines verweisen auf Baseline statt allgemeine Regeln zu duplizieren
- [ ] wesentliche Architekturentscheidungen als ADR oder vergleichbar dokumentieren
- [ ] Changelog und Release-Regeln vorhanden

## 7. Release und Artefakte

- [ ] Release nur aus freigegebenem `main`
- [ ] reproduzierbarer Build
- [ ] Build-/Release-Artefakte smoke-testen, soweit sinnvoll
- [ ] Nutzerpakete enthalten Doku und neutrale Beispiele
- [ ] keine Kundendaten, Secrets oder lokale Entwicklerkonfigurationen im Paket

## 8. Abschluss

- [ ] Compliance-Differenzen als Issues oder Ausnahmen erfasst
- [ ] erforderliche Refactorings umgesetzt
- [ ] `.rwa-baseline.yml` final auf `1.0.0` gesetzt
- [ ] Adoption im Projekt dokumentiert
