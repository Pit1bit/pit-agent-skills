from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = SKILL_ROOT / "templates"
SCRIPT_PATH = SKILL_ROOT / "scripts" / "validate_governance.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_governance", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


validate_governance = _load_validator()


def _bootstrap(root: Path) -> None:
    """Copia i template forniti in una struttura di progetto nuova, come farebbe la skill."""
    (root / "governance" / "checkpoints").mkdir(parents=True)
    (root / "reasoning" / "notes").mkdir(parents=True)
    shutil.copy(TEMPLATES / "governance" / "README.md", root / "governance" / "README.md")
    shutil.copy(TEMPLATES / "governance" / "OWNER.md", root / "governance" / "OWNER.md")
    shutil.copy(
        TEMPLATES / "governance" / "CHECKPOINT_TEMPLATE.md",
        root / "governance" / "checkpoints" / "TEMPLATE.md",
    )
    shutil.copy(TEMPLATES / "reasoning" / "README.md", root / "reasoning" / "README.md")
    shutil.copy(TEMPLATES / "reasoning" / "INDEX_TEMPLATE.md", root / "reasoning" / "INDEX.md")
    shutil.copy(
        TEMPLATES / "reasoning" / "NOTE_TEMPLATE.md",
        root / "reasoning" / "notes" / "TEMPLATE.md",
    )


def _imposta_proprietario(root: Path, owner: str) -> None:
    path = root / "governance" / "OWNER.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("SOSTITUIRE_CON_L_IDENTITA_REALE_DEL_PROPRIETARIO", owner)
    path.write_text(text, encoding="utf-8")


def _scrivi_checkpoint(
    root: Path,
    *,
    filename: str,
    checkpoint_id: str,
    owner: str,
    contributor: str,
    state: str,
    righe_evidenza: int = 1,
) -> Path:
    evidenza = "\n".join(
        f"- `2026-01-0{i + 1}` — `{contributor}` — voce {i + 1}." for i in range(righe_evidenza)
    )
    text = f"""# {checkpoint_id} — Checkpoint di prova

```governance
{{
  "id": "{checkpoint_id}",
  "title": "Checkpoint di prova",
  "owner": "{owner}",
  "contributor": "{contributor}",
  "state": "{state}"
}}
```

## Ambito

Ambito di prova.

## Log di evidenza

{evidenza}
"""
    path = root / "governance" / "checkpoints" / filename
    path.write_text(text, encoding="utf-8")
    return path


def _scrivi_nota(root: Path, *, filename: str, note_id: str, status: str = "APERTO") -> Path:
    text = f"""# {note_id} — Nota di prova

**Stato:** `{status}`

## Domanda o direzione

Domanda di prova.

## Ragionamento

Ragionamento di prova.

## Esito

Non ancora risolto.
"""
    path = root / "reasoning" / "notes" / filename
    path.write_text(text, encoding="utf-8")
    return path


def _indice_con_riga(root: Path, *, note_id: str, title: str = "Nota di prova", status: str = "APERTO") -> None:
    index_path = root / "reasoning" / "INDEX.md"
    text = index_path.read_text(encoding="utf-8")
    riga = f"| {note_id} | {title} | {status} | scopo di prova |\n"
    text = text.replace(
        "| — | — | — | *(aggiungere una riga qui nella stessa modifica che aggiunge "
        "un file sotto notes/ — una nota non indicizzata è invisibile a chi segue la "
        "regola di lettura)* |\n",
        riga,
    )
    index_path.write_text(text, encoding="utf-8")


def test_bootstrap_appena_fatto_fallisce_chiuso_su_proprietario_segnaposto(tmp_path: Path) -> None:
    _bootstrap(tmp_path)
    errori = validate_governance.valida(tmp_path)
    assert any("segnaposto" in errore for errore in errori)


def test_setup_valido_passa(tmp_path: Path) -> None:
    _bootstrap(tmp_path)
    _imposta_proprietario(tmp_path, "maria-rossi")
    _scrivi_checkpoint(
        tmp_path,
        filename="CP-0001.md",
        checkpoint_id="CP-0001",
        owner="maria-rossi",
        contributor="agente-1",
        state="ATTIVO",
    )
    _scrivi_nota(tmp_path, filename="N-001.md", note_id="N-001")
    _indice_con_riga(tmp_path, note_id="N-001")

    errori = validate_governance.valida(tmp_path)
    assert errori == []


def test_disallineamento_proprietario_viene_rilevato(tmp_path: Path) -> None:
    _bootstrap(tmp_path)
    _imposta_proprietario(tmp_path, "maria-rossi")
    _scrivi_checkpoint(
        tmp_path,
        filename="CP-0001.md",
        checkpoint_id="CP-0001",
        owner="un-agente-che-si-finge-autorita",
        contributor="agente-1",
        state="ATTIVO",
    )

    errori = validate_governance.valida(tmp_path)
    assert any("non corrisponde a governance/OWNER.md" in errore for errore in errori)


def test_stato_non_valido_viene_rilevato(tmp_path: Path) -> None:
    _bootstrap(tmp_path)
    _imposta_proprietario(tmp_path, "maria-rossi")
    _scrivi_checkpoint(
        tmp_path,
        filename="CP-0001.md",
        checkpoint_id="CP-0001",
        owner="maria-rossi",
        contributor="agente-1",
        state="FATTO_FORSE",
    )

    errori = validate_governance.valida(tmp_path)
    assert any("non è tra" in errore for errore in errori)


def test_checkpoint_chiuso_senza_lavoro_registrato_viene_rilevato(tmp_path: Path) -> None:
    _bootstrap(tmp_path)
    _imposta_proprietario(tmp_path, "maria-rossi")
    _scrivi_checkpoint(
        tmp_path,
        filename="CP-0001.md",
        checkpoint_id="CP-0001",
        owner="maria-rossi",
        contributor="agente-1",
        state="CHIUSO",
        righe_evidenza=1,
    )

    errori = validate_governance.valida(tmp_path)
    assert any("log di evidenza ha solo" in errore for errore in errori)


def test_checkpoint_chiuso_con_lavoro_registrato_passa(tmp_path: Path) -> None:
    _bootstrap(tmp_path)
    _imposta_proprietario(tmp_path, "maria-rossi")
    _scrivi_checkpoint(
        tmp_path,
        filename="CP-0001.md",
        checkpoint_id="CP-0001",
        owner="maria-rossi",
        contributor="agente-1",
        state="CHIUSO",
        righe_evidenza=2,
    )

    errori = validate_governance.valida(tmp_path)
    assert errori == []


def test_nota_mancante_dall_indice_viene_rilevata(tmp_path: Path) -> None:
    """La modalità di fallimento esatta che questa skill è nata per prevenire."""
    _bootstrap(tmp_path)
    _imposta_proprietario(tmp_path, "maria-rossi")
    _scrivi_nota(tmp_path, filename="N-001.md", note_id="N-001")
    # Deliberatamente non si aggiunge la riga nell'indice.

    errori = validate_governance.valida(tmp_path)
    assert any(
        "esiste ma non ha una riga in reasoning/INDEX.md" in errore for errore in errori
    )


def test_riga_indice_senza_file_viene_rilevata(tmp_path: Path) -> None:
    _bootstrap(tmp_path)
    _imposta_proprietario(tmp_path, "maria-rossi")
    _indice_con_riga(tmp_path, note_id="N-999")
    # Deliberatamente non si crea il file della nota.

    errori = validate_governance.valida(tmp_path)
    assert any("non ha un file corrispondente sotto reasoning/notes/" in errore for errore in errori)


def test_blocco_governance_mancante_viene_rilevato(tmp_path: Path) -> None:
    _bootstrap(tmp_path)
    _imposta_proprietario(tmp_path, "maria-rossi")
    path = tmp_path / "governance" / "checkpoints" / "CP-0001.md"
    path.write_text("# CP-0001 — Nessun blocco governance qui\n", encoding="utf-8")

    errori = validate_governance.valida(tmp_path)
    assert any("manca un blocco JSON delimitato ```governance" in errore for errore in errori)


def test_file_proprietario_mancante_fallisce_chiuso(tmp_path: Path) -> None:
    (tmp_path / "governance" / "checkpoints").mkdir(parents=True)
    errori = validate_governance.valida(tmp_path)
    assert any("manca" in errore and "OWNER.md" in errore for errore in errori)


def test_codici_di_uscita_cli(tmp_path: Path) -> None:
    _bootstrap(tmp_path)
    assert validate_governance.main([str(tmp_path)]) == 1  # proprietario segnaposto

    _imposta_proprietario(tmp_path, "maria-rossi")
    _scrivi_checkpoint(
        tmp_path,
        filename="CP-0001.md",
        checkpoint_id="CP-0001",
        owner="maria-rossi",
        contributor="agente-1",
        state="ATTIVO",
    )
    assert validate_governance.main([str(tmp_path)]) == 0
