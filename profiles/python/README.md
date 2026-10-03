# Python Profile

Empfohlene Ergänzungen zur Baseline:

- Ruff oder äquivalenter Linter inkl. Docstring-Regeln
- Google-Style-Docstrings oder ein projektweit konsistenter Standard
- `compileall`/Syntaxprüfung in CI
- Coverage-Gate über `coverage.py`/pytest-cov oder äquivalent
- Complexity-Gate, Richtwert max. 12
- Runtime- und Development-Dependencies trennen
- GUI, Netzwerkzugriff, Rendering und Fachlogik trennen
