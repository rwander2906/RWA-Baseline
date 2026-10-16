# Anwenderdokumentation

## Mindeststandard

Auslieferbare Anwendungen enthalten eine Anwenderdokumentation unter `docs/user/`. Sie richtet sich an tatsächliche Nutzer und ist von Entwicklerdokumentation getrennt.

Soweit für den Anwendungstyp relevant, beschreibt sie:
- Installation bzw. Bezug und Start der Anwendung
- grundlegende Bedienung und zentrale Arbeitsabläufe
- relevante, durch Anwender oder Administratoren vorzunehmende Konfiguration
- typische Fehlerbilder, Selbsthilfe und Supporthinweise
- Version oder Gültigkeitsstand der beschriebenen Anwendung

`docs/user/README.md` ist der verpflichtende Einstiegspunkt. Sichtbare Funktionsänderungen aktualisieren die Anwenderdokumentation im selben Issue/PR. Release- und Nutzerpakete enthalten die erforderliche Anwenderdokumentation.

Die ausgelieferte Dokumentation enthält keine kundenspezifischen Daten, Secrets, Tokens, produktiven Zugangsdaten oder lokale Entwicklerkonfigurationen.

## Screenshots

Screenshots der Anwenderdokumentation werden als einzelne Bilddateien unter `docs/user/screenshots/` versioniert. Sie werden nicht in ZIP-Dateien versteckt und nicht als undokumentierte Binärdateien an anderer Stelle abgelegt.

Ein bestehender Screenshot behält einen stabilen, beschreibenden Dateinamen und wird bei einer Aktualisierung unter diesem Namen ersetzt. Nicht mehr verwendete Screenshots werden entfernt.

Wenn bei Entwicklung, Review oder Dokumentationspflege ein neuer oder aktualisierter Screenshot erforderlich ist und die AI ihn nicht zuverlässig aus dem realen Anwendungszustand erzeugen kann, fordert die AI ihn über ein GitHub Issue oder Subissue an. Diese Anforderung nennt mindestens:
- exakten Dateinamen
- Ablageort `docs/user/screenshots/`
- darzustellenden Anwendungszustand bzw. Bildinhalt
- Verwendungsstelle in der Anwenderdokumentation

Der reale Screenshot wird durch einen Menschen bereitgestellt. Die AI darf ihn anschließend in die Dokumentation integrieren und die Referenzen pflegen.

## Release-Gate

Vor einem Release muss maschinell geprüft werden:
- `docs/user/README.md` existiert und enthält die Mindeststruktur
- alle aus der Anwenderdokumentation lokal referenzierten Dateien existieren
- referenzierte Screenshots liegen unter `docs/user/screenshots/`
- offensichtliche Secret-Dateien werden nicht als Dokumentationsbestandteil ausgeliefert

Fehlende oder inkonsistente Anwenderdokumentation blockiert den Release. Projektspezifisch nicht relevante Inhalte dürfen als nicht anwendbar dokumentiert werden; das Vorhandensein der Anwenderdokumentation selbst ist für auslieferbare Anwendungen nicht optional.
