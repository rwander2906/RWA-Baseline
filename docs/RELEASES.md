# Releases & Versioning

Anwendungsprojekte verwenden eine nachvollziehbare Versionierung; Semantic Versioning wird empfohlen.

## Changelog

Ein Changelog unterscheidet mindestens `Unreleased` von veröffentlichten Versionen.

Aufgenommen werden:
- neue Funktionen
- sichtbare Verhaltensänderungen
- relevante Bugfixes
- Security-Änderungen
- Breaking Changes und Migrationen
- wichtige Betriebs-/Deployment-Änderungen

Reine Formatierung, interne Refactorings ohne sichtbare Wirkung und generierte Dokumentation müssen normalerweise nicht einzeln im Changelog erscheinen.

Ein Changelog-Eintrag beschreibt die Wirkung, nicht die Implementierungsdetails.

## Version und Release

Versionsangaben in Manifesten, Lockfiles, Build-Metadaten und README müssen, soweit vorhanden, konsistent bleiben.

Ein Release erfolgt erst aus dem freigegebenen `main`-Stand.

## Build- und Release-Artefakte

Build- und Release-Artefakte sollen reproduzierbar erzeugt und, soweit sinnvoll, automatisch smoke-getestet werden.

Nutzerpakete enthalten die für Betrieb und Nutzung erforderlichen Dokumente und neutrale Beispielkonfigurationen, jedoch:
- keine kundenspezifischen Daten
- keine Secrets
- keine lokalen Entwicklerkonfigurationen

Binärartefakte werden nur über einen dokumentierten Build-/Release-Prozess erzeugt und nicht manuell als undokumentierte Einzeldateien verteilt.

## Anwenderdokumentations-Gate

Für auslieferbare Anwendungen ist `docs/user/README.md` Release-Bestandteil. Der Mindeststandard und der Screenshot-Lifecycle sind in `docs/USER_DOCUMENTATION.md` definiert. Fehlende Anwenderdokumentation oder gebrochene lokale Referenzen blockieren einen Release.


## Windows-Desktop-Releases

Für Desktop-Anwendungen gilt zusätzlich der Vertrag aus `docs/WINDOWS_DESKTOP_RELEASE.md`. Das unterstützte Python-Desktop-Profil erzeugt das Windows-Nutzerpaket automatisiert auf `windows-latest`, smoke-testet das Executable und veröffentlicht das versionsbezogene Paket als Build-Artefakt. Manuell erzeugte lokale Binaries sind kein zulässiger Release-Prozess.
