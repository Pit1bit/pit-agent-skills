# Governance

Una skill per agenti AI (bootstrap in stile SKILL.md) che imposta una struttura di governance leggera e basata su file per un progetto nuovo costruito con assistenza AI.

## Cosa fa

Installa due cartelle in un progetto:

- **`governance/`** — un file (un "checkpoint") per ogni unità di lavoro, uno stato esplicito per ciascuno, e un'unica identità dichiarata (il Proprietario) contro cui viene verificato tutto il resto. Nessuna autorità è valida se non è scritta in un file che può essere riletto e verificato — mai solo asserita in conversazione.
- **`reasoning/`** — memoria durevole per decisioni e domande aperte, con un indice e una regola di lettura, così un filo di ragionamento sopravvive alla fine di una sessione, al cambio di dispositivo, o a un agente diverso che riprende il progetto.

Entrambe arrivano con un piccolo validatore deterministico (`scripts/validate_governance.py`) che verifica solo la struttura: i campi richiesti sono presenti, gli stati sono validi, una rivendicazione di autorità del Proprietario corrisponde all'unica identità dichiarata, e ogni nota di reasoning è davvero rintracciabile dall'indice.

## Cosa non fa

- Non giudica se una decisione fosse corretta, se un ragionamento fosse solido, o se un ambito fosse ragionevole. Sono valutazioni umane (o comunque esterne); il validatore verifica solo che i file siano coerenti tra loro.
- Non è uno standard fisso a cui ogni progetto deve conformarsi. È un punto di partenza — adattare il vocabolario, gli stati, la forma dei file al progetto, purché i principi sottostanti (l'autorità è verificabile, il lavoro è delimitato, il ragionamento è durevole, i registri sono append-only) restino intatti.
- Non si scala da sola. Nessuno scheduler, coda di ticket o macchina a stati viene installato di default — quelli si aggiungono dopo, solo se un progetto reale dimostra di averne bisogno.

## Perché esiste

Due fallimenti si ripetono nei progetti costruiti con agenti AI attraverso più sessioni:

1. Un agente agisce con un'autorità che non ha davvero — rilancia o asserisce un'approvazione che esiste solo in un messaggio di chat, che nessun altro agente o sessione può verificare.
2. Le decisioni e il loro ragionamento si perdono tra una sessione e l'altra, costringendo a rispiegare lo stesso terreno (e a volte a deciderlo diversamente) ogni volta.

Entrambi nascono dall'usare la conversazione come sistema di registrazione. Questa skill rende i file del progetto stesso il sistema di registrazione.

## Come usarla

Vedere `SKILL.md` per la procedura completa. In breve: copiare `templates/governance/` e `templates/reasoning/` nel progetto di destinazione, compilare `governance/OWNER.md` con un'identità reale, eseguire il validatore, poi fermarsi — lasciare che il progetto venga usato davvero prima di aggiungere qualunque cosa oltre a questo minimo.

## Struttura

```
SKILL.md                          — la definizione della skill (leggere prima questo)
templates/
  governance/
    README.md                     — spiegazione della cartella governance/, copiata così com'è
    OWNER.md                      — dichiarazione dell'identità del Proprietario, da compilare prima dell'uso
    CHECKPOINT_TEMPLATE.md        — un file di checkpoint per ogni unità di lavoro
  reasoning/
    README.md                     — spiegazione della cartella reasoning/, copiata così com'è
    INDEX_TEMPLATE.md             — indice del reasoning, diventa reasoning/INDEX.md
    NOTE_TEMPLATE.md              — una nota di reasoning per ogni filo di pensiero
scripts/
  validate_governance.py          — il validatore strutturale, solo libreria standard
tests/
  test_validate_governance.py     — casi positivi e negativi, incluso il fallimento esatto
                                     "la nota esiste ma non è indicizzata" che questa skill
                                     è nata per prevenire
```

## Stato

Prima versione delimitata. Deliberatamente minimale. Il passo successivo consigliato è eseguirla su un progetto vero e vuoto e lasciare che sia l'attrito reale — non la speculazione — a giustificare qualcosa di più elaborato.
