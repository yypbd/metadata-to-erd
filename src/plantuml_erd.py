from src.converter import get_column_type_name
from src.database import Database


class PlantumlErd:
    def __init__(self, database: Database):
        super().__init__()

        self.database = database

    def get_erd(self, schema: str, use_table_comment: bool, relation_type: str) -> str | None:
        if schema not in self.database.schemas:
            return None

        self.database.select_schema(schema)

        puml = f"@startuml {schema}\n\n"

        puml += f"title Entity Relationship Diagram - {schema}\n\n"

        puml += "left to right direction\n\n"

        relations = ""
        for table_name in self.database.table_names:
            table_short_name = self.database.get_table_short_name(table_name)

            if use_table_comment:
                desc = self.database.get_table_comment(table_name)
                if desc is None:
                    desc = table_short_name
            else:
                desc = table_short_name
            primary_keys = self.database.get_primary_keys(table_name)
            foreign_keys = self.database.get_foreign_keys(table_name)

            puml += f"entity \"{desc}\" as {table_short_name} {{\n"

            for column in self.database.get_columns(table_name):
                line = "  "
                if not column.nullable:
                    line += "*"

                line += column.name + " : " + get_column_type_name(column.type)

                # if column.autoincrement:
                #     line += " <<generated>>"
                if primary_keys is not None:
                    if column.name in primary_keys:
                        line += " <<PK>>"

                if relation_type == 'laravel':
                    related = self.database.get_related_table_laravel(column.name)

                    if related is not None:
                        line += " <<FK>>"
                        if column.nullable:
                            relations += f"{table_short_name} }}|--o| {related} : {column.name}\n"
                        else:
                            relations += f"{table_short_name} }}|--|| {related} : {column.name}\n"
                else:
                    if foreign_keys is not None and column.name in foreign_keys:
                        line += " <<FK>>"

                puml += line + "\n"

            puml += "}\n\n"

        puml += relations + "\n"
        puml += "@enduml\n"

        return puml
