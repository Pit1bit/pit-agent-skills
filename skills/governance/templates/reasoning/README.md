# Reasoning

Questa cartella è la memoria durevole del *perché* — il ragionamento, le decisioni e le domande aperte che precedono la trasformazione di qualcosa in lavoro autorizzato. Esiste perché un filo di ragionamento non muoia quando una sessione finisce, un dispositivo cambia, o un agente diverso riprende il progetto.

Non è la stessa cosa di `governance/`. La governance traccia il lavoro autorizzato e il suo stato. Questa cartella traccia la comprensione — compresa la comprensione poi scartata o superata, che vale comunque la pena conservare così lo stesso vicolo cieco non viene riesplorato da zero.

## Regola di lettura

Prima di continuare o riaprire un qualunque filo di ragionamento:

1. Leggere prima `INDEX.md` — non ogni nota in questa cartella, solo l'indice.
2. Trovare la sezione "Frontiera corrente" — indica la nota o le note che rappresentano il punto in cui questo ragionamento si trova adesso.
3. Aprire le singole note sotto `notes/` solo quando l'indice non basta a rispondere alla domanda del momento.
4. Non ripartire da zero su un ragionamento che l'indice segna come `CONSOLIDATO` senza un motivo davvero nuovo per riaprirlo.

Questa regola esiste specificamente perché chi (o cosa) riprende il progetto a freddo non debba leggere l'intera cartella per sapere a che punto sono le cose.

## Stati

Ogni nota in `INDEX.md` ha esattamente uno stato. I nomi sono adattabili al progetto; mantenere le quattro distinzioni:

| Stato | Significato |
|---|---|
| `APERTO` | Una domanda o direzione non ancora risolta. |
| `CONSOLIDATO` | Risolta abbastanza bene da non dover essere rimessa in discussione senza un motivo nuovo e specifico. |
| `SUPERATO` | Sostituita da una nota successiva. Conservata, non cancellata — il ragionamento futuro può ancora vedere cosa è stato provato e perché è cambiato. |
| `FRONTIERA_CORRENTE` | La nota o le note che rappresentano il punto vivo attuale di questo ragionamento — la prima cosa da leggere quando lo si riprende. |

## Regole

1. Ogni nota aggiunta sotto `notes/` deve essere aggiunta a `INDEX.md` nella stessa modifica. Una nota che esiste ma non è indicizzata è di fatto invisibile alla regola di lettura sopra, e questo ha già mandato in crisi progetti reali — è la singola modalità di fallimento più comune che questa cartella è costruita per prevenire.
2. Niente viene cancellato. Una nota superata resta, segnata `SUPERATO`, con un rimando a cosa l'ha sostituita.
3. Questa cartella non autorizza nulla. Una conclusione raggiunta qui diventa lavoro reale solo quando ha un checkpoint in `governance/`.
