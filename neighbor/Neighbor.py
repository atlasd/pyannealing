import pandas  as pd
import numpy as np
from numpy.random import randint

class Neighbor:
    def __init__(self, states, n_states):
        '''
        This class is used for generating neighbors of
        a given state. It will randomly change integers in a state
        vector.

        Parameters
        -----------
        states : int
            The number of valid states

        n_states : int
            The number of elements in the
            state space vector (equal to the
            dimensionality of the range of
            the function to be optimized)
        '''
        self.states = states
        self.n_states = n_states

    def get_changes(self, n_changes):
        new_places = randint(low=0, high=self.n_states, size=n_changes)
        new_states = randint(low=0, high=self.states, size=n_changes)
        return new_places, new_states

    def get_neighbor(self, theta, new_places, new_states):
        '''
        Function to get a neighbor from a theta

        Parameters
        ---------
        theta : np.ndarray
            A numpy array of integers describing the state

        new_places : np.ndarray
            An array of locations for which to swap values

        new_states : np.ndarray
            An array of new values to swap out

        Output:
        --------
        Returns a neighboring state
        '''
        # Check for correctness
        assert isinstance(theta, np.ndarray)
        assert np.all([x < self.states for x in theta]), "Invalid theta"

        # Copy the array, replace the elements, and return it
        new_theta = np.copy(theta)
        new_theta.put(new_places, new_states)
        return new_theta

    def neighbor(self, x, n_changes=1):
        '''
        This function generates the neighbors of a
        state, based on the initialization parameters.

        Parameters:
        -----------
        x : np.ndarray
            An array describing the state

        n_changes : int
            The number of elements in the state to change

        '''
        assert isinstance(x, np.ndarray)
        assert np.all([elem < self.states for elem in x]), "Invalid x"
        newplaces, newstates = self.get_changes(n_changes)
        return self.get_neighbor(x, newplaces, newstates)
