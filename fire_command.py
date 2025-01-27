import os

from dotenv import load_dotenv

from src.database import Database
from src.plantuml_erd import PlantumlErd

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

class FireCommand:
    def show_schemas(self):
        database = Database(DATABASE_URL)

        return database.get_schemas()

    def generate_erd(self, schema = '', use_table_comment = False, relation_type = 'none', out_filename = None):
        if out_filename is not None and os.path.exists(out_filename):
            return '[error] Exists - ' + out_filename

        database = Database(DATABASE_URL)
        erd = PlantumlErd(database)

        if database.get_schemas().count == 0:
            return '[error] Schema is empty'

        if schema == '':
            schema = database.get_schemas()[0]

        if schema not in database.get_schemas():
            return '[error] Not exists schemas'

        puml = erd.get_erd(schema, use_table_comment, relation_type)
        if out_filename is None:
            return puml
        else:
            with open(out_filename, "w") as text_file:
                text_file.write(puml)
                text_file.close()

            return "[success] Save puml to " + out_filename
