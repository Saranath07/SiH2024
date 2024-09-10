import numpy as np
from activations import Activations
from lossfunctions import LossFunctions
from initialization import ParameterInitializer

softmax = Activations.Softmax()
sigmoid = Activations.Sigmoid()
crossentropy = LossFunctions.CrossEntropyLoss()

class FeedForwardNeuralNets:
    def __init__(self, inputs, hidden_layers, outputs, g=sigmoid, L=crossentropy, O=softmax, eta=0.01,
                 optimizer="gd", initialization_method="glorot", batch_size=32,
                 beta1=0.9, beta2=0.999, epsilon=1e-8, t=0):
        self.inputs = inputs
        self.outputs = outputs
        self.batch_size = min(batch_size, inputs.shape[0])
        if len(self.outputs.shape) < 2:
            self.parameters = ParameterInitializer(initialization_method).initialize_parameters(
            inputs[0].shape[0], hidden_layers, 1)
        else:
            self.parameters = ParameterInitializer(initialization_method).initialize_parameters(
                inputs[0].shape[0], hidden_layers, outputs[0].shape[0])
        self.g = g
        self.O = O
        self.L = L
        self.eta = eta
        self.losses = {}
        self.activations = {}
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.t = t
        self.v = {key: np.zeros_like(value) for key, value in self.parameters.items()}
        self.s = {key: np.zeros_like(value) for key, value in self.parameters.items()}
        self.training_loss = []
        self.validation_loss = []


        if optimizer == "gd":
            self.optimizer = self.gradient_descent
        elif optimizer == "adam":
            self.optimizer = self.adam

    def forward_propogation(self, x):
        """
        Performs forward propagation through the neural network.

        Parameters:
            x (numpy array): The input to the neural network.

        Returns:
            y_pred (numpy array): The predicted output of the neural network.
        """

        self.activations["a1"] = self.parameters["W1"] @ x + self.parameters["b1"]
        self.activations["h1"] = self.g(self.activations["a1"])
        for i in range(2, len(self.parameters) // 2):
            self.activations[f"a{i}"] = self.parameters[f"W{i}"] @ self.activations[f"h{i - 1}"] + self.parameters[f"b{i}"]
            self.activations[f"h{i}"] = self.g(self.activations[f"a{i}"])

        self.activations[f"a{len(self.parameters) // 2}"] = self.parameters[f"W{len(self.parameters) // 2}"] @ self.activations[f"h{len(self.parameters) // 2 - 1}"] + self.parameters[f"b{len(self.parameters) // 2}"]
        y_pred = self.O(self.activations[f"a{len(self.parameters) // 2}"])
        return y_pred

    def backPropogation(self, y_pred, y, x):
        """
        Performs backpropagation through the neural network.

        Parameters:
            y_pred (numpy array): The predicted output of the neural network.
            y (numpy array): The actual output of the neural network.
            x (numpy array): The input to the neural network.

        Returns:
            None
        """
        n = len(self.parameters) // 2
        m = len(self.activations) // 2

        La = y_pred - y

        Lh = La @ self.parameters[f"W{n}"]

        da = self.g.gradient(self.activations[f"a{m}"])
        self.losses[f"W{n}"] = np.outer(La, self.activations[f"h{m}"])
        self.losses[f"b{n}"] = La.copy()

        for i in range(1, m):
            La = Lh * da
            Lh = La @ self.parameters[f"W{m - i + 1}"]
            da = self.g.gradient(self.activations[f"a{m - i}"])
            self.losses[f"W{m - i + 1}"] = np.outer(La, self.activations[f"h{m - i}"])
            self.losses[f"b{m - i + 1}"] = La.copy()

        La = Lh * da
        self.losses["W1"] = np.outer(La, x)
        self.losses["b1"] = La.copy()

        _, gradients_weights = self.L.gradient(y_pred, y, list(self.parameters.values()))

        for i, key in enumerate(self.parameters.keys()):
            if key.startswith('W'):
                self.losses[key] += gradients_weights[i]



    def gradient_descent(self):
        """
        Performs gradient descent optimization on the neural network's parameters.

        Updates the weights (W) and biases (b) of the neural network by subtracting the product of the learning rate (eta) and the corresponding losses.

        Parameters:
            None

        Returns:
            None
        """
        for i in range(len(self.parameters) // 2):
            self.parameters[f"W{i + 1}"] = self.parameters[f"W{i + 1}"] - self.eta * self.losses[f"W{i + 1}"]
            self.parameters[f"b{i + 1}"] = self.parameters[f"b{i + 1}"] - self.eta * self.losses[f"b{i + 1}"]


    def adam(self):
        """
        Performs Adam optimization on the neural network's parameters.

        Updates the weights (W) and biases (b) of the neural network using the Adam optimization algorithm.

        Parameters:
            None

        Returns:
            None
        """
        self.t += 1
        for key in self.parameters.keys():
            if key.startswith("W") or key.startswith("b"):
                gradient = self.losses[key]

                self.v[key] = self.beta1 * self.v[key] + (1 - self.beta1) * gradient
                self.s[key] = self.beta2 * self.s[key] + (1 - self.beta2) * (gradient ** 2)

                v_corrected = self.v[key] / (1 - self.beta1 ** self.t)
                s_corrected = self.s[key] / (1 - self.beta2 ** self.t)

                self.parameters[key] -= self.eta * v_corrected / (np.sqrt(s_corrected) + self.epsilon)

    def train(self, epochs, validation_data=None):
        """
        Trains the neural network model for a specified number of epochs.

        This function takes in the number of epochs as input and performs the following operations:
            - Shuffles the input data and corresponding outputs.
            - Divides the shuffled data into batches based on the batch size.
            - For each batch, it calculates the total gradient loss by iterating over each input and output pair.
            - It then updates the model parameters using the optimizer function.
            - If validation data is provided, calculates and appends the validation loss every 200 iterations.

        Parameters:
            epochs (int): The number of epochs to train the model for.
            validation_data (tuple): A tuple containing validation inputs and outputs.

        Returns:
            None
        """
        for epoch in range(epochs):
            permutation = np.random.permutation(self.inputs.shape[0])
            inputs_shuffled = self.inputs[permutation]
            outputs_shuffled = self.outputs[permutation]

            total_loss = 0

            for i in range(0, self.inputs.shape[0], self.batch_size):
                batch_inputs = inputs_shuffled[i:i + self.batch_size]
                batch_outputs = outputs_shuffled[i:i + self.batch_size]

                total_gradient_loss = {key: 0 for key in self.parameters.keys()}
                batch_loss = 0

                for x, y in zip(batch_inputs, batch_outputs):
                    y_pred = self.forward_propogation(x)
                    batch_loss += self.L(y_pred, y, list(self.parameters.values()))
                    self.backPropogation(y_pred, y, x)

                    for key in total_gradient_loss:
                        total_gradient_loss[key] += self.losses.get(key, 0)

                for key in total_gradient_loss:
                    total_gradient_loss[key] /= self.batch_size

                self.optimizer()

                total_loss += batch_loss / self.batch_size


                if (i // self.batch_size) % 200 == 0:
                    iteration_loss = batch_loss / self.batch_size
                    self.training_loss.append(iteration_loss)

                    if validation_data is not None:
                        val_inputs, val_outputs = validation_data
                        val_loss = 0
                        for x_val, y_val in zip(val_inputs, val_outputs):
                            y_pred_val = self.forward_propogation(x_val)
                            val_loss += self.L(y_pred_val, y_val, list(self.parameters.values()))
                        val_loss /= val_inputs.shape[0]
                        self.validation_loss.append(val_loss)

            epoch_loss = total_loss / (self.inputs.shape[0] // self.batch_size)
            if validation_data is not None:
                val_loss = self.validation_loss[-1] if self.validation_loss else None
                print(f'Epoch {epoch + 1}/{epochs}, Training Loss: {epoch_loss:.4f}, Validation Loss: {val_loss:.4f}')
            else:
                print(f'Epoch {epoch + 1}/{epochs}, Training Loss: {epoch_loss:.4f}')


    def evaluate(self, X):
        """
        Evaluates the neural network model for the given input X.

        Parameters:
            X (numpy array): The input to the neural network.

        Returns:
            numpy array: The predicted output of the neural network.
        """
        return np.array(self.forward_propogation(X))

    def predict(self, X):
        """
        Uses evaluate function and get arg max and get the prediction

        Parameters:
            X (numpy array): The input to the neural network

        Returns:
            Class label: The label that has the highest probabiltiy
        """
        return np.argmax(self.evaluate(X))
