import logging
import os
from datetime import datetime
from pathlib import Path

import structlog


def get_agent_dir() -> Path:
    """Get the agent directory, searching upward from current directory."""
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        agent_dir = parent / "agent"
        if agent_dir.is_dir():
            return agent_dir
    # Fallback: create in current directory
    return cwd / "agent"


def get_journal_dir(agent_dir: Path | None = None) -> Path:
    """Get the journal directory for today."""
    agent_dir = agent_dir or get_agent_dir()
    today = datetime.now().strftime("%Y/%m/%d")
    return agent_dir / "journal" / today


def get_logs_dir(agent_dir: Path | None = None) -> Path:
    """Get the logs directory for today."""
    agent_dir = agent_dir or get_agent_dir()
    today = datetime.now().strftime("%Y/%m/%d")
    return agent_dir / "logs" / today


def get_goals_dir(agent_dir: Path | None = None) -> Path:
    """Get the goals directory."""
    agent_dir = agent_dir or get_agent_dir()
    return agent_dir / "goals"


def ensure_dirs(agent_dir: Path | None = None) -> None:
    """Ensure all required directories exist."""
    agent_dir = agent_dir or get_agent_dir()
    journal_dir = get_journal_dir(agent_dir)
    logs_dir = get_logs_dir(agent_dir)
    goals_dir = get_goals_dir(agent_dir)

    for d in [journal_dir, logs_dir, goals_dir]:
        d.mkdir(parents=True, exist_ok=True)


def setup_logging(agent_dir: Path | None = None) -> structlog.stdlib.BoundLogger:
    """Set up structured logging."""
    agent_dir = agent_dir or get_agent_dir()
    logs_dir = get_logs_dir(agent_dir)
    ensure_dirs(agent_dir)

    pid = os.getpid()
    log_file = logs_dir / f"{pid}.log"

    # Configure standard logging for file output
    logging.basicConfig(
        filename=str(log_file),
        level=logging.INFO,
        format="%(message)s",
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


class Journal:
    """Manages journal entries for the agent."""

    def __init__(self, agent_dir: Path | None = None):
        self.agent_dir = agent_dir or get_agent_dir()
        self.journal_dir = get_journal_dir(self.agent_dir)
        ensure_dirs(self.agent_dir)

    def _get_file(self, name: str) -> Path:
        """Get a journal file path, creating parent dirs if needed."""
        return self.journal_dir / name

    def append(self, filename: str, content: str) -> None:
        """Append content to a journal file."""
        path = self._get_file(filename)
        timestamp = datetime.now().isoformat()
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "a") as f:
            f.write(f"\n## {timestamp}\n{content}\n")

    def read(self, filename: str) -> str:
        """Read a journal file."""
        path = self._get_file(filename)
        if path.exists():
            return path.read_text()
        return ""

    def write(self, filename: str, content: str) -> None:
        """Write content to a journal file (overwrite)."""
        path = self._get_file(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def exists(self, filename: str) -> bool:
        """Check if a journal file exists."""
        return self._get_file(filename).exists()


class Goals:
    """Manages the agent's goal queue."""

    def __init__(self, agent_dir: Path | None = None):
        self.agent_dir = agent_dir or get_agent_dir()
        self.goals_dir = get_goals_dir(self.agent_dir)
        self.active_file = self.goals_dir / "active.md"
        self.completed_file = self.goals_dir / "completed.md"
        ensure_dirs(self.agent_dir)

    def get_active(self) -> str:
        """Get active goals."""
        if self.active_file.exists():
            return self.active_file.read_text()
        return ""

    def set_active(self, content: str) -> None:
        """Set active goals."""
        self.active_file.parent.mkdir(parents=True, exist_ok=True)
        self.active_file.write_text(content)

    def append_completed(self, goal: str, result: str) -> None:
        """Append a completed goal with its result."""
        timestamp = datetime.now().isoformat()
        entry = f"\n## Completed: {timestamp}\n\n**Goal:** {goal}\n\n**Result:** {result}\n"
        with open(self.completed_file, "a") as f:
            f.write(entry)

    def is_empty(self) -> bool:
        """Check if there are active goals."""
        return not self.get_active().strip()
