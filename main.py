import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, MetaData

load_dotenv()

ENGINE_URL = os.environ.get("ENGINE_URL")

engine = create_engine(
    ENGINE_URL,
    isolation_level="REPEATABLE READ",
)

db_inspect = inspect(engine)
metadata = MetaData()
metadata.reflect(bind=engine)

schemas = db_inspect.get_schema_names()

table_names = metadata.tables.keys()

def get_type_name(column_type):
    # if hasattr(column_type, "data_type"):
    #     name = column_type.data_type.python_type.__name__
    # elif hasattr(column_type, "python_type"):

    name = column_type.python_type.__name__
    if name == "str":
        return "text"
    elif name == "int":
        return "number"
    elif name == "datetime":
        return "datetime"

    return name

def get_table_comment(name: str) -> str:
    table = metadata.tables[name]
    if table is None:
        return name

    if table.comment is None:
        return name

    return table.comment

def get_primary_keys(name: str):
    table = metadata.tables[name]
    if table is None:
        return None

    return [col.name for col in table.primary_key]

def get_foreign_keys(name: str):
    table = metadata.tables[name]
    if table is None:
        return None

    return [col.name for col in table.foreign_keys]

def is_foreign_key(column_name: str) -> bool:
    if column_name.endswith("_id"):
        related_table_name = column_name[:-3] + "s"
        return related_table_name in table_names

    return False


puml = "@startuml\r\n\r\n"

relations = ""

for schema in schemas:
    if schema != "public":
        continue

    for table_name in db_inspect.get_table_names(schema=schema):
        desc = get_table_comment(table_name)
        primary_keys = get_primary_keys(table_name)
        foreign_keys = get_foreign_keys(table_name)

        puml += f"entity \"{desc}\" as \"{table_name}\" " + "{\r\n"

        for column in db_inspect.get_columns(table_name, schema=schema):
            line = "  "
            if not column['nullable']:
                line += "*"

            line += column['name'] + " : " + get_type_name(column['type'])

            # if column['autoincrement']:
            #     line += " <<generated>>"
            if primary_keys is not None:
                if column['name'] in primary_keys:
                    line += " <<PK>>"

            if is_foreign_key(column['name']):
                line += " <<FK>>"
                relations += table_name + " }|--|| " + column['name'][:-3] + "s : " +column['name'] + "\r\n"

            puml += line + "\r\n"

        puml += "}\r\n\r\n"
    break

puml += relations + "\r\n"

puml += "@enduml\r\n"

print(puml)
