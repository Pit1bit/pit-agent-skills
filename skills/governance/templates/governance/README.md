# Governance

Questa cartella è il registro del progetto su chi può autorizzare cosa, e in quale stato si trova ogni unità di lavoro. Non è un posto per idee o discussioni — quelle appartengono a `reasoning/`. Questa è solo per decisioni che portano autorità.

## Perché esiste

Senza un registro scritto, l'autorità viene asserita invece che verificata: un agente o una persona può dire "questo è stato approvato" senza nulla con cui confrontarlo. Questa cartella esiste perché "approvato" significhi sempre "scritto qui, dall'unica identità che può scriverlo" — mai "qualcuno l'ha detto".

## Ruoli

- **Proprietario** — l'unica identità con l'autorità di autorizzare nuovo lavoro, cambiare l'ambito o chiudere qualcosa come fatto. Dichiarato una sola volta, in `governance/OWNER.md`. Mai un agente AI.
- **Collaboratore** — chiunque o qualunque cosa (una persona, un agente AI) svolga il lavoro. Un Collaboratore può proporre, eseguire e riferire, ma non può attribuirsi autorità, e non può autorizzare il proprio stesso lavoro.

Se qualcosa rivendica l'autorità del Proprietario e non è riconducibile a `governance/OWNER.md`, non è valido — fermarsi e chiedere, non procedere su quella base.

## Checkpoint

Ogni unità di lavoro riceve esattamente un file sotto `checkpoints/`, creato a partire da `checkpoints/TEMPLATE.md`. Un checkpoint registra:

- cos'è il lavoro e perché;
- chi l'ha autorizzato (deve corrispondere a `OWNER.md`);
- chi lo sta svolgendo;
- il suo stato attuale (vedi sotto);
- un log append-only di ciò che è successo — mai modificato o cancellato, solo ampliato.

## Stati

Un checkpoint si trova sempre esattamente in uno di questi stati. Adattare i nomi se il progetto usa già parole diverse per la stessa cosa — mantenere la forma:

| Stato | Significato |
|---|---|
| `PROPOSTO` | Descritto, non ancora autorizzato. In questo stato non dovrebbe avvenire alcun lavoro. |
| `AUTORIZZATO` | Il Proprietario l'ha approvato. Il lavoro può iniziare. |
| `ATTIVO` | Il lavoro è in corso. |
| `BLOCCATO` | Il lavoro si è fermato perché qualcosa è ambiguo, mancante, o richiede una decisione del Proprietario. È uno stato normale e atteso — non un fallimento da nascondere. |
| `CHIUSO` | Fatto. Deve avere almeno una voce nel log di evidenza; un checkpoint non può passare da `AUTORIZZATO` direttamente a `CHIUSO` senza nulla registrato nel mezzo. |

## Regole

1. Nessun lavoro inizia senza un checkpoint in stato `AUTORIZZATO` o successivo.
2. Solo il Proprietario sposta un checkpoint da `PROPOSTO` ad `AUTORIZZATO`, o approva `CHIUSO`.
3. Se un Collaboratore non riesce a determinare lo stato, l'ambito o l'autorizzazione di qualcosa dai file di questa cartella, si ferma e segnala l'ambiguità — non tira a indovinare.
4. Le voci si aggiungono, non si riscrivono mai. Se qualcosa cambia, si aggiunge una nuova voce che spiega cosa è cambiato e perché; la voce vecchia resta.
5. Una modifica alle regole di questa cartella (questo README, la forma del template, il validatore) è trattata come più delicata del lavoro ordinario — non dovrebbe avvenire come effetto collaterale di una modifica non correlata.
6. Se una modifica rende inesatto un altro file di ingresso (un README, un indice), quel file viene corretto come parte della stessa modifica — non rimandato.
