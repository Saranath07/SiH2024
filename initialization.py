import numpy as np
from scipy.special import expit

import numpy as np

class ParameterInitializer:
    def __init__(self, initialization='random'):
        """
        Parameters:
        initialization (str): 'random' for uniform random initialization,
                              'gaussian' for Gaussian distribution,
                              'glorot' for Glorot initialization.
        """
        self.initialization = initialization

    def initialize_parameters(self, inputs, hidden_layers, outputs):
        """
        Initializes the parameters for a neural network.

        Args:
            inputs (int): The number of input nodes.
            hidden_layers (list): A list of integers representing the number of nodes in each hidden layer.
            outputs (int): The number of output nodes.

        Returns:
            dict: A dictionary containing the initialized parameters, with keys "W1" and "b1" for the first layer, and "W{i+1}" and "b{i+1}" for each hidden layer, where i is the index of the layer. The last two keys are "W{len(hidden_layers) + 1}" and "b{len(hidden_layers) + 1}" for the output layer.

        Raises:
            None.
        """
        parameters = {}

        if self.initialization == 'random':
            parameters["W1"] = np.random.rand(hidden_layers[0], inputs)
            parameters["b1"] = np.random.rand(hidden_layers[0])

        elif self.initialization == 'gaussian':
            parameters["W1"] = np.random.randn(hidden_layers[0], inputs)
            parameters["b1"] = np.random.randn(hidden_layers[0])

        elif self.initialization == 'glorot':
            parameters["W1"] = np.random.uniform(-np.sqrt(6 / (inputs + hidden_layers[0])),
                                                 np.sqrt(6 / (inputs + hidden_layers[0])),
                                                 (hidden_layers[0], inputs))
            parameters["b1"] = np.zeros(hidden_layers[0])

        for i in range(1, len(hidden_layers)):
            if self.initialization == 'random':
                parameters[f"W{i+1}"] = np.random.rand(hidden_layers[i], hidden_layers[i - 1])
                parameters[f"b{i+1}"] = np.random.rand(hidden_layers[i])
            elif self.initialization == 'gaussian':
                parameters[f"W{i+1}"] = np.random.randn(hidden_layers[i], hidden_layers[i - 1])
                parameters[f"b{i+1}"] = np.random.randn(hidden_layers[i])
            elif self.initialization == 'glorot':
                parameters[f"W{i+1}"] = np.random.uniform(-np.sqrt(6 / (hidden_layers[i - 1] + hidden_layers[i])),
                                                          np.sqrt(6 / (hidden_layers[i - 1] + hidden_layers[i])),
                                                          (hidden_layers[i], hidden_layers[i - 1]))
                parameters[f"b{i+1}"] = np.zeros(hidden_layers[i])

        if self.initialization == 'random':
            parameters[f"W{len(hidden_layers) + 1}"] = np.random.rand(outputs, hidden_layers[-1])
            parameters[f"b{len(hidden_layers) + 1}"] = np.random.rand(outputs)
        elif self.initialization == 'gaussian':
            parameters[f"W{len(hidden_layers) + 1}"] = np.random.randn(outputs, hidden_layers[-1])
            parameters[f"b{len(hidden_layers) + 1}"] = np.random.randn(outputs)
        elif self.initialization == 'glorot':
            parameters[f"W{len(hidden_layers) + 1}"] = np.random.uniform(-np.sqrt(6 / (hidden_layers[-1] + outputs)),
                                                                         np.sqrt(6 / (hidden_layers[-1] + outputs)),
                                                                         (outputs, hidden_layers[-1]))
            parameters[f"b{len(hidden_layers) + 1}"] = np.zeros(outputs)

        return parameters
