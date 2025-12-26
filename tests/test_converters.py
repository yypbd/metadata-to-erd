import pytest
from sqlalchemy import Integer, String, DateTime
from src.converter import get_column_type_name

def test_get_column_type_name_basic_types():
    assert get_column_type_name(String()) == "text"
    assert get_column_type_name(Integer()) == "number"
    assert get_column_type_name(DateTime()) == "datetime"

def test_get_column_type_name_custom_type():
    class CustomType:
        python_type = str

    assert get_column_type_name(CustomType()) == "text"

def test_get_column_type_name_with_data_type():
    class TypeWithDataType:
        class DataType:
            python_type = int
        data_type = DataType()

    assert get_column_type_name(TypeWithDataType()) == "number"

