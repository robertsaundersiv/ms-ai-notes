from typing import TypedDict
from lib.state_machine import (
    StateMachine,
    Step,
    EntryPoint,
    Termination,
)
import pprint
pp = pprint.PrettyPrinter(indent=2)

class Schema(TypedDict):
    input: int
    output: int

workflow = StateMachine(Schema)

def step_input(state:Schema) -> Schema:
    return {"output": state["input"]+1, "input": state["input"]}

def step_double(state:Schema) -> Schema:
    return {"output": state["input"]*2, "input": state["input"]}

entry = EntryPoint()
s1 = Step("input", step_input)
s2 = Step("double", step_double)
termination = Termination()

workflow.add_steps([entry, s1, s2, termination])
workflow.connect(entry, s1)
workflow.connect(s1, s2)
workflow.connect(s2, termination)

initial_state = {"input": 4}
run_object = workflow.run(initial_state)
pp.pprint(run_object)

pp.pprint(run_object.snapshots)

class CounterSchema(TypedDict):
    count: int
    max_value: int

workflow2 = StateMachine(CounterSchema)

def increment_counter(state:CounterSchema) -> CounterSchema:
    return {"count": state["count"] + 1, "max_value": state["max_value"]}

entry = EntryPoint()
increment = Step("increment", increment_counter)
termination = Termination()

workflow2.add_steps([entry, increment, termination])

def check_counter(state:CounterSchema) -> Step:
    if state["count"] >= state["max_value"]:
        return termination
    return increment

workflow2.connect(entry, increment)
workflow2.connect(increment, [increment, termination], check_counter)

initial_state = {"count": 0, "max_value": 10}
run_object = workflow2.run(initial_state)
pp.pprint(run_object)
pp.pprint(run_object.snapshots)