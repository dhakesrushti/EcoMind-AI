# EcoMind AI

## Overview

EcoMind AI is an AI-powered Environmental Consultant that uses Retrieval Augmented Generation (RAG) to answer environmental questions using scientific papers and datasets.

---

## Architecture

User
↓
Streamlit UI
↓
RAG Pipeline
↓
ChromaDB
↓
Gemini API
↓
Response Generation

Components:

- Streamlit Frontend
- Gemini LLM
- ChromaDB Vector Database
- PDF Ingestion Module
- Retrieval Engine
- Reasoning Engine

---

## Database / Schema

Vector Database: ChromaDB

Collections:

documents
embeddings
metadata

Stored Metadata:

- document_name
- chunk_id
- source
- page_number

---

## Local Setup

### Install Dependencies

pip install -r requirements.txt

### Environment Variables

Create .env

GEMINI_API_KEY=YOUR_KEY

### Run Application

streamlit run app.py

---

## Features

- PDF Upload
- RAG
- Citation Support
- Reasoning Trace
- Environmental Recommendations

---

## Tech Stack

- Python
- Streamlit
- Gemini
- ChromaDB
- Sentence Transformers

---

## CI/CD

Currently using GitHub repository version control.

Future CI/CD:

GitHub Actions

Pipeline:

Push
↓
Build
↓
Test
↓
Deploy
