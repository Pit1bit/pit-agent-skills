# CP-0000 — Sostituire con un titolo breve

```governance
{
  "id": "CP-0000",
  "title": "Sostituire con un titolo breve",
  "owner": "SOSTITUIRE_CON_L_IDENTITA_REALE_DEL_PROPRIETARIO",
  "contributor": "SOSTITUIRE_CON_CHI_ESEGUE_IL_LAVORO",
  "state": "PROPOSTO"
}
```

`owner` deve corrispondere esattamente a `governance/OWNER.md`, altrimenti l'autorizzazione di questo checkpoint non è valida.
`state` deve essere uno tra: `PROPOSTO`, `AUTORIZZATO`, `ATTIVO`, `BLOCCATO`, `CHIUSO`.

## Ambito

Cos'è questa unità di lavoro, e cosa esplicitamente non include. Se l'ambito non può essere espresso in poche frasi senza tergiversare, probabilmente non è ancora abbastanza delimitato da poter essere autorizzato.

## Log di evidenza

Append-only. Aggiungere una nuova riga per ogni evento materiale — mai modificare o rimuovere una riga esistente. Se qualcosa cambia, aggiungere una nuova riga che spiega il cambiamento; non riscrivere quella vecchia.

- `AAAA-MM-GG` — `<collaboratore>` — proposta iniziale.

<!--
Quando lo stato diventa CHIUSO, qui deve esserci almeno una riga che registra cosa è stato realmente
fatto — non solo la proposta iniziale. Un log di evidenza vuoto o con una sola riga su un checkpoint
CHIUSO significa che il lavoro è avvenuto senza essere registrato, e il validatore lo tratta come un
fallimento strutturale.
-->
