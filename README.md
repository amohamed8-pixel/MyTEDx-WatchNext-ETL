# MyTEDx — Homework 3: Serverless API (AWS Lambda & API Gateway)

**Studente:** Ahmed Sabry Azab Mohamed  
**Matricola:** 1100748  
**Docente:** Prof. Mauro Pelucchi  
**Corso:** Piattaforme Cloud e Mobile (21069)  

---

## Descrizione del Progetto
In questa fase del progetto, è stata sviluppata un'architettura serverless per fornire le raccomandazioni **"Watch Next"** all'applicazione mobile MyTEDx in modo dinamico e ad alta prestazione (latenza < 100ms).

---

## Tecnologie Utilizzate
* **AWS Lambda:** Sviluppo della funzione `Get_Watch_Next_by_Idx` in Python 3.x per interrogare i dati elaborati.
* **Amazon API Gateway:** Creazione di un endpoint RESTful per esporre la funzione Lambda.
* **Amazon DynamoDB:** Database NoSQL utilizzato per la lettura veloce delle raccomandazioni con accesso **O(1)**.

---

## Funzionalità
L'API riceve l'ID del video (`idx`) tramite query string e restituisce un payload JSON contenente:
1. L'ID del video originale (`video_id`).
2. Una lista di video suggeriti (`watch_next`).
3. Il motivo della raccomandazione (`reason`), es: *"Suggerito in base ai percorsi di studio degli altri utenti"*.

---

## Endpoint Live & Test (HTTP 200 OK)

**URL REST API:**
```http
GET [https://2hix9nunuk.execute-api.us-east-1.amazonaws.com/default/Get_Watch_Next_by_Idx?idx=talk_001](https://2hix9nunuk.execute-api.us-east-1.amazonaws.com/default/Get_Watch_Next_by_Idx?idx=talk_001)


Esempio di Payload JSON restituito:
{
  "video_id": "talk_001",
  "watch_next": [
    "talk_002",
    "talk_003"
  ],
  "reason": "Suggerito in base ai percorsi di studio degli altri utenti"
}
