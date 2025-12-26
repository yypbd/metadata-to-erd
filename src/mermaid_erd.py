from src.converter import get_column_type_name
from src.database import Database


class MermaidErd:
    def __init__(self, database: Database):
        super().__init__()
        self.database = database

    def get_erd(self, schema: str, use_table_comment: bool, relation_type: str) -> str | None:
        if schema not in self.database.schemas:
            return None

        self.database.select_schema(schema)

        mmd = f"erDiagram\n\n"
        mmd += f"    %% Entity Relationship Diagram - {schema}\n\n"

        # First define all entities and their attributes
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

            # Start entity definition
            mmd += f"    {table_short_name} {{\n"

            for column in self.database.get_columns(table_name):
                line = "        "
                col_type = get_column_type_name(column.type)

                # In Mermaid, we can specify if a field is required using PK/FK notation
                if primary_keys is not None and column.name in primary_keys:
                    line += f"{col_type} {column.name} PK"
                elif relation_type == 'laravel':
                    related = self.database.get_related_table_laravel(column.name)
                    if related is not None:
                        line += f"{col_type} {column.name} FK"
                    else:
                        line += f"{col_type} {column.name}"
                elif foreign_keys is not None and column.name in foreign_keys:
                    line += f"{col_type} {column.name} FK"
                else:
                    line += f"{col_type} {column.name}"

                if not column.nullable:
                    line += " \"required\""

                mmd += line + "\n"

            mmd += "    }\n\n"

        # Then define relationships
        for table_name in self.database.table_names:
            table_short_name = self.database.get_table_short_name(table_name)

            for column in self.database.get_columns(table_name):
                if relation_type == 'laravel':
                    related = self.database.get_related_table_laravel(column.name)
                    if related is not None:
                        # In Mermaid, relationship syntax is: EntityA [relationship] EntityB : label
                        # ||--o| means zero or one
                        # ||--|| means exactly one
                        if column.nullable:
                            mmd += f"    {table_short_name} ||--o| {related} : {column.name}\n"
                        else:
                            mmd += f"    {table_short_name} ||--|| {related} : {column.name}\n"

        return mmd
