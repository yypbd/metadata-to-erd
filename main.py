import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

load_dotenv()

ENGINE_URL = os.environ.get("ENGINE_URL")

engine = create_engine(
    ENGINE_URL,
    isolation_level="REPEATABLE READ",
)

inspect = inspect(engine)

schemas = inspect.get_schema_names()


def get_type_name(column_type):
    name = column_type.data_type.python_type.__name__

    if name == "str":
        return "text"
    elif name == "int":
        return "number"

    return name


puml = "@startuml\r\n\r\n"

for schema in schemas:
    for table_name in inspect.get_table_names(schema=schema):
        puml += f"entity \"{table_name}\" as \"{table_name}\" " + "{\r\n"

        for column in inspect.get_columns(table_name, schema=schema):
            line = "  "
            if not column['nullable']:
                line += "*"

            line += column['name'] + " : " + get_type_name(column['type'])

            if column['autoincrement']:
                line += " <<generated>>"

            puml += line + "\r\n"
        puml += "}\r\n\r\n"
    break

puml += "@enduml\r\n"

print(puml)
