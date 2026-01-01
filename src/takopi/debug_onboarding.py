from __future__ import annotations

import typer

from .backends import SetupIssue
from .config import ConfigError
from .engines import get_backend, list_backend_ids
from .onboarding import SetupResult, check_setup, config_issue, render_setup_guide


def _dedupe_issues(issues: list[SetupIssue]) -> list[SetupIssue]:
    seen: set[SetupIssue] = set()
    deduped: list[SetupIssue] = []
    for issue in issues:
        if issue in seen:
            continue
        seen.add(issue)
        deduped.append(issue)
    return deduped


def run(
    engine: str = typer.Option(
        "codex",
        "--engine",
        help=f"Engine backend id ({', '.join(list_backend_ids())}).",
    ),
    force: bool = typer.Option(
        True,
        "--force/--no-force",
        help="Render onboarding panel even if setup looks OK.",
    ),
) -> None:
    try:
        backend = get_backend(engine)
    except ConfigError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)
    setup = check_setup(backend)
    if force:
        install_issue = backend.install_issue or SetupIssue(
            f"Install {backend.display_name}",
            ("   [dim]See engine setup docs for install instructions.[/]",),
        )
        forced_issues = [
            install_issue,
            config_issue(setup.config_path),
        ]
        setup = SetupResult(
            issues=_dedupe_issues([*setup.issues, *forced_issues]),
            config_path=setup.config_path,
        )
    render_setup_guide(setup)


def main() -> None:
    typer.run(run)


if __name__ == "__main__":
    main()
