# Windows Desktop Release

Die Baseline unterstützt als ersten Desktop-Stack Python-Anwendungen, die mit PyInstaller als Windows-Executable ausgeliefert werden.

## Vertrag

Das Desktop-Profil baut ausschließlich aus dem freigegebenen `main`-Stand bzw. über einen explizit gestarteten Release-Workflow. Der Build läuft auf `windows-latest`, verwendet die gepinnten Abhängigkeiten aus `requirements-build.txt` und erzeugt das Executable aus `desktop.spec`.

Die Anwendung muss `--version` unterstützen. Der Smoke-Test startet das erzeugte Executable mit diesem Parameter. Die ausgegebene Version muss dem Inhalt von `VERSION` entsprechen bzw. daraus abgeleitet sein.

Das Nutzerpaket enthält:
- das erzeugte Windows-Executable
- die Anwenderdokumentation aus `docs/user/`
- einen versionsbezogenen Paketnamen

Das ZIP wird als GitHub Actions Artefakt bereitgestellt. Release-Binaries werden nicht manuell auf Entwicklerrechnern erzeugt und nicht als Ersatz für den automatisierten Release-Prozess in `bin/` oder an anderer Stelle eingecheckt.

## Projektanpassung

Das Bootstrap-Artefakt verwendet bewusst `app.exe` und `desktop.spec` als neutrale Startwerte. Ein Desktop-Projekt passt Name, Entry Point und PyInstaller-Spec im ersten projektbezogenen Issue an; der Release-Vertrag, Smoke-Test und die Dokumentationsbeigabe bleiben erhalten.
