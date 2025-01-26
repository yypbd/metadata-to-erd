import os
import fire

from dotenv import load_dotenv

from src.database import Database
from src.plantuml_erd import PlantumlErd


load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

database = Database(DATABASE_URL)
erd = PlantumlErd(database)

# schema = 'public'
# use_table_comment = True
# # relation_type = 'none'
# relation_type = 'laravel'
#
# puml = erd.get_erd(schema, use_table_comment, relation_type)
#
# print(puml)

class FireCommand:
    def show_schemas(self):
        return database.get_schemas()

    def generate_erd(self, schema = '', use_table_comment = False, relation_type = 'none', out_filename = None):
        if database.get_schemas().count == 0:
            return 'Schema is empty'

        if schema == '':
            schema = database.get_schemas()[0]

        if schema not in database.get_schemas():
            return 'not exists schemas'

        puml = erd.get_erd(schema, use_table_comment, relation_type)
        if out_filename is None:
            return puml
        else:
            with open(out_filename, "w") as text_file:
                text_file.write(puml)
                text_file.close()

            return "Save puml to " + out_filename


if __name__ == '__main__':
    fire.Fire(FireCommand)

    # puml = FireCommand().generate_erd(schema='public', use_table_comment=False, relation_type='laravel', out_filename='test.puml')
    # print(puml)
