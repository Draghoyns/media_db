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
    - [Sample Queries](#sample-queries)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

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
# PostgreSQL example
createdb entertainment
psql -d entertainment -f sql/schema.sql
psql -d entertainment -f sql/seeds.sql
```
If using Docker, provide docker-compose or Dockerfile steps here.

## Usage
Run example queries from sql/examples or via psql:
```bash
psql -d entertainment -f sql/examples/top_rated_movies.sql
```

### Sample Queries
Top 10 highest-rated movies:
```sql
SELECT m.id, m.title, AVG(r.score) AS avg_score
FROM movies m
JOIN ratings r ON r.item_id = m.id
GROUP BY m.id
ORDER BY avg_score DESC
LIMIT 10;
```

## Testing
Describe how to run tests, if any (SQL unit tests or integration):
```bash
# run SQL test suite (example)
./scripts/run_tests.sh
```

## Contributing
- Fork the repo
- Create a branch: feature/your-feature
- Add migrations and seeds for schema changes
- Open a PR with description and related SQL examples

## License
Specify license (e.g., MIT). See LICENSE file.

## Contact
Project maintainer: Your Name — email@example.com

Placeholders:
- Replace example SQL and file paths with real files in sql/
- Add CI badges and workflow docs as needed
- Keep schema and seeds in sql/schema.sql and sql/seeds.sql
