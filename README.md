# MyTEDx — Homework 3: Serverless API & Interactive Quiz Engine

**Student:** Ahmed Sabry Azab Mohamed  
**Matricola:** 1100748  
**Course:** Piattaforme Cloud e Mobile (21069) — A.A. 2024/2025  
**Docent:** Prof. Mauro Pelucchi  

---

## 🚀 Live API Endpoint
- **Base Endpoint:** `https://2hix9nunuk.execute-api.us-east-1.amazonaws.com/default/Get_Watch_Next_by_Idx`
- **Example Request:** `https://2hix9nunuk.execute-api.us-east-1.amazonaws.com/default/Get_Watch_Next_by_Idx?video_id=talk_001`

## 📌 Descrizione del Progetto
In questa fase del progetto MyTEDx, è stata implementata un'architettura **Serverless Backend** basata su **AWS Lambda** e **Amazon API Gateway** per servire i dati denormalizzati da **Amazon DynamoDB** all'applicazione mobile Flutter.

Il backend supporta la restituzione unificata di:
1. **Metadati del Video**: Titolo, speaker e id del talk.
2. **Watch Next Engine**: Raccomandazioni di talk correlati (`recommended_talks`) accompagnate da una motivazione esplicita (`reason`).
3. **Interactive Quiz Engine**: Test di comprensione integrato (*Active Learning*) da eseguire in locale sul client mobile senza ulteriore latenza di rete.

---

## 🏗️ Architettura Serverless [ App Flutter ] ---> (HTTPS GET) ---> [ API Gateway ] ---> (Invoke) ---> [ AWS Lambda (Python 3) ] ---> (GetItem) ---> [ Amazon DynamoDB ]
- **Amazon API Gateway**: REST Endpoint con abilitazione CORS e routing delle richieste.
- **AWS Lambda**: Execution Engine serverless con supporto `boto3` e gestione della serializzazione dei tipi `Decimal`.
- **Amazon DynamoDB**: Database NoSQL denormalizzato con lettura $O(1)$ tramite Partition Key (`video_id`).

---

## 🚀 REST API Endpoints

### 1. Get Watch Next & Quiz by Video ID
- **URL:** `https://<api-id>.execute-api.us-east-1.amazonaws.com/default/Get_Watch_Next_by_Idx`
- **Method:** `GET`
- **URL Params:** `video_id=[string]` (es. `video_id=talk_001`)

#### Example Response (`200 OK`):
```json
{
  "video_id": "talk_001",
  "title": "The Future of Quantum Computing in STEM",
  "speaker": "Dr. Elena Rossi",
  "recommended_talks": ["talk_002", "talk_003"],
  "reason": "Correlazione basata sui temi del talk",
  "quiz": [
    {
      "question": "Qual è il tema principale affrontato in questo talk?",
      "options": [
        "Innovazione e Tecnologia",
        "Sviluppo Personale e Società",
        "Scienza e Ricerca Applicata"
      ],
      "correct_idx": 0
    }
  ]
}
