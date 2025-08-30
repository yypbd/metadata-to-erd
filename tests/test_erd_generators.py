import pytest
from src.plantuml_erd import PlantumlErd
from src.d2_erd import D2Erd
from src.mermaid_erd import MermaidErd
from src.database import Database

@pytest.fixture
def database(test_db):
    db = Database()
    db.connect('sqlite:///:memory:')
    return db

def test_plantuml_erd_generation(test_db):
    generator = PlantumlErd(test_db)
    output = generator.get_erd('main', True, 'none')
    assert output is not None
    assert '@startuml' in output
    assert '@enduml' in output
    assert 'entity' in output

def test_d2_erd_generation(test_db):
    generator = D2Erd(test_db)
    output = generator.get_erd('main', True, 'none')
    assert output is not None
    assert 'shape: sql_table' in output

def test_mermaid_erd_generation(test_db):
    generator = MermaidErd(test_db)
    output = generator.get_erd('main', True, 'none')
    assert output is not None
    assert 'erDiagram' in output

@pytest.mark.parametrize("generator_class", [PlantumlErd, D2Erd, MermaidErd])
def test_invalid_schema(test_db, generator_class):
    generator = generator_class(test_db)
    output = generator.get_erd('nonexistent', True, 'none')
    assert output is None

@pytest.mark.parametrize("generator_class", [PlantumlErd, D2Erd, MermaidErd])
def test_laravel_relations(test_db, generator_class):
    generator = generator_class(test_db)
    output = generator.get_erd('main', True, 'laravel')
    assert output is not None
    # Add specific assertions for Laravel-style relationships
