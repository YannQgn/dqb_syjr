DATA QUERY BUILDER — MCP SERVER
================================

Project Overview
----------------
This project implements a Model Context Protocol (MCP) server that allows an AI assistant
(Gemini CLI) to query structured data using natural language.

Instead of manually writing SQL queries, users can ask questions in English. The LLM
translates the request into SQL and executes it via MCP tools.

Main features:
- Load CSV files into a SQLite database
- Inspect database schema
- Run SQL queries
- Secure read-only query execution
- Query history tracking

The database used during execution is an in-memory SQLite database.


Architecture
------------
User (Natural language)
        |
        v
Gemini CLI (LLM reasoning)
        |
        v
MCP Server (server.py)
        |
        +---- Tools
        |       load_csv
        |       list_tables
        |       describe_schema
        |       run_query
        |
        +---- Resources
                db://schema
                db://query-history
        |
        v
SQLite (in-memory database)


Project Structure
-----------------
electiveclaude/
│
├─ server.py
├─ sqlite_helper.py
├─ requirements.txt
├─ README.txt
│
├─ data/
│   └─ pokemon.csv
│
└─ venv/


Dataset
-------
This project uses the Pokémon TCG dataset available on Kaggle:

https://www.kaggle.com/datasets/adampq/pokemon-tcg-all-cards-1999-2023

Download the dataset and place the CSV file inside the project:

data/pokemon.csv

Dataset size:
~17,000 Pokémon trading cards from 1999 to 2023.

The dataset includes attributes such as:
- card name
- HP
- type
- rarity
- generation
- attacks
- abilities
- flavor text


Installation
============

1) Install Python
-----------------
Python 3.10+ recommended.

Check installation:

`python --version`


2) Create Virtual Environment
-----------------------------

Windows:

`python -m venv venv`

Activate the environment:

`venv\Scripts\activate`


3) Install Dependencies
-----------------------

`pip install -r rq.txt`

Gemini CLI Installation
=======================

Gemini CLI is required to interact with the MCP server.

Official documentation:

https://goo.gle/gemini-cli

Install globally:

`npm install -g @google/gemini-cli`

Verify installation:

`gemini --version`


Adding the MCP Server to Gemini
================================

Register the MCP server:

`gemini mcp add electiveclaude python server.py`

Verify that the server is registered:

`gemini mcp list`

Expected output:

electiveclaude: python server.py (stdio)


Running Gemini
==============

Start Gemini:

`gemini -y`
The -y flag automatically accepts tool execution.


Running the MCP Inspector
=========================

The MCP Inspector allows debugging the server without an LLM.

Start the inspector:

`mcp dev server.py`

Open the web interface by clicking the link provided by the result.

The inspector displays:

Tools:
- load_csv
- list_tables
- describe_schema
- run_query

Resources:
- db://schema
- db://query-history


Available Tools
===============

load_csv(file_path: str, table_name: str)

Loads a CSV file into a SQLite table with automatic type detection.


list_tables()

Returns all tables currently stored in the database.


describe_schema()

Returns the database schema (tables, columns, and types).


run_query(query: str)

Executes a SQL query on the database.

Security restriction:
Only SELECT queries are allowed.


Available Resources
===================

db://schema

Returns the current database schema as JSON.


db://query-history

Returns all SQL queries executed during the session.


Security Model
==============

The system prevents destructive queries.

Blocked SQL commands:

DROP
DELETE
ALTER
INSERT
UPDATE
CREATE
REPLACE
TRUNCATE
ATTACH
DETACH
PRAGMA

Only single SELECT queries are allowed.

Example rejected query:

`DROP TABLE pokemon`


Usage Example
=============

Start Gemini:

`gemini -y`


Load dataset:

Load the CSV file data/pokemon.csv into a table called pokemon


Check available tables:

`What tables exist in the database?`


Inspect schema:

`Describe the schema of the pokemon table`


Example queries:

`How many cards are in the dataset?`
`What are the 10 Pokémon cards with the highest HP?`
`How many cards exist per generation?`
`What is the average HP per rarity?`


Example Generated SQL
=====================

Natural language:

"What are the strongest Pokémon cards?"

Generated SQL:

SELECT name, hp
FROM pokemon
ORDER BY hp DESC
LIMIT 10


Testing Security
================

Test a forbidden query:

`DROP TABLE pokemon`

Expected response:

Query rejected. Only single SELECT statements are allowed.


Test multi-statement injection:

`SELECT * FROM pokemon; DROP TABLE pokemon`

Expected response:

Query rejected.


Comparison: With vs Without Tools
=================================

Without Tools
-------------
The LLM attempts to answer questions from general knowledge.
Results are unreliable and often hallucinated.


With Tools
----------
The LLM queries the database using SQL.
Answers are based on real data and are accurate.


Evaluation Criteria Coverage
=============================

Tool Design
✓ load_csv
✓ list_tables
✓ describe_schema
✓ run_query

Implementation
✓ SQLite integration
✓ CSV ingestion
✓ automatic type detection

Integration
✓ Gemini CLI
✓ MCP Inspector

Documentation
✓ setup instructions
✓ usage examples
✓ tool descriptions

Comparison Analysis
✓ with tools vs without tools