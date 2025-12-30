import signal
import time
from datetime import datetime
from pathlib import Path

from .llm import LLMClient
from .memory import Goals, Journal, ensure_dirs, get_agent_dir, setup_logging
from .prompts import EXECUTE, PLAN, REFLECT, SELF_MODIFY, SYSTEM


class Agent:
    """Autonomous self-improving agent."""

    def __init__(self, agent_dir: Path | None = None):
        self.agent_dir = agent_dir or get_agent_dir()
        ensure_dirs(self.agent_dir)

        self.llm = LLMClient()
        self.journal = Journal(self.agent_dir)
        self.goals = Goals(self.agent_dir)
        self.logger = setup_logging(self.agent_dir)

        self.running = False
        self.last_activity_time = time.time()
        self.idle_threshold_seconds = 3600  # 1 hour

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    def _handle_shutdown(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self.logger.info("shutdown_requested", signal=signum)
        self.running = False

    def _should_reflect(self) -> bool:
        """Determine if reflection should trigger."""
        # TODO: Add proper tracking for:
        # - After completing a goal
        # - Every hour if idle
        # - User-triggered (via external signal)
        return False

    def _get_context(self) -> str:
        """Get current context for prompts."""
        return f"""Current time: {datetime.now().isoformat()}
Agent directory: {self.agent_dir}
PID: {__import__('os').getpid()}
Last activity: {datetime.fromtimestamp(self.last_activity_time).isoformat()}"""

    def _get_history(self) -> str:
        """Get relevant history for planning."""
        notes = self.journal.read("notes.md")
        reflections = self.journal.read("reflections.md")
        return f"## Recent Notes\n{notes}\n\n## Recent Reflections\n{reflections}"

    def _plan(self, goal: str) -> str:
        """Plan how to achieve a goal."""
        self.logger.info("planning", goal=goal[:100])

        context = self._get_context()
        history = self._get_history()

        prompt = PLAN.format(
            goal=goal,
            context=context,
            history=history,
        )

        response = self.llm.complete(prompt, system=SYSTEM.format(context=context))

        self.journal.append("notes.md", f"## Plan for: {goal}\n\n{response}")
        return response

    def _execute(self, goal: str, plan: str) -> str:
        """Execute a plan toward a goal."""
        self.logger.info("executing", goal=goal[:100])
        self.last_activity_time = time.time()

        context = self._get_context()

        prompt = EXECUTE.format(
            goal=goal,
            plan=plan,
        )

        response = self.llm.complete(prompt, system=SYSTEM.format(context=context))

        self.journal.append("notes.md", f"## Execution result for: {goal}\n\n{response}")
        return response

    def _reflect(self) -> tuple[bool, str | None]:
        """Reflect on recent operations and identify improvements."""
        self.logger.info("reflecting")

        context = self._get_context()

        # Gather information
        notes = self.journal.read("notes.md")
        user_feedback = self.journal.read("user-feedback.md") if self.journal.exists("user-feedback.md") else ""

        prompt = REFLECT.format(
            operations=notes,
            goals=self.goals.get_active() or "(No active goals - idle)",
            user_feedback=user_feedback or "(No user feedback)",
        )

        response = self.llm.complete(prompt, system=SYSTEM.format(context=context))

        self.journal.write("reflections.md", response)

        # Check if reflection identifies improvements
        # For now, we'll look for keywords like "improve", "change", "modify"
        needs_improvement = any(
            word in response.lower() for word in ["improve", "change", "modify", "should", "recommend"]
        )

        return needs_improvement, response

    def _self_modify(self, improvement: str) -> bool:
        """Improve the agent's own implementation."""
        self.logger.info("self_modifying", improvement=improvement[:100])

        context = self._get_context()

        # Get code structure
        src_dir = Path(__file__).parent
        code_structure = self._describe_code_structure(src_dir)

        prompt = SELF_MODIFY.format(
            improvement=improvement,
            code_structure=code_structure,
        )

        response = self.llm.complete(prompt, system=SYSTEM.format(context=context))

        self.journal.append("notes.md", f"## Self-modification\n\n{response}")
        return True

    def _describe_code_structure(self, src_dir: Path) -> str:
        """Describe the agent's code structure."""
        parts = []
        for py_file in src_dir.rglob("*.py"):
            rel_path = py_file.relative_to(src_dir)
            parts.append(f"- {rel_path}")

        return "\n".join(parts) if parts else "(No Python files found)"

    def run(self) -> None:
        """Main run loop."""
        self.logger.info("agent_started")
        self.running = True

        while self.running:
            try:
                # 1. Read goals
                active_goals = self.goals.get_active()

                if not active_goals.strip():
                    # No goals - enter self-improvement mode
                    self.logger.info("no_goals", message="Entering self-improvement mode")
                    goal = "Improve yourself: Analyze your implementation and suggest optimizations"

                    # Check if we should reflect (hourly idle check)
                    idle_time = time.time() - self.last_activity_time
                    if idle_time >= self.idle_threshold_seconds:
                        needs_improvement, reflection = self._reflect()
                        if needs_improvement and reflection:
                            self._self_modify(reflection)
                        continue
                else:
                    # Parse first goal from active.md
                    # For now, assume one goal per line or first paragraph
                    goal = active_goals.strip().split("\n\n")[0].strip()

                # 2. Plan
                plan = self._plan(goal)

                # 3. Execute
                result = self._execute(goal, plan)

                # 4. Journal execution results
                self.journal.append("notes.md", f"## Completed: {goal}\n\n{result}")

                # 5. Check for reflection trigger
                if self._should_reflect():
                    needs_improvement, reflection = self._reflect()
                    if needs_improvement and reflection:
                        self._self_modify(reflection)

                # 6. Journal reflection results (if any)
                # (handled in reflect and self_modify)

                # Small delay to prevent tight loop
                time.sleep(1)

            except Exception as e:
                self.logger.error("error", error=str(e), error_type=type(e).__name__)
                self.journal.append("notes.md", f"## Error\n\n{type(e).__name__}: {e}")
                time.sleep(5)  # Back off on error

        self.logger.info("agent_stopped")

    def reflect_now(self) -> None:
        """Trigger an immediate reflection cycle."""
        self.logger.info("manual_reflection")
        needs_improvement, reflection = self._reflect()
        if needs_improvement and reflection:
            self._self_modify(reflection)

    def status(self) -> dict:
        """Get current agent status."""
        return {
            "running": self.running,
            "agent_dir": str(self.agent_dir),
            "last_activity": datetime.fromtimestamp(self.last_activity_time).isoformat(),
            "idle_seconds": time.time() - self.last_activity_time,
            "tokens_used": self.llm.total_tokens,
            "active_goals": self.goals.get_active()[:200] if self.goals.get_active() else "(none)",
        }
