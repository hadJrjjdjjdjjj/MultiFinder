import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image


def newton_raphson(f, df, x0, tol=1e-6, max_iter=1000):
    """
    Newton-Raphson method for finding roots of the equation f(x) = 0.

    Parameters:
    f: The function for which we are finding the root
    df: The derivative of the function f
    x0: Initial guess for the root
    tol: Tolerance for the root value
    max_iter: Maximum number of iterations

    Returns:
    x: The estimated root of the function
    iter_values: List of values of x during iteration
    """
    x = x0
    iter_values = [x0]
    for _ in range(max_iter):
        fx = f(x)
        dfx = df(x)
        if abs(dfx) < tol:
            raise ValueError("Derivative near zero; no convergence.")
        x_new = x - fx / dfx
        iter_values.append(x_new)
        if abs(x_new - x) < tol:
            return x_new, iter_values
        x = x_new
    raise ValueError("Maximum iterations exceeded; no convergence.")


def solve_and_visualize(expr, initial_guesses, filename='pic.png'):
    """
    Solve an equation using Newton-Raphson method for multiple initial guesses and visualize the process.

    Parameters:
    expr: The equation to solve (sympy expression)
    initial_guesses: List of initial guesses for the root
    """
    # Define the function and its derivative
    x = sp.symbols('x')
    f = sp.lambdify(x, expr, 'numpy')
    df = sp.lambdify(x, sp.diff(expr, x), 'numpy')

    plt.figure(figsize=(12, 8))

    for i, x0 in enumerate(initial_guesses):
        try:
            root, iter_values = newton_raphson(f, df, x0)
            print(f"Initial guess {x0}: Converged to root {root}")

            # Prepare data for plotting
            iter_steps = list(range(len(iter_values)))

            # Plot the iteration process
            plt.plot(iter_steps, iter_values, marker='o', linestyle='dashed',
                     label=f'Initial guess {x0}, root {root:.6f}')
        except ValueError as e:
            print(f"Initial guess {x0}: {e}")

    plt.xlabel('Iteration step')
    plt.ylabel('Root value')
    plt.title('Newton-Raphson Iteration for Multiple Initial Guesses')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    image = Image.open(filename)
    image.show()
    plt.show()


# Example usage:
# Define the equation to solve, e.g., sin(x) - 0.5 = 0
x = sp.symbols('x')
equation = x**8 - 32  # Roots are around x = π/6, 5π/6, ...

initial_guesses = np.linspace(-20, 20, 10)
# initial_guesses = [-3.0, -4.0, 2.0, 4.0, 7.0]  # Multiple initial guesses
solve_and_visualize(equation, initial_guesses)
