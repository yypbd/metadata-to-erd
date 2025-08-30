
# MetaData To ERD

## Description

This is a tool that automatically generates Entity Relationship Diagrams (ERD) in PlantUML, D2, or Mermaid format using SQLAlchemy's MetaData.

## Features

- Generate ERD diagrams from database metadata using SQLAlchemy
- Support multiple output formats
  - PlantUML
  - D2
  - Mermaid
- Support multiple databases
  - PostgreSQL
  - MySQL
- Relationship detection
  - Standard foreign key relationships
  - Laravel-style naming conventions
- Customization options
  - Table comments
  - Layout direction

## Installation

### compose env

- copy .env.sample to .env
- write DATABASE_URL in SQLAlchemy url string.

```dotenv
# postgresql
DATABASE_URL="postgresql+pg8000://<<username>>:<<password>>@<<host>>:<<port>>/<<dbname>>"
```

```dotenv
# mysql
DATABASE_URL="mysql+pymysql://<<username>>:<<passwored>>@<<host>>:<<port>>/<<dbname>>?charset=utf8mb4"
```

## Usages

### schemas

```bash
uv run main.py schemas
```

### erd

#### PlantUML sample

```bash
uv run main.py erd \
  --schema=<<schema>> \
  --engine=plantuml \
  --use_table_comment=True \
  --relation_type=laravel \
  --out_filename=out.puml
```

#### D2 sample

```bash
uv run main.py erd \
  --schema=<<schema>> \
  --engine=d2 \
  --use_table_comment=True \
  --relation_type=laravel \
  --out_filename=out.d2
```

#### Mermaid sample

```bash
uv run main.py erd \
  --schema=<<schema>> \
  --engine=mermaid \
  --use_table_comment=True \
  --relation_type=laravel \
  --out_filename=out.mmd
```

## Options

### erd options

| option            | Type     | Value           | Description                                                |
|-------------------|----------|-----------------|------------------------------------------------------------|
| schema            | String   |                 | Database schema name.                                      |
| engine            | String   | puml<br>d2<br>mermaid | PlantUML, D2, or Mermaid                                             |
| use_table_comment | Boolean  | True<br>False   | Use table comment as description.                          |
| relation_type     | String   | none<br>laravel | none: Read database FK<br>laravel: laravel migration style |
| out_filename      | String   |                 | erd filename                                               |

## Links

### PlantUML

- [Information Engineering Diagrams](https://plantuml.com/en/ie-diagram)
- [Entity Relationship Diagrams](https://plantuml.com/en/er-diagram)

### D2

- [D2](https://d2lang.com/tour/intro/)

### Mermaid

- [Entity Relationship Diagrams](https://mermaid.js.org/syntax/entityRelationshipDiagram.html)

### SQLAlchemy

- [SQLAlchemy Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html)

## Samples

### converted plantuml_sample.puml : laravel

![Alt text](./samples/plantuml_sample.png?raw=true "plantuml sample")

### converted d2_sample.d2 : laravel

![Alt text](./samples/d2_sample.svg?raw=true "d2 sample")

### converted mermaid_sample.mmd : laravel

![Alt text](./samples/mermaid_sample.mmd "mermaid sample")
