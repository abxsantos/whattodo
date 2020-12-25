from click.testing import CliRunner
from src.cli import whattodo_cli


def test_whattodo_cli_entrypoint():
    runner = CliRunner()
    result = runner.invoke(whattodo_cli)
    assert result.exit_code == 0
    assert "What Todo" in result.output
