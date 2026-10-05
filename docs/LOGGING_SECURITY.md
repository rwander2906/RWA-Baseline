# Logging & Security

## Logging

Projekte verwenden einen zentralen Logging-Pfad. Ad-hoc-Debug-Ausgaben dürfen nicht zum parallelen Logging-System werden.

Logs liefern technischen und fachlichen Kontext, ohne unnötige Nutzdaten zu enthalten. Log-Level werden projektweit konsistent verwendet:

- **ERROR:** Vorgang fehlgeschlagen oder nicht fortsetzbar
- **WARNING:** unerwarteter Zustand/Fallback, Verarbeitung läuft weiter
- **INFO:** relevante Lebenszyklus- oder Prozessereignisse
- **DEBUG:** technische Diagnose
- **TRACE:** sehr detaillierte Ablaufdiagnose, falls der Stack dies unterstützt

## Secrets

Passwörter, Tokens, API-Keys, Authorization-Header und vergleichbare Secrets dürfen niemals geloggt oder im Repository eingecheckt werden.

Secrets werden über geeignete Secret Stores, CI-Secrets oder lokale, ignorierte Konfiguration bereitgestellt. Beispielkonfigurationen enthalten ausschließlich neutrale Platzhalter.

## Datenschutz

Personenbezogene oder sensible Inhalte werden nur geloggt, wenn dies zwingend erforderlich und ausdrücklich vertretbar ist. Wo möglich werden IDs reduziert, abstrahiert oder maskiert.

Rohdaten externer Systeme, vollständige Freitexte und komplette Request-/Response-Payloads sind standardmäßig nicht zu loggen.

## Exceptions

Exceptions werden nicht verschluckt. Fehlermeldungen enthalten ausreichenden technischen Kontext, ohne externe Exceptiontexte ungeprüft zu übernehmen, wenn diese sensible Daten enthalten könnten.

## Externe/AI-Daten

Ausgaben externer Systeme oder AI-Modelle dürfen nicht ungeprüft als Berechtigung, Identität, Sicherheitsentscheidung oder persistenter Konfigurationszustand übernommen werden. Dazwischen liegt eine deterministische Validierung.

## Dependency- und Supply-Chain-Sicherheit

Abhängigkeiten werden automatisiert auf bekannte Schwachstellen geprüft. Automatisierte Dependency-Updates (z. B. Dependabot oder äquivalent) sind für aktiv gepflegte Projekte einzurichten.

Build- und CI-Aktionen sollen auf nachvollziehbare Versionen festgelegt werden. Berechtigungen von CI-Workflows folgen dem Least-Privilege-Prinzip.

Dependabot-Befunde werden zusätzlich zum automatisch erzeugten Pull Request als verknüpfte GitHub-Issues dokumentiert. So bleiben Dependency- und Security-Arbeiten im normalen Issue-Backlog nachvollziehbar, auch wenn der technische PR später geschlossen oder ersetzt wird.

## Security-relevante Änderungen

Änderungen an Authentifizierung, Autorisierung, Secrets, Persistenz, Datenschutz, Rollen/Rechten, Stage-Routing oder sicherheitsrelevanter Validierung benötigen explizite Tests.
