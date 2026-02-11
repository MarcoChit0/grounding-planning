
#
# This file is part of pyperplan.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

"""
Implements the breadth first search algorithm.
"""
from ..task import Task

def grounded(planning_task: Task):
    print("--------------------------------")
    print("Initial State Facts:")
    for fact in planning_task.initial_state:
        print(fact)
    print("--------------------------------")
    print("Goal Facts:")
    for fact in planning_task.goals:
        print(fact)
    print("--------------------------------")
    print("Operators:")
    for op in planning_task.operators:
        print("name: ", op.name, "; preconditions: ", ', '.join(list(op.preconditions)), "; delete effects: ", ', '.join(list(op.del_effects)), "; add effects: ", ', '.join(list(op.add_effects)))
    print("--------------------------------")
    exit(1)
