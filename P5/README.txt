Our search approach was basic A* with adjustments. In order to be entered into the queue
a state must not have been visited before or must have a time cost less than the previous state.
The heuristic implemented prioritizes effective tools over least effective tools. Also
crafting tools have more priority than other actions. In addition to this, we created a complete
list of possible items neeeded to achieve the goal. We compare this to our current state list so that
if we ever have more items than we at most need than that state is not considered at all.