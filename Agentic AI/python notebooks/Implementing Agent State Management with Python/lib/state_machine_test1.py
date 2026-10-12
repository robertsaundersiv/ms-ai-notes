"""A minimal state machine for orchestrating agent workflows.

A workflow is a graph of steps. Each step reads the shared state (a TypedDict),
returns a partial update, and the machine merges that update into the state
before moving to the next step. Execution starts at an EntryPoint and stops
when it reaches a Termination.

Example:
    class MyState(TypedDict):
        count: int

    machine = StateMachine[MyState](MyState)
    entry = EntryPoint[MyState]()
    increment = Step[MyState]("increment", lambda s: {"count": s["count"] + 1})
    end = Termination[MyState]()

    machine.add_steps([entry, increment, end])
    machine.connect(entry, increment)
    machine.connect(increment, end)

    run = machine.run({"count": 0})
    print(run.final_state)  # {'count': 1}
"""

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, Generic, List, Mapping, Optional, TypeVar, Union, cast

# Bound to Mapping so Pylance knows the state can be unpacked with ** (TypedDicts satisfy this)
StateSchema = TypeVar("StateSchema", bound=Mapping[str, Any])


def _no_update(_: Any) -> None:
    """Step logic that leaves the state unchanged (used by EntryPoint and Termination)."""
    return None


class Step(Generic[StateSchema]):
    """A single unit of work in the workflow.

    Args:
        step_id: Unique name for this step
        logic: Function that receives the current state and returns a dict of
            updates to merge into it (or None for no changes)
    """

    # Mapping (not Dict) so logic can return the full TypedDict state or a partial dict of updates
    def __init__(self, step_id: str, logic: Callable[[StateSchema], Optional[Mapping[str, Any]]]):
        self.step_id = step_id
        self.logic = logic

    def run(self, state: StateSchema) -> StateSchema:
        updates = self.logic(state) or {}
        # Merging produces a plain dict; cast it back to the caller's state type
        return cast(StateSchema, {**state, **updates})

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.step_id!r})"


class EntryPoint(Step[StateSchema]):
    """The step where execution begins. Passes the state through unchanged."""

    def __init__(self, step_id: str = "__entry__"):
        super().__init__(step_id, _no_update)


class Termination(Step[StateSchema]):
    """The step where execution ends. Passes the state through unchanged."""

    def __init__(self, step_id: str = "__termination__"):
        super().__init__(step_id, _no_update)


@dataclass
class Transition(Generic[StateSchema]):
    """An edge from one step to one or more possible next steps.

    With a single target, the machine always moves there. With several targets,
    `condition` picks one: it receives the state and returns the chosen Step or
    its step_id.
    """
    source: str
    targets: List[str]
    condition: Optional[Callable[[StateSchema], Union[Step, str]]] = None

    def resolve(self, state: StateSchema) -> str:
        if self.condition is None:
            if len(self.targets) != 1:
                raise ValueError(
                    f"Step '{self.source}' has {len(self.targets)} targets but no condition to choose between them"
                )
            return self.targets[0]

        choice = self.condition(state)
        target_id = choice.step_id if isinstance(choice, Step) else choice
        if target_id not in self.targets:
            raise ValueError(
                f"Condition on '{self.source}' returned '{target_id}', which is not one of {self.targets}"
            )
        return target_id


@dataclass
class Snapshot(Generic[StateSchema]):
    """The state right after a step ran."""
    step_id: str
    state: StateSchema
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Run(Generic[StateSchema]):
    """The result of one execution: every snapshot in order, plus the final state."""
    snapshots: List[Snapshot] = field(default_factory=list)

    @property
    def final_state(self) -> Optional[StateSchema]:
        return self.snapshots[-1].state if self.snapshots else None

    @property
    def path(self) -> List[str]:
        return [snapshot.step_id for snapshot in self.snapshots]


class StateMachine(Generic[StateSchema]):
    """Runs a graph of Steps, threading a shared state through them.

    Args:
        state_schema: The TypedDict class describing the state (kept for reference)
    """

    def __init__(self, state_schema: type):
        self.state_schema = state_schema
        self.steps: Dict[str, Step[StateSchema]] = {}
        self.transitions: Dict[str, Transition[StateSchema]] = {}

    def add_steps(self, steps: List[Step[StateSchema]]) -> None:
        for step in steps:
            if step.step_id in self.steps:
                raise ValueError(f"Duplicate step_id '{step.step_id}'")
            self.steps[step.step_id] = step

    def connect(
        self,
        source: Step[StateSchema],
        targets: Union[Step[StateSchema], List[Step[StateSchema]]],
        condition: Optional[Callable[[StateSchema], Union[Step, str]]] = None,
    ) -> None:
        """Add an edge from `source` to one target, or to several chosen by `condition`."""
        if isinstance(targets, Step):
            targets = [targets]
        for step in [source, *targets]:
            if step.step_id not in self.steps:
                raise ValueError(f"Step '{step.step_id}' must be added with add_steps() before connecting it")
        self.transitions[source.step_id] = Transition(
            source=source.step_id,
            targets=[t.step_id for t in targets],
            condition=condition,
        )

    def run(self, state: StateSchema, max_steps: int = 100) -> Run[StateSchema]:
        """Execute from the EntryPoint until a Termination is reached.

        Args:
            state: The initial state
            max_steps: Safety limit so a cycle in the graph can't loop forever
        """
        entry_points = [s for s in self.steps.values() if isinstance(s, EntryPoint)]
        if len(entry_points) != 1:
            raise ValueError(f"Expected exactly one EntryPoint, found {len(entry_points)}")

        run = Run[StateSchema]()
        current = entry_points[0]
        state = deepcopy(state)

        for _ in range(max_steps):
            state = current.run(state)
            run.snapshots.append(Snapshot(step_id=current.step_id, state=deepcopy(state)))

            if isinstance(current, Termination):
                return run

            transition = self.transitions.get(current.step_id)
            if transition is None:
                raise ValueError(f"Step '{current.step_id}' has no outgoing transition and is not a Termination")
            current = self.steps[transition.resolve(state)]

        raise RuntimeError(f"Run exceeded max_steps={max_steps}; check for an infinite loop")
