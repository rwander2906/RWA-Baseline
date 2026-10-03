# Development Workflow

## Grundsatz

Jede fachliche Änderung, jeder Bugfix und jede technische Verbesserung beginnt mit einem GitHub Issue.

Ein Issue beschreibt mindestens Ziel, Scope, Akzeptanzkriterien sowie relevante automatische und manuelle Tests.

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
manueller Smoke-Test, falls erforderlich
  ↓
explizite Freigabe der Promotion
  ↓
Promotion staging → main
  ↓
Release / Deployment
```

## Branches

Standard für Arbeitsbranches:

`issue/<nummer>-<kurzname>`

Direkte fachliche Änderungen auf `staging` oder `main` sind zu vermeiden.

## Promotion nach main

`staging` ist Integrationsstand und darf mehrere abgeschlossene Änderungen enthalten. Eine Promotion nach `main` erfolgt ausschließlich nach expliziter Freigabe für die konkrete Promotion.

Empfohlen ist ein maschinelles Promotion-Gate, z. B. über ein PR-Label `promotion-approved`.

## Kleine Änderungen

Reine Tippfehler oder Formatkorrekturen dürfen innerhalb eines bereits offenen Issues mit erledigt werden. Änderungen an Verhalten, Architektur, Build, CI oder verbindlicher Dokumentation erhalten ein eigenes Issue.
