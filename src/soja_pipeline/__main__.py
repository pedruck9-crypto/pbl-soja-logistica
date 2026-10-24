"""Prepara a estrutura inicial; cálculos analíticos ainda não implementados."""
from pathlib import Path
def main() -> int:
    root = Path(__file__).resolve().parents[2]
    folders = (
        "data/originais",
        "data/hipoteses",
        "data/tratados",
        "data/resultados",
        "config",
        "docs",
    )
    for name in folders:
        (root / name).mkdir(parents=True, exist_ok=True)
    print("Estrutura do projeto verificada e pastas preparadas.")
    print("Pipeline de importação e cálculos ainda não implementado.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
