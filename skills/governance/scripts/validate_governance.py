#!/usr/bin/env python3
"""Validatore deterministico, solo strutturale, per governance/ e reasoning/.

Questo script verifica presenza, forma e coerenza incrociata tra i file. Non
giudica mai la qualità di una decisione, la correttezza di un ragionamento o
la solidità di un giudizio umano — solo se i file sono coerenti tra loro e
con la forma minima richiesta.

Il codice di uscita 0 significa che ogni controllo strutturale è passato.
Qualunque altro codice significa che almeno un controllo è fallito; i
messaggi stampati dicono esattamente quale e dove.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

STATI_AMMESSI = {"PROPOSTO", "AUTORIZZATO", "ATTIVO", "BLOCCATO", "CHIUSO"}
STATI_REASONING_AMMESSI = {"APERTO", "CONSOLIDATO", "SUPERATO", "FRONTIERA_CORRENTE"}
PROPRIETARIO_SEGNAPOSTO = "SOSTITUIRE_CON_L_IDENTITA_REALE_DEL_PROPRIETARIO"

BLOCCO_GOVERNANCE_RE = re.compile(r"```governance\s*\n(.*?)\n```", re.DOTALL)
NOTA_ID_RE = re.compile(r"^#\s+(N-\d{3,})\b", re.MULTILINE)
INDICE_RIGA_ID_RE = re.compile(r"\|\s*(N-\d{3,})\s*\|")
STATO_RIGA_RE = re.compile(r"\*\*Stato:\*\*\s*`([A-Z_]+)`")
EVIDENZA_VOCE_RE = re.compile(r"^-\s+`", re.MULTILINE)


class ErroreValidazione(Exception):
    """Sollevato per un singolo fallimento strutturale; il messaggio è per l'utente."""


def _leggi(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ErroreValidazione(f"impossibile leggere {path}: {exc}") from exc


def _carica_proprietario(root: Path) -> str:
    path = root / "governance" / "OWNER.md"
    if not path.is_file():
        raise ErroreValidazione(
            f"manca {path}: deve essere dichiarata un'identità del Proprietario"
        )
    text = _leggi(path)
    match = re.search(r"\*\*Identità del Proprietario:\*\*\s*`([^`]+)`", text)
    if not match:
        raise ErroreValidazione(
            f"{path}: non trovo una riga 'Identità del Proprietario'"
        )
    owner = match.group(1).strip()
    if not owner or owner == PROPRIETARIO_SEGNAPOSTO:
        raise ErroreValidazione(
            f"{path}: l'identità del Proprietario è ancora il segnaposto — "
            "sostituirla prima che l'autorizzazione di un qualunque checkpoint "
            "possa essere considerata valida"
        )
    return owner


def _itera_checkpoint(root: Path):
    checkpoints_dir = root / "governance" / "checkpoints"
    if not checkpoints_dir.is_dir():
        raise ErroreValidazione(f"manca {checkpoints_dir}")
    for path in sorted(checkpoints_dir.glob("*.md")):
        if path.name == "TEMPLATE.md":
            continue
        yield path


def _valida_checkpoint(path: Path, identita_proprietario: str, errori: list[str]) -> None:
    text = _leggi(path)
    match = BLOCCO_GOVERNANCE_RE.search(text)
    if not match:
        errori.append(f"{path}: manca un blocco JSON delimitato ```governance")
        return
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        errori.append(f"{path}: il blocco governance non è JSON valido ({exc})")
        return

    for campo in ("id", "title", "owner", "contributor", "state"):
        if not payload.get(campo):
            errori.append(f"{path}: nel blocco governance manca il campo richiesto '{campo}'")

    stato = payload.get("state")
    if stato is not None and stato not in STATI_AMMESSI:
        errori.append(f"{path}: lo stato '{stato}' non è tra {sorted(STATI_AMMESSI)}")

    proprietario_dichiarato = payload.get("owner")
    if proprietario_dichiarato is not None and proprietario_dichiarato != identita_proprietario:
        errori.append(
            f"{path}: il proprietario '{proprietario_dichiarato}' non corrisponde a "
            f"governance/OWNER.md ('{identita_proprietario}') — l'autorizzazione di "
            "questo checkpoint non è valida"
        )

    if stato == "CHIUSO":
        sezione_evidenza = text.split("## Log di evidenza", 1)
        corpo = sezione_evidenza[1] if len(sezione_evidenza) == 2 else ""
        numero_voci = len(EVIDENZA_VOCE_RE.findall(corpo))
        if numero_voci < 2:
            errori.append(
                f"{path}: lo stato è CHIUSO ma il log di evidenza ha solo "
                f"{numero_voci} voc{'e' if numero_voci == 1 else 'i'} — la chiusura "
                "richiede almeno una voce oltre alla proposta iniziale"
            )


def _itera_note(root: Path):
    notes_dir = root / "reasoning" / "notes"
    if not notes_dir.is_dir():
        return
    for path in sorted(notes_dir.glob("*.md")):
        if path.name == "TEMPLATE.md":
            continue
        yield path


def _id_nota(path: Path, errori: list[str]) -> str | None:
    text = _leggi(path)
    match = NOTA_ID_RE.search(text)
    if not match:
        errori.append(f"{path}: non trovo un id 'N-NNN' nel primo titolo")
        return None
    match_stato = STATO_RIGA_RE.search(text)
    if not match_stato:
        errori.append(f"{path}: manca una riga '**Stato:** `...`'")
    elif match_stato.group(1) not in STATI_REASONING_AMMESSI:
        errori.append(
            f"{path}: lo stato '{match_stato.group(1)}' non è tra "
            f"{sorted(STATI_REASONING_AMMESSI)}"
        )
    return match.group(1)


def _id_indice(root: Path, errori: list[str]) -> set[str]:
    index_path = root / "reasoning" / "INDEX.md"
    if not index_path.is_file():
        errori.append(f"manca {index_path}")
        return set()
    text = _leggi(index_path)
    return set(INDICE_RIGA_ID_RE.findall(text))


def valida(root: Path) -> list[str]:
    errori: list[str] = []

    try:
        identita_proprietario = _carica_proprietario(root)
    except ErroreValidazione as exc:
        return [str(exc)]

    for checkpoint_path in _itera_checkpoint(root):
        _valida_checkpoint(checkpoint_path, identita_proprietario, errori)

    id_note: dict[str, Path] = {}
    for note_path in _itera_note(root):
        note_id = _id_nota(note_path, errori)
        if note_id:
            id_note[note_id] = note_path

    id_indice = _id_indice(root, errori)

    for note_id, note_path in id_note.items():
        if note_id not in id_indice:
            errori.append(
                f"{note_path}: la nota '{note_id}' esiste ma non ha una riga in "
                "reasoning/INDEX.md — è invisibile alla regola di lettura"
            )
    for index_id in id_indice:
        if index_id not in id_note:
            errori.append(
                f"reasoning/INDEX.md: la riga '{index_id}' non ha un file "
                "corrispondente sotto reasoning/notes/"
            )

    return errori


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    root = Path(args[0]).resolve() if args else Path.cwd()

    try:
        errori = valida(root)
    except ErroreValidazione as exc:
        print(f"GOVERNANCE_VALIDAZIONE_FAIL_CLOSED: {exc}")
        return 2

    if errori:
        print(f"GOVERNANCE_VALIDAZIONE_FALLITA ({len(errori)} problema/i):")
        for errore in errori:
            print(f"  - {errore}")
        return 1

    print("GOVERNANCE_VALIDAZIONE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
