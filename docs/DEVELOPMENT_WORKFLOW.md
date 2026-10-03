# Development Workflow

## Grundsatz

Jede fachliche Änderung, jeder Bugfix und jede technische Verbesserung beginnt mit einem GitHub Issue.

Ein Issue beschreibt mindestens Ziel, Scope, Akzeptanzkriterien sowie relevante automatische und manuelle Tests. Offene Arbeit wird nicht dauerhaft in separaten TODO-Dateien oder Chat-Verläufen geführt.

## Source of Truth

Die Rollen sind eindeutig getrennt:

- **Issue:** Problem, Ziel, Scope, Akzeptanzkriterien und offene Arbeit
- **Pull Request:** konkrete Umsetzung, technische Entscheidungen im Änderungskontext und durchgeführte Tests
- **docs/** und **ADRs:** dauerhaft relevantes technisches Wissen und Architekturentscheidungen
- **CHANGELOG:** ausgelieferte, für Nutzung oder Betrieb relevante Änderungen
- **GitHub Project/Backlog:** Priorisierung und Arbeitsstatus, falls eingesetzt

## Standardablauf

```text
Issue
  ↓
issue/<nummer>-<kurzname>
  ↓
Implementierung + Tests + Dokumentation
  ↓
Pull Request nach staging
  ↓
CI vollständig grün
  ↓
manueller Smoke-/Staging-Test, falls erforderlich
  ↓
explizite Freigabe der Promotion
  ↓
Promotion staging → main
  ↓
Release / Deployment
  ↓
Issue schließen
```

## Branches

Standard für Arbeitsbranches:

`issue/<nummer>-<kurzname>`

Direkte fachliche Änderungen auf `staging` oder `main` sind zu vermeiden. Arbeitsbranches werden von `staging` erstellt und nach erfolgreichem Merge gelöscht.

## Pull Requests und Issue-Status

Der Arbeits-PR nach `staging` referenziert das Issue mit `Refs #N`. Er schließt es nicht automatisch.

Ein Issue gilt fachlich erst als erledigt, wenn die Änderung nach `main` promotet wurde und ein erforderliches Release/Deployment erfolgreich war. Die Promotion darf das Issue mit `Closes #N` schließen.

Damit bleibt sichtbar, welche Änderungen zwar integriert und getestet, aber noch nicht produktions- bzw. release-reif sind.

## Promotion nach main

`staging` ist Integrationsstand und darf mehrere abgeschlossene Änderungen enthalten. Eine Promotion nach `main` erfolgt ausschließlich nach expliziter Freigabe für die konkrete Promotion.

Ein maschinelles Promotion-Gate ist verbindlich. Empfohlen wird ein PR-Label `promotion-approved`, das nur nach ausdrücklicher Freigabe gesetzt wird.

## Kleine Änderungen

Reine Tippfehler oder Formatkorrekturen dürfen innerhalb eines bereits offenen Issues mit erledigt werden. Änderungen an Verhalten, Architektur, Build, CI oder verbindlicher Dokumentation erhalten ein eigenes Issue.
