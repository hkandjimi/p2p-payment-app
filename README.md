
# P2P Payment Integration Demo (Angular + FastAPI + WireMock)

This repository provides a simple local development environment that demonstrates a **Person‑to‑Person (P2P) payment integration** using:

- Angular – Web UI
- FastAPI – Backend API gateway
- WireMock – Mock external payment API

The application allows a user to submit a P2P payment request and view the transaction outcome.

---

# Architecture

Browser (Angular UI)
        |
        v
FastAPI Backend
        |
        v
WireMock Mock Payment API

Flow:

Angular → FastAPI → WireMock → FastAPI → Angular

FastAPI performs validation and forwards the request to WireMock which simulates the payment provider.

---

# Project Structure

p2p-payment-starter/
│
├── frontend/                 Angular UI placeholder
│
├── backend/                  FastAPI service
│   └── app/
│       ├── main.py
│       ├── api/payment.py
│       └── models/schemas.py
│
├── wiremock/
│   ├── mappings/
│   └── __files/
│
├── docker-compose.yml
└── README.md

---

# Setup Instructions (Mac)

Prerequisites

- Python 3.10+
- Node.js (for Angular)
- Docker
- Git

Clone repo

git clone <repo-url>
cd p2p-payment-starter

Start services

docker compose up --build

Services:

Angular UI
http://localhost:4200

FastAPI API
http://localhost:8000/docs

WireMock Admin
http://localhost:8080/__admin

---

# Testing the Integration

Example request

POST http://localhost:8000/api/payment

{
  "clientReference": "REF-20260306-001",
  "senderAccountNumber": "1234567890",
  "receiverAccountNumber": "0987654321",
  "amount": 150.00,
  "currency": "NAD",
  "reference": "Lunch payment"
}

FastAPI validates the payload then forwards the request to the mock WireMock endpoint:

POST /api/p2p-payment

WireMock returns a simulated success or error response.

---

# Assumptions

1. No authentication is required.
2. No database persistence is implemented.
3. Transaction IDs are simulated by the mock API.
4. Currency must be NAD.
5. Only basic validation is performed in FastAPI.

---

# Implementation Details

Angular

Provides a form for users to capture:

- clientReference
- senderAccountNumber
- receiverAccountNumber
- amount
- currency
- reference

FastAPI

Acts as the API gateway and performs:

- schema validation using Pydantic
- business rule checks
- forwarding requests to WireMock

WireMock

Simulates the external payment service using predefined stub responses.

---

# Future Improvements

- Add Angular form validation
- Add error simulation in WireMock
- Add transaction history persistence
- Add automated integration tests
