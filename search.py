# This is an application of A* search to the 8-puzzle problem. It is a python application to a simple AI problem using
#the hamming distance and manhattan distance, which one can selected between.

from queue import PriorityQueue
from queue import Queue
import numpy as np

class EightPuzzle:


	def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
		""" Define goal state and initialize a problem """
		self.initial = initial
		self.goal = goal

	def find_blank_square(self, state):
		"""Return the index of the blank square in a given state"""

		return state.index(0)

	def actions(self, state):
		""" Return the actions that can be executed in the given state.
		The result would be a list, since there are only four possible actions
		in any given state of the environment """

		possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
		# blank is the index of the blank square
		index_blank_square = self.find_blank_square(state)

		if index_blank_square % 3 == 0:
			possible_actions.remove('LEFT')
		if index_blank_square < 3:
			possible_actions.remove('UP')
		if index_blank_square % 3 == 2:
			possible_actions.remove('RIGHT')
		if index_blank_square > 5:
			possible_actions.remove('DOWN')

		return possible_actions

	def result(self, state, action):
		""" Given state and action, return a new state that is the result of the action.
		Action is assumed to be a valid action in the state """

		# blank is the index of the blank square
		blank = self.find_blank_square(state)
		new_state = list(state)

		delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
		neighbor = blank + delta[action]
		new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

		return tuple(new_state)

	def goal_test(self, state):
		""" Given a state, return True if state is a goal state or False, otherwise """

		return state == self.goal

	def h(self, state):
		""" Return the heuristic value for a given state. Default heuristic function used is 
		h(n) = number of misplaced tiles. """

		return sum(s != g for (s, g) in zip(state, self.goal))
		
	def h0(self, state):
		""" This is the Manhattan distance which finds the total distance between the current state and
			where each tile should be in the goal state"""
		
		return sum(abs(s-g) for (s, g) in zip(state, self.goal))
parent_vals = []

def succ(state):

	succs = Queue()
	
	if len(a.actions(state[1])) == 0:
		
		return []
	
	else:
	
		for i in range(len(a.actions(state[1]))):
		
			succ = a.result(state[1], a.actions(state[1])[i]) #successor puzzle state
			
			if a.find_blank_square(succ) != a.find_blank_square(state[1]):
			
				succs.queue.append((a.h(succ) + state[3] + 1, [succ, a.actions(state[1])[i], state[3] + 1])) #succ is puzzle state, a.actions gives action, state[1] + 1 is depth
				parent_vals.append((a.h(succ) + state[3] + 1, a.actions(state[1])[i] , succ, state[1])) #save visited states for later reversal
		
		return succs

def astar_search(problem):

	global a
	a = problem
	actions_record = [] #record of actions taken to reach goal
	state = (a.h(a.initial), a.initial, 0)
	visited = [] #visited states
	
	leaves = PriorityQueue() #priority queue for opened leaves of the tree
	leaves.put((a.h(state[1]), [state[1], None, state[2]])) #initialize priority queue with original heuristic, [initial puzzle state, None, depth = 0]
	state_list = leaves.get()
	
	state = (state_list[0], state_list[1][0], state_list[1][1] , state_list[1][2]) #state_list[0] = heur. state_list[1][0] = puzzle state, state_list[1][1] = move, state_list[1][2] = depth
	
	if a.goal_test(state[1]):
		
		return None

	check = False

	while check == False:
		
		if a.goal_test(state[1]): #end while loop if h = 0
			
			check = True
			break
		
		if state[1] not in visited: #never check a visited node, ie graph search instead of tree
			
			visited.append(state[1])
			front = succ(state)
			
			while front.empty() == False:
				
				child = front.get() #select child from front
				
				leaves.put(child) #add child to queue
				
		if leaves.empty(): #returns none if solution does not exist, ie priority queue becomes empty
			
			return None
			
		state_list = leaves.get()

		state = (state_list[0], state_list[1][0], state_list[1][1] , state_list[1][2])

	successors = [parent_vals[i][2] for i in range(len(parent_vals))] #successors of parents
	revstate = parent_vals[successors.index(state[1])] #set new reverse state for backtracking through steps
	
	while revstate[2] != a.initial: #run reversal of steps loop until we reach initial state
		
		b = successors.index(revstate[3])
		actions_record.append(revstate[1])
		revstate = parent_vals[b]
		
	actions_record.reverse() #reverse the list to output proper steps

	return actions_record
