from sqlalchemy import create_engine, inspect, MetaData


class PlantumlErd(object):
    def __init__(self, db_url: str):
        super().__init__()

        self.engine = create_engine(
            db_url,
            isolation_level="REPEATABLE READ",
        )

        self.db_inspect = inspect(self.engine)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        self.schemas = self.db_inspect.get_schema_names()

    def _get_table_comment(self, table_name: str) -> str:
        table = self.metadata.tables[table_name]
        if table is None:
            return table_name

        if table.comment is None:
            return table_name

        return table.comment

    def _get_primary_keys(self, table_name: str):
        table = self.metadata.tables[table_name]
        if table is None:
            return None

        return [col.name for col in table.primary_key]

    def _get_foreign_keys(self, table_name: str):
        table = self.metadata.tables[table_name]
        if table is None:
            return None

        return [col.name for col in table.foreign_keys]

    def _is_foreign_key_laravel(self, table_names: list[str], column_name: str) -> bool:
        if column_name.endswith("_id"):
            related_table_name = column_name[:-3] + "s"
            return related_table_name in table_names

        return False

    def _get_type_name(self, column_type):
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

    def get_schemas(self):
        return self.schemas

    def get_erd(self, schema: str, use_table_comment: bool, relation_type: str) -> str | None:
        if schema not in self.schemas:
            return None

        table_names = self.db_inspect.get_table_names(schema=schema)

        puml = "@startuml\r\n\r\n"
        relations = ""
        for table_name in table_names:
            if use_table_comment:
                desc = self._get_table_comment(table_name)
            else:
                desc = table_name
            primary_keys = self._get_primary_keys(table_name)
            foreign_keys = self._get_foreign_keys(table_name)

            puml += f"entity \"{desc}\" as {table_name} " + "{\r\n"

            for column in self.db_inspect.get_columns(table_name, schema=schema):
                line = "  "
                if not column['nullable']:
                    line += "*"

                line += column['name'] + " : " + self._get_type_name(column['type'])

                # if column['autoincrement']:
                #     line += " <<generated>>"
                if primary_keys is not None:
                    if column['name'] in primary_keys:
                        line += " <<PK>>"

                if relation_type == 'laravel':
                    if self._is_foreign_key_laravel(table_names, column['name']):
                        line += " <<FK>>"
                        relations += table_name + " }|--|| " + column['name'][:-3] + "s : " + column['name'] + "\r\n"
                else:
                    if foreign_keys is not None and column['name'] in foreign_keys:
                        line += " <<FK>>"

                puml += line + "\r\n"

            puml += "}\r\n\r\n"

        puml += relations + "\r\n"
        puml += "@enduml\r\n"

        return puml
