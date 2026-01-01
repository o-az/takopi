from takopi import cli, engines


def test_engine_discovery_skips_non_backend() -> None:
    ids = engines.list_backend_ids()
    assert "codex" in ids
    assert "claude" in ids
    assert "mock" not in ids


def test_cli_registers_engine_commands_sorted() -> None:
    command_names = [cmd.name for cmd in cli.app.registered_commands]
    assert command_names == engines.list_backend_ids()
