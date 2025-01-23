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

for schema in schemas:
    print("schema: %s" % schema)
    for table_name in inspect.get_table_names(schema=schema):
        print("  table: %s" % table_name)
        for column in inspect.get_columns(table_name, schema=schema):
            print("    Column: %s" % column)
            print("      name: %s" % column['name'])
            print("      type: %s" % column['type'])
            print("      nullable: %s" % column['nullable'])
            print("      default: %s" % column['default'])
            print("      autoincrement: %s" % column['autoincrement'])
            print("      comment: %s" % column['comment'])

