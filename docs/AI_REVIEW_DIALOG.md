# AI Review Issue Dialog

Jeder abgeschlossene AI-Code-Review-Lauf wird zusätzlich zur Job Summary im referenzierten Arbeits-Issue dokumentiert. Der Kommentar beginnt mit dem stabilen Marker `<!-- rwa-ai-review -->` und enthält Run, Commit, Reviewer/Modell, Verdict, Policy-Entscheidung und Findings mit Fundstellen.

Damit ist das Issue die dauerhafte fachliche Review-Historie. Menschen und nachfolgende Automatisierung können auf Befunde antworten und Entscheidungen dort nachvollziehbar dokumentieren.

Für Folge-Reviews werden ausschließlich Kommentare mit dem AI-Review-Marker sowie normale Issue-Kommentare in begrenzter Anzahl als Dialogkontext berücksichtigt. Workflow-/Bot-Kommentare anderer Systeme werden nicht ungefiltert in das Review-Paket übernommen. Die Historie wird begrenzt, damit sie nicht unkontrolliert wächst.

Der Workflow benötigt dafür `issues: write`; weitere Schreibrechte werden nicht vergeben.
