# GTF_Validator
A Project of Bioinformatics. Analyse and Check the syntax of a GTF file


Cartella contenente i file necessari all'esecuzione di un validatore di file in formato GTF (Gene Transfer Format)
per il progetto del corso di bioinformatica (gennaio 2018).

Questo programma si pone due obiettivi: 
1) la validazione di un file in input, se in formato GTF, tramite il controllo della sua formattazione e della correttezza dei suoi campi;
2) la stampa degli errori o del campo che non rendono il file in input un file GTF, se questo il caso.

All'interno del programma sono definite due funzioni utili:

is_Number(), che (come intuibile) controlla se l'argomento passatole è un numero (float), e dà errore in caso negativo;
print_status(), che si occupa della gestione degli errori su singola stringa, campo per campo, definendo se questa sia sintatticamente corretta o meno;

Per prima cosa, lo script riceve il file in input e lo divide nei suoi campi (9, se non sono presenti errori). Registra il primo come "idsorg" e il 
secondo come "software". In seguito, inizia a valutare le possibili combinazioni che si creano tra il campo feature (per i casi "exon" e "CDS") e il campo score 
in una serie di if/elif/else: in ognuno dei casi valutati, vengono effettuati controlli sul campo 9 con espressioni regolari (re.search) per verificare la correttezza sintattica
sia del valore che del nome dell'attributo a cui questo si riferisce. In sinergia con la funzione print_status(), ogni riga viene controllata e viene stampato a video l'esito 
riguardo la sua correttezza.
In ultima analisi, un prospetto generale verrà stampato in seguito allo scan del file: sapremo quindi il numero di righe non corrette secondo la formattazione GTF e se il file 
può essere verificato come GTF-valid.




