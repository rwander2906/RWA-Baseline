# Logging & Security

## Logging

Projekte verwenden einen zentralen Logging-Pfad. Ad-hoc-Debug-Ausgaben dürfen nicht zum parallelen Logging-System werden.

Logs sollen technischen und fachlichen Kontext liefern, ohne unnötige Nutzdaten zu enthalten.

## Secrets

Passwörter, Tokens, API-Keys, Authorization-Header und vergleichbare Secrets dürfen niemals geloggt oder im Repository eingecheckt werden.

Secrets werden über geeignete Secret Stores, CI-Secrets oder lokale, ignorierte Konfiguration bereitgestellt.

## Datenschutz

Personenbezogene oder sensible Inhalte werden nur geloggt, wenn dies zwingend erforderlich und ausdrücklich vertretbar ist. Wo möglich werden IDs reduziert, abstrahiert oder maskiert.

## Externe/AI-Daten

Ausgaben externer Systeme oder AI-Modelle dürfen nicht ungeprüft als Berechtigung, Identität, Sicherheitsentscheidung oder persistenter Konfigurationszustand übernommen werden. Dazwischen liegt eine deterministische Validierung.

## Security-relevante Änderungen

Änderungen an Authentifizierung, Autorisierung, Secrets, Persistenz, Datenschutz, Rollen/Rechten oder sicherheitsrelevanter Validierung benötigen explizite Tests.
