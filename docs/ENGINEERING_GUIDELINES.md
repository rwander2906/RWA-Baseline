# Engineering Guidelines

## 1. Grundprinzipien

Code muss verständlich, testbar, wartbar und möglichst selbsterklärend sein. Lesbarkeit hat Vorrang vor cleveren Kurzlösungen. Änderungen bleiben klein, thematisch klar und nachvollziehbar.

## 2. Verantwortlichkeiten

Funktionen, Klassen und Module sollen eine klar erkennbare Verantwortung besitzen. Fachlogik wird von Netzwerk, Dateisystem, UI, Persistenz und externen Diensten getrennt. Pure Functions sind zu bevorzugen.

Richtwerte für Funktionen:
- möglichst 40–60 Zeilen oder weniger
- möglichst maximal drei Verschachtelungsebenen
- Guard Clauses und frühe Returns bevorzugen

Richtwerte sind keine mechanischen Hard Limits. Abweichungen müssen fachlich begründbar sein.

## 3. Benennung

Namen beschreiben Zweck und Verhalten. Nichtssagende Namen wie `tmp`, `data2`, `foo` oder `bar` sind außerhalb sehr lokaler Kontexte zu vermeiden. Boolesche Werte sollen möglichst als Frage lesbar sein.

## 4. Eingaben und Validierung

Externe Eingaben gelten als nicht vertrauenswürdig. Dazu gehören insbesondere Benutzerparameter, Konfiguration, Dateien, API-Antworten, AI-Ausgaben und Netzwerkdaten. Eingaben werden vor Nutzung validiert und, wo sinnvoll, normalisiert.

## 5. Fehlerbehandlung

Fehler dürfen nicht unbemerkt verschwinden. Jeder Fehlerpfad muss mindestens einen kontrollierten Zweck erfüllen: sinnvolles Logging, definierter Fallback, fachliche Fehlerübersetzung oder bewusst dokumentiertes Ignorieren. Leere Catch-/Except-Blöcke sind verboten.

## 6. Persistenz

Persistente Dateien sollen atomar geschrieben werden. Ein fehlgeschlagener Schreibvorgang darf einen zuvor gültigen Zustand nicht beschädigen. Schemaänderungen sollen möglichst rückwärtskompatibel und migrationsfähig sein.

## 7. Abhängigkeiten

Neue Dependencies werden nur aufgenommen, wenn ihr Nutzen den Wartungsaufwand rechtfertigt. Vor Aufnahme sind Wartungszustand, Security, Lizenz, transitive Abhängigkeiten und vorhandene Alternativen zu prüfen.

## 8. Dead Code

Nicht mehr verwendeter Code wird gelöscht. Git ist die Historie. Auskommentierte Altimplementierungen, dauerhaft deaktivierte Codeblöcke und ungenutzte Imports/Parameter werden nicht als Archiv im Quelltext behalten.

## 9. Backward Compatibility

Breaking Changes werden bewusst beschlossen, dokumentiert, versioniert und nach Möglichkeit migrationsfähig umgesetzt.
