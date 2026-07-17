## Homework 3: Serverless API (AWS Lambda & API Gateway)
In questa fase del progetto, è stata sviluppata un'architettura serverless per fornire le raccomandazioni "Watch Next" all'applicazione mobile MyTEDx in modo dinamico.

**Tecnologie utilizzate:**
* **AWS Lambda**: Sviluppo della funzione `Get_Watch_Next_by_Idx` in Python 3.x per interrogare i dati elaborati.
* **Amazon API Gateway**: Creazione di un endpoint RESTful per esporre la Lambda function.
* **Amazon DynamoDB**: Database NoSQL utilizzato per la lettura veloce delle raccomandazioni.

**Funzionalità:**
L'API riceve l'ID del video (`idx`) tramite query string e restituisce un payload JSON contenente:
1. L'ID del video originale.
2. Una lista di video suggeriti ("Watch Next").
3. Il motivo della raccomandazione (modello di analisi), es: *"Suggerito in base ai percorsi di studio degli altri utenti"*.

Il codice sorgente della Lambda function è disponibile nel file `lambda_function.py`.
