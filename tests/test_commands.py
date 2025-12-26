import os
import pytest
from click.testing import CliRunner
from click_command import erd, schemas
from dotenv import load_dotenv

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture(scope="session", autouse=True)
def env_setup():
    old_env = os.getenv("DATABASE_URL")
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    load_dotenv()  # Reload environment variables
    yield
    if old_env:
        os.environ["DATABASE_URL"] = old_env
    else:
        del os.environ["DATABASE_URL"]

def test_schemas_command(runner, env_setup):
    result = runner.invoke(schemas)
    assert result.exit_code == 0
    # Add more specific assertions based on expected output

def test_erd_command_basic(runner, env_setup):
    result = runner.invoke(erd)
    assert result.exit_code == 0
    # Add more specific assertions based on expected output

@pytest.mark.parametrize("engine", ["puml", "d2", "mermaid"])
def test_erd_different_engines(runner, env_setup, engine, tmp_path):
    output_file = tmp_path / f"output.{engine}"
    result = runner.invoke(erd, [
        "--engine", engine,
        "--out_filename", str(output_file)
    ])
    assert result.exit_code == 0
    assert output_file.exists()

def test_erd_with_table_comments(runner, env_setup):
    result = runner.invoke(erd, ["--use_table_comment", "True"])
    assert result.exit_code == 0
    # Add assertions for table comment inclusion

@pytest.mark.parametrize("relation_type", ["none", "laravel"])
def test_erd_relation_types(runner, env_setup, relation_type):
    result = runner.invoke(erd, ["--relation_type", relation_type])
    assert result.exit_code == 0
    # Add assertions for relationship detection

def test_erd_invalid_schema(runner, env_setup):
    # 메모리 데이터베이스에는 스키마가 없으므로, 연결 실패를 시뮬레이션
    result = runner.invoke(erd, ["--schema", "nonexistent"])
    # 메모리 DB에서는 스키마가 없어서 "No schemas found" 에러가 발생할 수 있음
    assert result.exit_code == 1

def test_erd_invalid_engine(runner, env_setup):
    result = runner.invoke(erd, ["--engine", "invalid"])
    assert result.exit_code != 0
    assert "invalid value" in result.output.lower()

def test_erd_file_exists(runner, env_setup, tmp_path):
    output_file = tmp_path / "test.puml"
    output_file.write_text("existing content")

    result = runner.invoke(erd, ["--out_filename", str(output_file)])
    # 파일이 존재하면 "File exists" 에러가 발생해야 함
    assert result.exit_code == 1
