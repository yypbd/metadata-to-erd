from sqlalchemy import create_engine, inspect, MetaData, Column


class Database:
    def __init__(self, database_url: str):
        self.engine = create_engine(
            database_url,
            isolation_level="REPEATABLE READ",
        )

        self.db_inspect = inspect(self.engine)
        self.schemas = self.db_inspect.get_schema_names()
        self.metadata = MetaData()
        self.table_names = []

    def get_schemas(self) -> list[str]:
        return self.schemas

    def select_schema(self, schema: str):
        self.metadata.reflect(bind=self.engine, schema=schema)
        self.table_names = self.metadata.tables.keys()

    def get_table_comment(self, table_name: str) -> str:
        table = self.metadata.tables[table_name]
        if table is None or table.comment is None:
            return table_name

        return table.comment

    def get_primary_keys(self, table_name: str) -> list[str]:
        table = self.metadata.tables[table_name]
        if table is None:
            return []

        return [col.name for col in table.primary_key]

    def get_foreign_keys(self, table_name: str) -> list[str]:
        table = self.metadata.tables[table_name]
        if table is None:
            return []

        return [col.name for col in table.foreign_keys]

    def get_columns(self, table_name: str) -> list[Column]:
        table = self.metadata.tables[table_name]
        return table.columns

    def is_foreign_key_laravel(self,  column_name: str) -> bool:
        if column_name.endswith("_id"):
            related_table_name = column_name[:-3] + "s"
            return related_table_name in self.table_names

        return False
