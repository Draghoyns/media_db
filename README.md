# SQL Entertainment

 A small SQL-focused project containing schema, sample data, and queries for a non-comprehensive set of media (movie, tv show, manga, anime, books), coupled with user consumption (here it's my personal consumption).

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#) [![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## Table of Contents
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Install](#install)
    - [Database Setup](#database-setup)
- [Usage](#usage)
- [Testing](#testing)
- [License](#license)
- [TODO](#todo)

## Overview
This project is for refreshing knowledge and learning new skills involving all tech used.

The goal is to develop a web app based on a subjective media database to track media suggestions and consumed media by one user (me).

The app should allow the following operations:
- adding an element into the database
- modifying details of an element
- querying of all sorts
- looking at predefined queries (e.g. top 10 suggestions based on media length or completion)

Current status:
- SQL schema set in `schema.sql`
- CSV file to start populating the database
- some utility functions and FastAPI endpoints in main.py
- data insertion : testing (TODO)


## Tech Stack
- SQL dialect: SQLite
- Language : Python
- FastAPI
- TODO: Docker

## Database Schema
Main table repertories all media types in an uniform format:
- media(id, title, type, release_year, origin_lang, status, comment)

Specific media types have their own table :
- info_movie (id, title, year, runtime, description)
- info_tvshow (id, title, seasons, status)
- info_manga(id, volumes, authors, adapted_anime_id)
- info_anime(id seasons, ep_duration_min, total_episodes, status)
- info_book(id, pages, authors, status)

## Getting Started

### Prerequisites
- sqlite3
- fastapi
- [Optional] Docker
- [Optional] language runtime for helpers

### Install
Clone and enter repo:
```bash
git clone <repo-url>
cd SQL_entertainment
```

### Database Setup
Initialize database and load schema:

```bash
# SQLite example
sqlite3 entertainment.db < sql/schema.sql
# populate database with elements in data/raw.csv
python populate_db.py
```
If using Docker, provide docker-compose or Dockerfile steps here.

## Usage
- Run example queries directly on the database:
```bash
sqlite3 entertainment.db < sql/examples/top_rated_movies.sql
```
- Operations via FastAPI docs:
TODO


## Testing
Function tests are located in `test.py`.

## License
This project is licensed under the [MIT License](LICENSE).


## TODO

Placeholders:
- Add CI badges and workflow docs as needed
- Add how to populate database
- Explain usage with FastAPI
- Think about Docker ?
