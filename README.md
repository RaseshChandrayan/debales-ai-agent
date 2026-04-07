# debales-ai-agent
An intelligent AI agent that bridges the gap between static knowledge and the live web. Powered by LangGraph, it uses a smart router to navigate between a Debales AI RAG (ChromaDB) for internal specs and SerpAPI for real-time external queries. This hybrid workflow ensures precise, cited answers without hallucinations.

# Objective
This project implements an AI agent designed to:
Answer Debales AI-related queries using Retrieval-Augmented Generation (RAG).
Utilize SERP API for external and general-purpose queries.
Route queries intelligently through a stateful LangGraph workflow.

# Features

## Retrieval-Augmented Generation (RAG)
Scrapes and processes Debales AI website content.
Stores vectorized data in a Chroma DB instance.
Retrieves high-relevance context for specialized internal queries.

## SERP API Integration
Integrates SerpAPI for broad external information gathering.
Fetches real-time search results to provide up-to-date answers.

## LangGraph Workflow Orchestration
Implements a router to direct traffic into three specific paths:
RAG: For dedicated Debales-specific information.
SERP: For general or real-time external knowledge.
Hybrid: For complex queries requiring a synthesis of both sources.
Implements strict fallback protocols to prevent hallucinations.

## How it Works

1. User enters a query
2. Query is classified using LangGraph:
   - Debales-related → RAG
   - General → SERP API
   - Mixed → Both
3. Relevant data is retrieved
4. Final answer is formatted with sources



Project Structure

scraper.py → Scrapes website
ingest.py → Creates vector DB
rag_tool.py → RAG retrieval
serp_tool.py → SERP API tool
agent.py → LangGraph workflow
main.py → CLI interface

## Run Order (IMPORTANT)

1. python ingest.py
2. python main.py