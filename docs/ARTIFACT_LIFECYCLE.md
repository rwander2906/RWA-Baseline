# GitHub Actions: Artifact Lifecycle

## Grundregel

`actions/upload-artifact` ist **kein Archiv**. Erzeuge und prüfe Artefakte innerhalb
desselben Jobs ohne Upload. Veröffentliche dauerhaft benötigte Ergebnisse direkt
in GitHub Releases oder, falls ausdrücklich nötig, im versionierten Repository.
Binärarchive sollten möglichst nicht in die Git-Historie eingecheckt werden.

## Ausnahmen

Bei tatsächlichem Datentransfer zwischen Jobs oder zeitlich begrenzten Diagnosepaketen
ist ein Upload zulässig. Markiere den Upload-Schritt ausdrücklich mit
`# artifact-lifecycle: cross-job` oder `# artifact-lifecycle: diagnostic`
und verwende `retention-days: 1` (höchstens 3). Der CI-Check
`scripts/check_artifact_lifecycle.py` verhindert vergessene Ausnahmen und
lange Aufbewahrung. Er ersetzt keine manuelle Prüfung des tatsächlichen Bedarfs.

## Aufräumen nach erfolgreicher Veröffentlichung

Wo ein Cross-Job-Upload unvermeidbar ist, darf er **erst nach dem letzten Download**
und **nach expliziter Verifikation der Veröffentlichung** gelöscht werden.
`actions/upload-artifact@v4+` gibt `artifact-id` zurück. Übergib diese ID
über Job-Outputs an einen nachfolgenden Cleanup-Job. Verwende den minimalen
Job-Token-Scope `actions: write` und lösche ausschließlich diese ID der
aktuellen Ausführung:

```yaml
# Im Upload-Job:
- id: package
  # artifact-lifecycle: cross-job
  uses: actions/upload-artifact@v4
  with:
    name: package
    path: dist/package.zip
    retention-days: 1
# Job-Output: artifact_id: ${{ steps.package.outputs.artifact-id }}

# Im nachfolgenden Cleanup-Job, erst nach erfolgreicher, verifizierter
# Veröffentlichung und nach sämtlichen Downloads:
permissions:
  actions: write
  contents: read
steps:
  - name: Delete this run's published temporary artifact
    env:
      GH_TOKEN: ${{ github.token }}
      ARTIFACT_ID: ${{ needs.build.outputs.artifact_id }}
    run: |
      test -n "$ARTIFACT_ID"
      gh api --method DELETE "repos/$GITHUB_REPOSITORY/actions/artifacts/$ARTIFACT_ID"
```

Dies ist ein Integrationsmuster, kein direkt lauffähiger vollständiger Workflow.
`needs`, Job-Outputs und Publikationsverifikation müssen projektspezifisch
verbunden werden. Kein pauschales Löschen fremder Runs; bei fehlgeschlagener
Veröffentlichung darf der Cleanup-Job nicht anlaufen. Fehler im Cleanup melden
und protokollieren.

## Regelmäßige Kontrolle

Die GitHub-Billing-Anzeige für Actions Storage regelmäßig prüfen. Bestehende
Artefakte werden durch neue Retention-Regeln nicht nachträglich gelöscht.
Ein separater manueller, berechtigungsbeschränkter Bereinigungslauf ist
nur bei Bedarf sinnvoll.
