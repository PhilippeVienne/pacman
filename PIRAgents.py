import random

from game import Directions
from game import Agent
from game import Actions
from pacman import GameState


class RandomAgent(Agent):

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        direction = random.choice([Directions.WEST,Directions.EAST,Directions.SOUTH,Directions.NORTH])
        while direction not in state.getLegalPacmanActions():
            direction = random.choice([Directions.WEST,Directions.EAST,Directions.SOUTH,Directions.NORTH])
        return direction


class RandomHeuristicAgent(Agent):

    def __init__(self):
        self.map = []
        pass

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        :type state: GameState
        """
        self.map = state.getWalls()
        self.map_height = self.map.height
        self.map_width = self.map.width
        self.food_heuristic = [[state.hasFood(j,i) for j in range(0, self.map_width)] for i in range(0, self.map_height)]
        self.ghost_heuristic = [[0 for j in range(0, self.map_width)] for i in range(0, self.map_height)]

    def compute_ghost_heuristic(self, state):
        """

        :type state: GameState
        """
        self.ghost_heuristic = [[0 for j in range(0, self.map_width)] for i in range(0, self.map_height)]
        for ghost_index in range(1,state.getNumAgents()):
            position = state.getGhostPosition(ghost_index)
            position = (int(position[0]), int(position[1]))
            ghost_state = state.getGhostState(ghost_index)
            heuristic_val = 1
            self.ghost_heuristic[int(position[1])][int(position[0])] += heuristic_val
            for x in range(position[0]-1, position[0]+1):
                for y in range(position[1]-1, position[1]+1):
                    self.ghost_heuristic[y][x] += heuristic_val
            for x in range(position[0]-2, position[0]+2):
                for y in range(position[1]-2, position[1]+2):
                    self.ghost_heuristic[y][x] += heuristic_val


    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        self.compute_ghost_heuristic(state)
        self.food_heuristic = [[int(state.hasFood(j,i)) for j in range(0, self.map_width)] for i in range(0, self.map_height)]
        self.heuristic = [[-5 * self.food_heuristic[y][x] + 5*self.ghost_heuristic[y][x] for x in range(0, self.map_width)] for y in range(0, self.map_height)]

        best = 999999999
        best_choice = Directions.STOP
        for move in self.getPossibleActions(state):
            coordinates = [state.getPacmanPosition(), Actions.directionToVector(move)]
            final = [sum([int(z) for z in x]) for x in zip(*coordinates)]
            if self.heuristic[final[1]][final[0]] < best:
                best = self.heuristic[final[1]][final[0]]
                best_choice = move
            elif self.heuristic[final[1]][final[0]] == best and random.randint(1,3) == 2:
                best_choice = move
        return best_choice

    def getPossibleActions(self, state):
        actions = state.getLegalPacmanActions()
        actions.remove(Directions.STOP)
        return actions

    def not_acceptable(self, choice, state):
        """

        :type state: GameState
        """
        final = state.getPacmanPosition() + Actions.directionToVector(choice)
        return self.heuristic[final[1]][final[0]] > 10
