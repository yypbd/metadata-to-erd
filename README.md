
# MetaData To ERD

## Description

This is a tool that automatically generates Entity Relationship Diagrams (ERD) in PlantUML or D2 using SQLAlchemy's MetaData.

## Features

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
  --out_filename=out.puml
```

## Options

### erd options

| option            | Type     | Value           | Description                                                |
|-------------------|----------|-----------------|------------------------------------------------------------|
| schema            | String   |                 | Database schema name.                                      |
| engine            | String   | puml<br>d2      | PlantUML or D2                                             |
| use_table_comment | Boolean  | True<br>False   | Use table comment as description.                          |
| relation_type     | String   | none<br>laravel | none: Read database FK<br>laravel: laravel migration style |
| out_filename      | String   |                 | erd filename                                               |

## Links

### PlantUML

- [Information Engineering Diagrams](https://plantuml.com/en/ie-diagram)
- [Entity Relationship Diagrams](https://plantuml.com/en/er-diagram)

### D2

= [D2](https://d2lang.com/tour/intro/)

### SQLAlchemy

- [SQLAlchemy Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html)

## Samples

### converted plantuml_sample.puml : laravel

![Alt text](./samples/plantuml_sample.png?raw=true "plantuml sample")

### converted d2_sample.d2 : laravel

![Alt text](./samples/d2_sample.svg?raw=true "d2 sample")
