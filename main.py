import os

from dotenv import load_dotenv

from src.plantuml_erd import PlantumlErd


load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

erd = PlantumlErd(DATABASE_URL)

schemas = erd.get_schemas()

schema = 'public'
use_table_comment = True
# relation_type = 'none'
relation_type = 'laravel'

puml = erd.get_erd(schema, use_table_comment, relation_type)

print(puml)
