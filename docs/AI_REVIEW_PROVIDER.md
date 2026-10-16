# AI Review Provider Adapter

Der Harness trennt den neutralen Review-Vertrag vom Provider. Provider werden ausschließlich über eine Adapter-Schnittstelle angesprochen.

Der Adapter `fake` ist deterministisch und dient Pipeline- und Regressionstests. Ein Provider-Ausfall wird als Harness-Status `UNAVAILABLE` transportiert und ausdrücklich nicht als fachliches `BLOCK` interpretiert.

Provider- und Modellwahl sind Laufzeitkonfiguration des Review-Jobs. Secrets gehören ausschließlich in CI-Secrets und niemals in Repository-Dateien. Weitere Provider implementieren dieselbe Adapter-Schnittstelle und normalisieren ihr Ergebnis auf den Vertrag `ai-review-result-v1`; der Core bleibt unverändert.
