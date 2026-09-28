---
name: governance
description: Imposta una struttura di governance leggera e basata su file per un progetto nuovo costruito con uno o più agenti AI. Crea una cartella governance/ (chi può autorizzare cosa, un file di checkpoint per unità di lavoro, default fail-closed, log delle decisioni append-only) e una cartella reasoning/ (memoria durevole di decisioni e domande aperte che sopravvive alle interruzioni tra sessioni). Da usare quando si inizia un progetto nuovo con assistenza AI, quando un agente sta per prendere una decisione consequenziale senza una tracciabilità chiara dell'autorizzazione, quando il lavoro viene continuamente rispiegato perché non è stato scritto nulla di durevole, o quando l'utente chiede esplicitamente di "impostare la governance" o "impostare le regole del progetto".
---

# Governance

## Panoramica

Due modalità di fallimento si ripresentano puntualmente non appena più di un agente AI (o un solo agente attraverso molte sessioni scollegate) lavora sullo stesso progetto:

1. **Un agente agisce con un'autorità che non ha.** Dice "il proprietario ha approvato questo" o rilancia un'istruzione come se portasse un'autorizzazione, e non esiste da nessuna parte un file che lo affermi davvero. L'unico riscontro è un messaggio in chat, e i messaggi in chat non sono verificabili da un altro agente, un'altra sessione o un altro giorno.
2. **Le decisioni si perdono tra una sessione e l'altra.** Qualcuno spiega una decisione, un vincolo, un motivo per cui qualcosa è stato scartato — e alla sessione successiva (un giorno diverso, un dispositivo diverso, un agente diverso) quel ragionamento è sparito. Lo stesso terreno viene ripercorso da capo, a volte con una risposta diversa e contraddittoria la seconda volta.

Entrambi i fallimenti hanno la stessa causa: **la conversazione viene usata come sistema di registrazione, e le conversazioni non sono persistenti, non sono verificabili e non sono condivise tra agenti.**

Questa skill risolve il problema rendendo i file del progetto stesso il sistema di registrazione. Crea due cartelle — `governance/` per l'autorizzazione e la tracciabilità delle decisioni, `reasoning/` per la memoria durevole pre-decisionale — con regole abbastanza semplici da poter essere verificate meccanicamente, e abbastanza leggere da non intralciare un progetto ancora agli inizi.

## Quando usarla

Applicare questa skill quando:

- Un progetto nuovo sta iniziando e verrà costruito con l'aiuto di uno o più agenti AI.
- Il lavoro si estende su più sessioni che non condivideranno la memoria della conversazione (giorno diverso, dispositivo diverso, un reset di contesto, un agente completamente diverso).
- Più di un agente o collaboratore tocca lo stesso progetto e uno qualsiasi di loro potrebbe agire su un'istruzione che non può verificare.
- L'utente chiede esplicitamente di "impostare la governance", "impostare le regole del progetto" o simili.
- Ci si accorge di stare per compiere un'azione consequenziale e difficile da annullare basandosi solo su qualcosa detto in chat, senza alcun file a sostegno.

**Quando NON usarla:**

- Uno sviluppatore solo, una sessione sola, una sola seduta di lavoro — non c'è ancora nulla da perdere.
- Un progetto che ha già una struttura equivalente (non crearne una seconda; estendere quella esistente).
- Come modo per aggiungere processo fine a sé stesso. Se non si è mai perso o attribuito male nulla, si sta risolvendo un problema che il progetto non ha ancora.

## Principi fondamentali

Questi sono i principi che l'impostazione iniziale incarna. Sono la parte trasferibile — i nomi delle cartelle e i formati dei file qui sotto sono un'implementazione ragionevole di questi principi, non l'unica possibile.

1. **Autorità ed esecuzione sono ruoli diversi.** Un'unica identità (il Proprietario) può autorizzare, cambiare l'ambito o chiudere qualcosa come fatto. Chiunque e qualunque altra cosa — compreso ogni agente AI — può proporre, eseguire e riferire, ma non può attribuirsi un'autorità che non gli è stata data. Un agente che rilancia "il Proprietario ha detto X" non equivale al Proprietario che ha scritto X da qualche parte verificabile.
2. **Nessuna autorità è valida se non è scritta e verificabile.** Non "il Proprietario probabilmente intendeva", non "in base alla nostra conversazione", non il resoconto di un agente su ciò che un altro agente o una persona avrebbe presumibilmente detto. Se non è in un file che chiunque (o qualunque cosa) può aprire e rileggere, non è autorizzato.
3. **Ogni unità di lavoro ha un solo file con uno stato esplicito.** Non tracciata nella testa di qualcuno, non solo in un thread di chat — un unico file che dice cos'è, chi l'ha autorizzata e in quale stato si trova adesso.
4. **L'ambiguità ferma il lavoro; non viene risolta per assunzione.** Se lo stato, l'ambito o l'autorità dietro un'azione non possono essere determinati dai file del progetto, il lavoro si ferma e l'ambiguità viene segnalata — non viene mai colmata in silenzio con un'ipotesi.
5. **Il registro delle decisioni è append-only.** Una volta che qualcosa è registrato come deciso o fatto, il lavoro successivo aggiunge al registro — non lo riscrive né lo cancella. Se una decisione cambia, il cambiamento e il suo motivo vengono aggiunti, non sostituiti al posto di quello vecchio.
6. **Il ragionamento è memoria, separata dal lavoro.** Il "perché" dietro una direzione — compreso il ragionamento poi scartato o superato — vive in un posto suo, fuori dai file di tracciamento del lavoro, così sopravvive indipendentemente da qualunque singolo task e può essere letto a freddo da qualcuno (o qualcosa) che non c'era quando è successo.
7. **Cambiare le regole è più raro che seguirle.** Una modifica alla struttura di governance stessa (le regole, non un pezzo di lavoro fatto sotto di esse) viene trattata come più esclusiva/delicata del lavoro ordinario — non dovrebbe accadere per caso o come effetto collaterale di un lavoro non correlato.
8. **I controlli meccanici restano meccanici.** Uno script può verificare che un file esista, che un campo richiesto sia presente, che due file siano coerenti tra loro, che nulla di referenziato sia sparito. Uno script non può verificare che una decisione fosse saggia, che un ragionamento fosse corretto, o che il giudizio di una persona fosse quello giusto. Non far credere il contrario agli strumenti.
9. **I punti di ingresso non devono diventare obsoleti.** Se una modifica rende inesatto un README, un indice o un altro file "da leggere per primo", quel file viene corretto nella stessa modifica — non "dopo", non "se c'è tempo". Una porta d'ingresso non aggiornata è peggio di nessuna porta d'ingresso.
10. **Nulla qui dovrebbe dipendere da uno storico di chat per avere senso.** Chiunque — un nuovo collaboratore, un nuovo agente, la stessa persona un anno dopo — dovrebbe poter leggere i file del progetto e capire cos'è attuale, cos'è consolidato e cosa resta aperto, senza accesso a nessuna conversazione che li ha prodotti.

## Cosa NON è questa impostazione iniziale

- **Non è un'autorità universale.** È un framework di partenza per un progetto, non uno standard a cui ogni progetto deve conformarsi. Il progetto che la adotta dovrebbe adattare ruoli, stati e vocabolario al proprio caso — purché l'adattamento non rompa il registro append-only né renda l'autorità non verificabile.
- **Non è un giudice di qualità.** I controlli meccanici installati da questa skill verificano la struttura (un campo è presente, due file sono coerenti, nulla manca) — mai la correttezza di una decisione, il rigore di un ragionamento o la solidità di un giudizio umano.
- **Non sostituisce l'architettura, lo stack o le scelte di processo del progetto.** Imposta solo la tracciabilità dell'autorizzazione e la memoria durevole del ragionamento. Non ha opinioni su come il progetto viene costruito.
- **Non è qualcosa da costruire per intero fin dal primo giorno.** Partire dal minimo qui sotto. Aggiungere meccanismi solo quando un problema reale e osservato lo giustifica — mai in via preventiva.

## Procedura

### Passo 1 — Confermare che serva davvero

Non impostare la governance in un progetto che non ne ha ancora bisogno (vedi "Quando NON usarla"). In caso di dubbio se il progetto abbia già qualcosa di equivalente, controllare prima — cercare una cartella decisions/, checkpoints/ o con scopo simile già esistente prima di crearne una nuova.

### Passo 2 — Creare la struttura minima

Copiare i template dalla cartella `templates/` di questa skill nel progetto di destinazione:

```
governance/
├── README.md              — da templates/governance/README.md
├── OWNER.md                — da templates/governance/OWNER.md
└── checkpoints/
    └── TEMPLATE.md          — da templates/governance/CHECKPOINT_TEMPLATE.md

reasoning/
├── README.md               — da templates/reasoning/README.md
├── INDEX.md                 — da templates/reasoning/INDEX_TEMPLATE.md
└── notes/
    └── TEMPLATE.md           — da templates/reasoning/NOTE_TEMPLATE.md
```

Compilare `governance/OWNER.md` con l'identità reale del Proprietario per questo progetto (un nome, un handle, un account — qualunque cosa identifichi univocamente l'unica entità con potere di autorizzazione qui). Il campo Proprietario di ogni checkpoint verrà verificato contro questo file, quindi va compilato prima di qualunque altra cosa, e non deve mai essere un agente AI.

Non creare nulla oltre a questo — nessuno scheduler, nessuna coda di ticket, nessuna macchina a stati, nessun secondo indice — a meno che il progetto non dimostri di averne bisogno. Questo è il punto di partenza minimo che entrambi i team hanno confermato come smallest-sufficient; trattare qualunque cosa in più come un'aggiunta successiva, guidata dall'evidenza.

### Passo 3 — Collegare il validatore

Copiare `scripts/validate_governance.py` nel progetto di destinazione (es. `scripts/validate_governance.py` o dove vivono gli script del progetto) ed eseguirlo:

```
python scripts/validate_governance.py
```

Verifica, in modo deterministico, soltanto che:

- ogni checkpoint dichiari uno stato tra quelli ammessi;
- il campo Proprietario di ogni checkpoint corrisponda esattamente a `governance/OWNER.md`;
- un checkpoint segnato come chiuso abbia almeno una voce nel proprio log di evidenza (il registro append-only non è vuoto);
- ogni file sotto `reasoning/notes/` sia elencato in `reasoning/INDEX.md`, e ogni riga dell'indice abbia il file corrispondente — bidirezionale (è il controllo singolo che cattura più affidabilmente il caso "l'abbiamo scritto e poi ci siamo dimenticati di renderlo rintracciabile").

**Non** verifica se una decisione fosse corretta, se l'ambito di un checkpoint fosse ragionevole, o se un ragionamento abbia retto. Vedi il Principio fondamentale 8.

Se il progetto di destinazione ha una CI, collegare questo script come controllo obbligatorio su ogni modifica. Se non ce l'ha ancora, resta comunque utile eseguirlo a mano.

### Passo 4 — Spiegare cosa è stato creato

Dire chiaramente all'utente: sono state create due cartelle (governance/, reasoning/), a cosa serve ciascuna, che `governance/OWNER.md` va compilato con un valore reale prima che tutto questo abbia senso, e che il validatore è disponibile ma non ancora collegato alla CI a meno che non venga chiesto anche quello.

### Passo 5 — Fermarsi e lasciarla mettere alla prova

Non costruire in anticipo struttura aggiuntiva "nel caso servisse". Il passo successivo consigliato è usare il progetto normalmente per un po' e vedere quale attrito emerge davvero — solo l'attrito reale e osservato giustifica l'aggiunta di altro.

## Verifica

Dopo l'impostazione iniziale:

- [ ] `governance/OWNER.md` contiene un'identità reale e specifica — non un segnaposto, non un agente AI.
- [ ] `governance/checkpoints/` esiste con almeno il template; nessun lavoro è iniziato senza un checkpoint corrispondente.
- [ ] `reasoning/INDEX.md` esiste con la regola di lettura intatta (leggere prima l'indice e il puntatore alla frontiera corrente, non ogni nota in sequenza).
- [ ] Il validatore viene eseguito e passa sulla struttura appena creata.
- [ ] L'utente capisce che questo è un punto di partenza adattabile, non uno standard fisso, e che nulla oltre questo minimo è stato creato senza un bisogno dimostrato.
