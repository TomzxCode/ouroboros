import subprocess
from datetime import datetime

import typer

from .core import Agent
from .memory import get_agent_dir, get_journal_dir, get_logs_dir

app = typer.Typer(help="Ouroboros - Autonomous self-improving agent")


@app.command()
def run() -> None:
    """Start the agent's main loop."""
    agent = Agent()
    agent.run()


@app.command()
def reflect() -> None:
    """Trigger an immediate reflection cycle."""
    agent = Agent()
    agent.reflect_now()


@app.command()
def status() -> None:
    """Show current agent status."""
    agent_dir = get_agent_dir()
    agent = Agent(agent_dir)

    s = agent.status()

    typer.echo("Ouroboros Status")
    typer.echo("=" * 40)
    typer.echo(f"Running: {s['running']}")
    typer.echo(f"Agent directory: {s['agent_dir']}")
    typer.echo(f"Last activity: {s['last_activity']}")
    typer.echo(f"Idle for: {s['idle_seconds']:.0f} seconds")
    typer.echo(f"Tokens used: {s['tokens_used']}")
    typer.echo()
    typer.echo("Active goals:")
    typer.echo(s['active_goals'] or "(none)")


@app.command()
def tail_logs(
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow log output"),
    lines: int = typer.Option(50, "--lines", "-n", help="Number of lines to show"),
) -> None:
    """Show the current log file."""
    agent_dir = get_agent_dir()
    logs_dir = get_logs_dir(agent_dir)

    # Find most recent log file
    log_files = sorted(logs_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)

    if not log_files:
        typer.echo("No log files found.")
        return

    log_file = log_files[0]
    typer.echo(f"Showing: {log_file}")
    typer.echo()

    if follow:
        subprocess.run(["tail", "-f", str(log_file)])
    else:
        result = subprocess.run(["tail", "-n", str(lines), str(log_file)], capture_output=True, text=True)
        typer.echo(result.stdout)


@app.command("feedback")
def feedback_cmd(
    message: str = typer.Argument(..., help="Feedback message to provide to the agent"),
) -> None:
    """Add feedback for the agent to consume during reflection."""
    agent_dir = get_agent_dir()
    journal_dir = get_journal_dir(agent_dir)
    feedback_file = journal_dir / "user-feedback.md"

    timestamp = datetime.now().isoformat()
    entry = f"\n## {timestamp}\n\n{message}\n"

    feedback_file.parent.mkdir(parents=True, exist_ok=True)
    with open(feedback_file, "a") as f:
        f.write(entry)

    typer.echo(f"Feedback added to: {feedback_file}")


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
