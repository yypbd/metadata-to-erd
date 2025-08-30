import inflect
from sqlalchemy import create_engine, inspect, MetaData, Column


class Database:
    def __init__(self):
        self.engine = None
        self.db_inspect = None
        self.schemas = None
        self.metadata = None
        self.table_names = None
        self.table_short_names = None
        self.is_connected = False

    def connect(self, database_url: str) -> bool:
        try:
            # SQLite uses different isolation levels
            if database_url.startswith('sqlite'):
                self.engine = create_engine(database_url)
            else:
                self.engine = create_engine(
                    database_url,
                    isolation_level="REPEATABLE READ",
                )

            self.db_inspect = inspect(self.engine)
            self.schemas = self.db_inspect.get_schema_names()
            self.metadata = MetaData()
            self.table_names = []
            self.table_short_names = []
            self.is_connected = True

            return True
        except Exception as e:
            self.engine = None
            self.db_inspect = None
            self.schemas = None
            self.metadata = None
            self.table_names = None
            self.table_short_names = None
            self.is_connected = False

            print('[error] connect exception - ' + str(e))

            return False

    def get_schemas(self) -> list[str]:
        if not self.is_connected:
            return []

        return self.schemas

    def select_schema(self, schema: str):
        if not self.is_connected:
            return

        self.metadata.reflect(bind=self.engine, schema=schema)
        self.table_names = self.metadata.tables.keys()
        self.table_short_names = []
        for table in self.metadata.tables:
            self.table_short_names.append(self.metadata.tables[table].name)

    def get_table_comment(self, table_name: str) -> str | None:
        if not self.is_connected:
            return None

        table = self.metadata.tables[table_name]
        if table.comment is None or table.comment == "":
            return table.name

        # If table.comment has multiple lines, use only the first line.
        if "\n" in table.comment:
            return table.comment.split("\n")[0].strip()

        return table.comment

    def get_table_short_name(self, table_name: str) -> str:
        if not self.is_connected:
            return table_name

        table = self.metadata.tables[table_name]
        return table.name

    def get_primary_keys(self, table_name: str) -> list[str]:
        if not self.is_connected:
            return []

        table = self.metadata.tables[table_name]
        if table is None:
            return []

        return [col.name for col in table.primary_key]

    def get_foreign_keys(self, table_name: str) -> list[str]:
        if not self.is_connected:
            return []

        table = self.metadata.tables[table_name]
        if table is None:
            return []

        return [col.name for col in table.foreign_keys]

    def get_columns(self, table_name: str) -> list[Column]:
        if not self.is_connected:
            return []

        table = self.metadata.tables[table_name]
        return table.columns

    # def is_foreign_key_laravel(self,  column_name: str) -> bool:
    #     if column_name.endswith("_id"):
    #         p = inflect.engine()
    #         related_table_name = p.plural(text=column_name[:-3])
    #         return related_table_name in self.table_short_names
    #
    #     return False

    def get_related_table_laravel(self,  column_name: str) -> str | None:
        if not self.is_connected:
            return None

        if column_name.endswith("_id"):
            p = inflect.engine()
            related_table_name = p.plural(text=column_name[:-3])
            if related_table_name in self.table_short_names:
                return related_table_name

        return None
