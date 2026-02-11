from __future__ import annotations
from ..task import Task, Operator
import copy

# ... (Your Node and Edge classes remain the same) ...
class Node:
    def __init__(self, object: any, label: str):
        self.object = object
        self.label = label
        self.successors: list[Node] = []
        self.predecessors: list[Node] = []
    
    def __str__(self):
        # Make the string representation more compact and readable for debugging
        obj_str = self.object if isinstance(self.object, str) else self.object.name
        return f"<{self.label.upper()}: {obj_str}>"

    # Add hash and eq to make Node objects hashable for sets and dict keys
    def __hash__(self):
        return hash((self.label, str(self.object)))

    def __eq__(self, other):
        return isinstance(other, Node) and self.label == other.label and str(self.object) == str(other.object)
    
    def add_successor(self, successor: Node):
        self.successors.append(successor)
        successor.predecessors.append(self)



def zhu_givan(task: Task):
    """
    Extracts landmarks from a planning task using the Zhu-Givan method
    based on a simplified Relaxed Task Graph (sRTG).
    """
    facts: set[str] = set()
    facts.update(task.initial_state)
    _facts = set()
    operators: set[Operator] = set()
    while len(facts) > len(_facts):
        _facts = facts.copy()
        for op in task.operators:
            if op.preconditions <= facts:
                facts.update(op.add_effects)
                operators.add(op)

    nodes: set[Node] = set()
    operator_to_node_map: dict[Operator, Node] = {}
    fact_to_node_map: dict[str, Node] = {}

    for fact in facts:
        label = "<init>" if fact in task.initial_state else "or"
        node = Node(object=fact, label=label)
        nodes.add(node)
        fact_to_node_map[fact] = node

    for operator in operators:
        node = Node(object=operator, label="and")
        nodes.add(node)
        operator_to_node_map[operator] = node

    for op, op_node in operator_to_node_map.items():
        # Edge from precondition (fact) to operator (AND node).
        for precon in op.preconditions:
            fact_node = fact_to_node_map[precon]
            fact_node.add_successor(op_node)

        # Edge from operator (AND node) to add_effect (fact).
        for effect in op.add_effects:
            fact_node = fact_to_node_map[effect]
            op_node.add_successor(fact_node)

    landmarks = {}
    for node in nodes:
        if node.label == "<init>":
            landmarks[node] = {node}
        else:
            landmarks[node] = nodes.copy()
    changed = True
    while changed:
        changed = False

        for node in nodes:
            if node.label == "<init>":
                continue

            new_lm: set[Node] = set()
            if node.label == "or":
                if len(node.predecessors) > 0:
                    new_lm = landmarks[node.predecessors[0]].copy()
                    for pred in range(1, len(node.predecessors)):
                        new_lm.intersection_update(landmarks[node.predecessors[pred]])
            elif node.label == "and":
                for pred in node.predecessors:
                    new_lm.update(landmarks[pred])
            else:
                 raise ValueError(f"Unknown node label: {node.label}")
            
            new_lm.add(node)

            if new_lm != landmarks[node]:
                landmarks[node] = new_lm
                changed = True
            
    # 7. Return the landmarks for the goal node.
    # You can now use these landmarks in your heuristic.
    goal_landmarks = set()
    for goal in task.goals:
        goal_landmarks.update(landmarks[fact_to_node_map[goal]])

    def is_operator_landmark(operator: Operator, landmarks: set[Node]) -> bool:
        for lm in landmarks:
            if lm.label == "and" and isinstance(lm.object, Operator) and lm.object == operator:
                return True
        return False

    print("--------------------------------")
    print("Initial State Facts:")
    for fact in task.initial_state:
        print(fact)
    print("--------------------------------")
    print("Goal Facts:")
    for fact in task.goals:
        print(fact)
    print("--------------------------------")
    print("Operators:")
    for op in task.operators:

        print("name: ", op.name, "; preconditions: ", ', '.join(list(op.preconditions)), "; delete effects: ", ', '.join(list(op.del_effects)), "; add effects: ", ', '.join(list(op.add_effects)), "; is landmark: ", is_operator_landmark(op, goal_landmarks))
    print("--------------------------------")
    exit(1)