#Task7: Implementation of Monkey Banana Problem in Goal stack planning using python by applying following constraints.

def move(subject, x1, x2):
 return f"Move {subject} from {x1} to {x2}"
def push_box(x1, x2):
 return f"Push box from {x1} to {x2}"
def climb_box(x, direction):
 return f"Climb box at {x} {direction}"
def have_banana(x):
 return f"Have banana at {x}"
initial_state = {
 'monkeyAt0': True,
 'monkeyLevel': 'Down',
 'bananaAt1': True,
 'boxAt2': True
}
goal_state = {
 'GetBanana': True,
 'at': 1
}
def plan_actions(initial_state, goal_state):
 actions = []
 if initial_state['monkeyAt0'] and initial_state['bananaAt1']:
     actions.append(move('Monkey',0,1))
     actions.append(climb_box(1,'Up'))
     actions.append(have_banana(1))
 return actions
actions = plan_actions(initial_state, goal_state)

print("Plan:")
for action in actions:
 print(action)
    

#Output:

#Plan:
# Move Monkey from 0 to 1
# Climb box at 1 Up
# Have banana at 1
   
