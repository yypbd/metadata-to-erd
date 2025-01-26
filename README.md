
# MetaData To ERD

## Description

This is a tool that automatically generates Entity Relationship Diagrams (ERD) in PlantUML using SQLAlchemy's MetaData.

## Features

## Installation

### install packages
```bash
pip install -r requirements.txt
```

### compose env

- copy .cnv.sample to .env
- write DATABASE_URL in SQLAlchemy url string.

```dotenv
DATABASE_URL="postgresql+pg8000://<<username>>:<<password>>@<<host>>:<<port>>/<<dbname>>"
```

## Usages

### show_schemas

```bash
python main.py show_schemas
```

### generate_erd 

```bash
python main.py generate_erd \ 
  --schema=<<schema>> \
  --use_table_comment=True \
  --relation_type=laravel \
  --out_filename=out.puml  
```

## Options

### generate_erd options

| option            | Type    | Value           | Description                                                |
|-------------------|---------|-----------------|------------------------------------------------------------|
| schema            | String  |                 | Database schema name.                                      |
| use_table_comment | String  |                 | Directory where backup files will be stored.               |
| relation_type     | String  | none<br>laravel | none: Read database FK<br>laravel: laravel migration style |
| out_filename      | String  |                 | plantuml filename                                          |

## Links

### PlantUML

- [Information Engineering Diagrams](https://plantuml.com/en/ie-diagram)
- [Entity Relationship Diagrams](https://plantuml.com/en/er-diagram)
