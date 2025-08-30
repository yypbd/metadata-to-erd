
# MetaData To ERD

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-green.svg)](https://www.sqlalchemy.org/)

## 📝 Description

This is a tool that automatically generates Entity Relationship Diagrams (ERD) in PlantUML, D2, or Mermaid format using SQLAlchemy's MetaData.

## ✨ Features

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

## 🚀 Installation

### 🔧 Sync uv

```bash
uv sync
```

### 🔧 Environment Setup

- copy .env.sample to .env
- write DATABASE_URL in SQLAlchemy url string.

```properties
# postgresql
DATABASE_URL="postgresql+pg8000://<<username>>:<<password>>@<<host>>:<<port>>/<<dbname>>"
```

```properties
# mysql
DATABASE_URL="mysql+pymysql://<<username>>:<<passwored>>@<<host>>:<<port>>/<<dbname>>?charset=utf8mb4"
```

## 📖 Usage

### 📋 List Schemas

```bash
uv run main.py schemas
```

### 🎨 Generate ERD

#### 📊 PlantUML Sample

```bash
uv run main.py erd \
  --schema=<<schema>> \
  --engine=plantuml \
  --use_table_comment=True \
  --relation_type=laravel \
  --out_filename=out.puml
```

#### 📑 D2 Sample

```bash
uv run main.py erd \
  --schema=<<schema>> \
  --engine=d2 \
  --use_table_comment=True \
  --relation_type=laravel \
  --out_filename=out.d2
```

#### 📈 Mermaid Sample

```bash
uv run main.py erd \
  --schema=<<schema>> \
  --engine=mermaid \
  --use_table_comment=True \
  --relation_type=laravel \
  --out_filename=out.mmd
```

## ⚙️ Options

### 🛠️ ERD Options

| Option            | Type     | Values          | Description                                          | Default |
|-------------------|----------|-----------------|------------------------------------------------------|---------|
| `schema`          | String   | Any schema name | Database schema to analyze                          | First available schema |
| `engine`          | String   | `puml`<br>`d2`<br>`mermaid` | Output format to generate | `puml` |
| `use_table_comment` | Boolean | `True`<br>`False` | Use table comments in diagram | `False` |
| `relation_type`   | String   | `none`<br>`laravel` | Relationship detection method:<br>• none: Use database FK<br>• laravel: Use Laravel naming | `none` |
| `out_filename`    | String   | Any valid path  | Output file path (prints to stdout if not specified) | None |

## 🔗 Links

### 📌 PlantUML

- [Information Engineering Diagrams](https://plantuml.com/en/ie-diagram)
- [Entity Relationship Diagrams](https://plantuml.com/en/er-diagram)

### 📌 D2

- [D2](https://d2lang.com/tour/intro/)

### 📌 Mermaid

- [Entity Relationship Diagrams](https://mermaid.js.org/syntax/entityRelationshipDiagram.html)

### 📌 SQLAlchemy

- [SQLAlchemy Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html)

## 📊 Samples

### converted plantuml_sample.puml : laravel

![Alt text](./samples/plantuml_sample.png?raw=true "plantuml sample")

### converted d2_sample.d2 : laravel

![Alt text](./samples/d2_sample.svg?raw=true "d2 sample")

### converted mermaid_sample.mmd : laravel

![Alt text](./samples/mermaid_sample.mmd "mermaid sample")
