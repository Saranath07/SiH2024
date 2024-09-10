import numpy as np

class LossFunctions:

    class SquaredErrorLoss:
        def __init__(self, alpha=0.01, regularization='l2'):
            """
            Initializes the SquaredErrorLoss with optional L1 or L2 regularization.

            Parameters:
            alpha (float): Regularization constant.
            regularization (str): Type of regularization ('l1' for L1, 'l2' for L2, or None).
            """
            self.alpha = alpha
            self.regularization = regularization

        def __call__(self, y_pred, y_true, model_weights=None):
            """
            Computes the Mean Squared Error (MSE) with optional L1 or L2 regularization.

            Parameters:
            y_pred (ndarray): The predicted values.
            y_true (ndarray): The true values.
            model_weights (list): A list of model weights (e.g., numpy arrays).

            Returns:
            float: The regularized mean squared error.
            """
            mse_loss = 0.5 * np.mean((y_pred - y_true) ** 2)

            # Regularization term
            if self.regularization == 'l2':
                reg_term = self.alpha * sum(np.sum(w ** 2) for w in model_weights)
            elif self.regularization == 'l1':
                reg_term = self.alpha * sum(np.sum(np.abs(w)) for w in model_weights)
            else:
                reg_term = 0  # No regularization

            return mse_loss + reg_term

        def gradient(self, y_pred, y_true, model_weights=None):
            """
            Computes the gradient of the Mean Squared Error (MSE) Loss with respect to y_pred,
            including the gradient of the regularization term.

            Parameters:
            y_pred (ndarray): The predicted values.
            y_true (ndarray): The true values.
            model_weights (list): A list of model weights (e.g., numpy arrays).

            Returns:
            tuple: The gradient with respect to y_pred and the gradients with respect to the model weights.
            """
            gradient_y_pred = 2 * (y_pred - y_true)


            gradients_weights = []
            if model_weights is not None:
                for w in model_weights:
                    if self.regularization == 'l2':
                        grad_w = self.alpha * w
                    elif self.regularization == 'l1':
                        grad_w = self.alpha * np.sign(w)
                    else:
                        grad_w = np.zeros_like(w)
                    gradients_weights.append(grad_w)

            return gradient_y_pred, gradients_weights

        def __repr__(self):
            return f"SquaredErrorLoss(alpha={self.alpha}, regularization={self.regularization})"



    class CrossEntropyLoss:
        def __init__(self, alpha=0.01, regularization=None):
            self.alpha = alpha
            self.regularization = regularization

        def __call__(self, y_pred, y_true, model_weights):

            y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
            ce_loss = -np.sum(y_true * np.log(y_pred))


            if self.regularization == 'l2':
                reg_term = self.alpha * sum(np.sum(w ** 2) for w in model_weights)
            elif self.regularization == 'l1':
                reg_term = self.alpha * sum(np.sum(np.abs(w)) for w in model_weights)
            else:
                reg_term = 0

            return ce_loss + reg_term

        def gradient(self, y_pred, y_true, model_weights):
            """
            Compute the gradient of the Cross-Entropy Loss with respect to y_pred,
            including the gradient of the regularization term.

            Parameters:
            y_pred (ndarray): The predicted probabilities (output of softmax) of shape (num_classes,).
            y_true (ndarray): The one-hot encoded true labels of shape (num_classes,).
            model_weights (list): A list of model weights (e.g., numpy arrays).

            Returns:
            list: A list containing the gradient with respect to y_pred and the gradients
                  with respect to the model weights.
            """

            y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
            gradient_y_pred = -(y_true / y_pred)


            gradients_weights = []
            for w in model_weights:
                if self.regularization == 'l2':
                    grad_w = self.alpha * w
                elif self.regularization == 'l1':
                    grad_w = self.alpha * np.sign(w)
                else:
                    grad_w = np.zeros_like(w)
                gradients_weights.append(grad_w)


            return gradient_y_pred, gradients_weights


        def __repr__(self):
            return f"CrossEntropyLoss(alpha={self.alpha}, regularization={self.regularization})"
