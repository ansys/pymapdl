# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import math
import random
from typing import Callable, Tuple

import numpy as np


def find_solution(
    func: Callable[[float], float],
    derivative_func: Callable[[float], float],
    acceptable_solution_error: float,
    solution_range: Tuple[float, float],
) -> float:
    """Find the solution of g(x) = 0 within a solution range where g(x) is non-linear.

    Parameters
    ----------
    func : Callable[float, float]
        Definition of the function.
    derivative_func : Callable[float, float]
        Derivative of the preceding function.
    acceptable_solution_error : float
        Error the solution is acceptable at.
    solution_range : Tuple[float, float]
        Range for searching for the solution.

    Returns
    -------
    float
        Solution to g(x) = 0.
    """

    current_guess = random.uniform(*solution_range)
    iteration_counter = 1

    while True:
        if iteration_counter > 100:
            iteration_counter = 1
            current_guess = random.uniform(*solution_range)
            continue

        updated_guess = current_guess - func(current_guess) / derivative_func(
            current_guess
        )
        error = abs(updated_guess - current_guess)

        if error < acceptable_solution_error and not (
            solution_range[0] < updated_guess < solution_range[1]
        ):
            current_guess = random.uniform(*solution_range)
            continue
        elif error < acceptable_solution_error and (
            solution_range[0] < updated_guess < solution_range[1]
        ):
            return updated_guess

        current_guess = updated_guess
        iteration_counter += 1


def evaluate_KL_cosine_terms(
    domain: Tuple[float, float], correl_length_param: float, min_eigen_value: float
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Build array of eigenvalues and constants of the cosine terms in the KL expansion of a Gaussian stochastic process.

    Parameters
    ----------
    domain : Tuple[float, float]
        Domain for finding the KL representation of the stochastic process.
    correl_length_param : float
        Correlation length parameter of the autocorrelation function of the process.
    min_eigen_value : float
        Minimum eigenvalue to achieve required accuracy.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        Arrays of frequencies, eigenvalues, and constants of the retained cosine terms (P in total) in the KL expansion.
    """

    A = (domain[1] - domain[0]) / 2  # Symmetric domain parameter -> [-A, A]

    frequency_array = []
    cosine_eigen_values_array = []
    cosine_constants_array = []

    # Define the functions related to the sine terms
    def func(w_n):
        return 1 / correl_length_param - w_n * math.tan(w_n * A)

    def deriv_func(w_n):
        return -w_n * A / math.cos(w_n * correl_length_param) ** 2 - math.tan(w_n * A)

    def eigen_value(w_n):
        return (2 * correl_length_param) / (1 + (correl_length_param * w_n) ** 2)

    def cosine_constant(w_n):
        return 1 / (A + (math.sin(2 * w_n * A) / (2 * w_n))) ** 0.5

    # Build the array of eigenvalues and constant terms for the accuracy required
    for n in range(1, 100):
        # start solving here
        acceptable_solution_error = 1e-10
        solution_range = [(n - 1) * math.pi / A, (n - 0.5) * math.pi / A]
        solution = find_solution(
            func, deriv_func, acceptable_solution_error, solution_range
        )

        frequency_array.append(solution)
        cosine_eigen_values_array.append(eigen_value(solution))
        cosine_constants_array.append(cosine_constant(solution))
        if eigen_value(solution) < min_eigen_value:
            break

    return (
        np.array(frequency_array),
        np.array(cosine_eigen_values_array),
        np.array(cosine_constants_array),
    )


def evaluate_KL_sine_terms(
    domain: Tuple[float, float], correl_length_param: float, min_eigen_value: float
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Build an array of eigenvalues and constants of the sine terms in the KL expansion of a gaussian stochastic process.

    Parameters
    ----------
    domain : Tuple[float, float]
        Domain for finding the KL representation of the stochastic process.
    correl_length_param : float
        Correlation length parameter of the autocorrelation function of the process.
    min_eigen_value : float
        Minimum eigenvalue to achieve required accuracy.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        Arrays of frequencies, eigenvalues, and constants of the retained sine terms (Q in total) in the KL expansion.
    """

    A = (domain[1] - domain[0]) / 2  # Symmetric domain parameter -> [-A, A]

    frequency_array = []
    sine_eigen_values_array = []
    sine_constants_array = []

    # Define functions related to the sine terms
    def func(w_n):
        return (1 / correl_length_param) * math.tan(w_n * A) + w_n

    def deriv_func(w_n):
        return A / (correl_length_param * math.cos(w_n * A) ** 2) + 1

    def eigen_value(w_n):
        return (2 * correl_length_param) / (1 + (correl_length_param * w_n) ** 2)

    def sine_constant(w_n):
        return 1 / (A - (math.sin(2 * w_n * A) / (2 * w_n))) ** 0.5

    # Build the array of eigenvalues and constant terms for the accuracy required
    for n in range(1, 100):
        # start solving here
        acceptable_solution_error = 1e-10
        solution_range = [(n - 0.5) * math.pi / A, n * math.pi / A]
        solution = find_solution(
            func, deriv_func, acceptable_solution_error, solution_range
        )

        frequency_array.append(solution)
        sine_eigen_values_array.append(eigen_value(solution))
        sine_constants_array.append(sine_constant(solution))
        if eigen_value(solution) < min_eigen_value:
            break

    return (
        np.array(frequency_array),
        np.array(sine_eigen_values_array),
        np.array(sine_constants_array),
    )


def stochastic_field_realization(
    cosine_frequency_array: np.ndarray,
    cosine_eigen_values: np.ndarray,
    cosine_constants: np.ndarray,
    cosine_random_variables_set: np.ndarray,
    sine_frequency_array: np.ndarray,
    sine_eigen_values: np.ndarray,
    sine_constants: np.ndarray,
    sine_random_variables_set: np.ndarray,
    domain: Tuple[float, float],
    evaluation_point: float,
) -> float:
    """Realization of the Gaussian field f(x).

    Parameters
    ----------
    cosine_frequency_array : np.ndarray
        Array of length P, containing the frequencies associated with the retained cosine terms.
    cosine_eigen_values : np.ndarray
        Array of length P, containing the eigenvalues associated with the retained cosine terms.
    cosine_constants : np.ndarray
        Array of length P, containing constants associated with the retained cosine terms.
    cosine_random_variables_set : np.ndarray
        Array of length P, containing the random variables drawn from N(0,1) for the cosine terms.
    sine_frequency_array : np.ndarray
        Array of length Q, containing the frequencies associated with the retained sine terms.
    sine_eigen_values : np.ndarray
        Array of length Q, containing eigenvalues associated with retained sine terms.
    sine_constants : np.ndarray
         Array of length Q, containing the constants associated with the retained sine terms.
    sine_random_variables_set : np.ndarray
         Array of length P, containing the random variable drawn from N(0,1) for the sine terms.
    domain : Tuple[float, float]
        Domain for finding the KL representation of the stochastic process.
    evaluation_point : float
        Point within the domain at which the value of a realization is required.

    Returns
    -------
    float
        Value of the realization at a given point within the domain.
    """
    # Shift parameter -> Because terms are solved in a symmetric domain [-A, A]
    T = (domain[0] + domain[1]) / 2

    # Using the array operation provided by the numpy package is much simpler for expressing the stochastic process
    cosine_function_terms = (
        np.sqrt(cosine_eigen_values)
        * cosine_constants
        * np.cos((evaluation_point - T) * cosine_frequency_array)
        * cosine_random_variables_set
    )

    sine_function_terms = (
        np.sqrt(sine_eigen_values)
        * sine_constants
        * np.sin((evaluation_point - T) * sine_frequency_array)
        * sine_random_variables_set
    )

    return np.sum(cosine_function_terms) + np.sum(sine_function_terms)


def young_modulus_realization(
    cosine_frequency_list,
    cosine_eigen_values,
    cosine_constants,
    cosine_random_variables_set,
    sine_frequency_list,
    sine_eigen_values,
    sine_constants,
    sine_random_variables_set,
    domain,
    evaluation_point,
):
    return 1e5 * (
        1
        + 0.1
        * stochastic_field_realization(
            cosine_frequency_list,
            cosine_eigen_values,
            cosine_constants,
            cosine_random_variables_set,
            sine_frequency_list,
            sine_eigen_values,
            sine_constants,
            sine_random_variables_set,
            domain,
            evaluation_point,
        )
    )


# Generate K-L expansion parameters
import matplotlib.pyplot as plt

domain = (0, 4)
correl_length_param = 3
min_eigen_value = 0.001

cosine_frequency_array, cosine_eigen_values, cosine_constants = (
    evaluate_KL_cosine_terms(domain, correl_length_param, min_eigen_value)
)
sine_frequency_array, sine_eigen_values, sine_constants = evaluate_KL_sine_terms(
    domain, correl_length_param, min_eigen_value
)

# See what the realizations looks like
no_of_realizations = 10
x = np.linspace(domain[0], domain[1], 101)

fig, ax = plt.subplots()
ax.set_xlabel(r"$x \: (m)$")
ax.set_ylabel(r"Realizations of $E$")
ax.grid(True)
fig.set_size_inches(15, 8)
ax.set_xlim(domain[0], domain[1])

for i in range(no_of_realizations):
    cosine_random_variables_set = np.random.normal(
        0, 1, size=len(cosine_frequency_array)
    )
    sine_random_variables_set = np.random.normal(0, 1, size=len(sine_frequency_array))

    realization = np.array(
        [
            young_modulus_realization(
                cosine_frequency_array,
                cosine_eigen_values,
                cosine_constants,
                cosine_random_variables_set,
                sine_frequency_array,
                sine_eigen_values,
                sine_constants,
                sine_random_variables_set,
                domain,
                evaluation_point,
            )
            for evaluation_point in x
        ]
    )
    ax.plot(x, realization)

plt.show()

# Verify that the previous implementation represents the Young's modulus
no_of_realizations = 5000
x = np.linspace(domain[0], domain[1], 101)
realization_collection = np.zeros((no_of_realizations, len(x)))

for i in range(no_of_realizations):
    cosine_random_variables_set = np.random.normal(
        0, 1, size=len(cosine_frequency_array)
    )
    sine_random_variables_set = np.random.normal(0, 1, size=len(sine_frequency_array))

    realization = np.array(
        [
            young_modulus_realization(
                cosine_frequency_array,
                cosine_eigen_values,
                cosine_constants,
                cosine_random_variables_set,
                sine_frequency_array,
                sine_eigen_values,
                sine_constants,
                sine_random_variables_set,
                domain,
                evaluation_point,
            )
            for evaluation_point in x
        ]
    )

    realization_collection[i:] = realization

ensemble_mean_with_realization = np.zeros(realization_collection.shape[0])
ensemble_var_with_realization = np.zeros(realization_collection.shape[0])
for i in range(realization_collection.shape[0]):
    ensemble_mean_with_realization[i] = np.mean(realization_collection[: i + 1, :])
    ensemble_var_with_realization[i] = np.var(realization_collection[: i + 1, :])

# Plot the ensemble mean
fig, ax = plt.subplots()
fig.set_size_inches(15, 8)
ax.plot(ensemble_mean_with_realization, label="Computed mean")
ax.axhline(y=1e5, color="r", linestyle="dashed", label="Actual mean")
plt.xlabel("No of realizations")
plt.ylabel(r"Ensemble mean of $E$")
ax.grid(True)
ax.set_xlim(0, no_of_realizations)
ax.legend()
plt.show()

# Plot of ensemble variance
fig, ax = plt.subplots()
fig.set_size_inches(15, 8)
ax.plot(ensemble_var_with_realization, label="Computed variance")
ax.axhline(y=1e8, color="r", linestyle="dashed", label="Actual variance")
plt.xlabel("No of realizations")
plt.ylabel(r"Ensemble varianc of $E$")
ax.grid(True)
ax.set_xlim(0, no_of_realizations)
ax.legend()
plt.show()

# .................................... PyMAPDL part starts here ........................................


# Single-threaded approach
# Function for running the simulations
def run_simulations(
    length: float,
    height: float,
    thickness: float,
    mesh_size: float,
    no_of_simulations: int,
) -> np.ndarray:
    """Run desired number of simulations to obtain response data.

    Parameters
    ----------
    length : float
        Length of the cantilever structure.
    height : float
        Height of the cantilever structure.
    thickness : float
        Thickness of the cantilever structure.
    mesh_size : float
        Desired mesh size.
    no_of_simulations : int
       Number of simulations to run.

    Returns
    -------
    np.ndarray
        Array containing simulation results.
    """

    from pathlib import Path

    from ansys.mapdl.core import launch_mapdl

    path = Path.cwd()
    mapdl = launch_mapdl(run_location=path)

    domain = [0, length]
    correl_length_param = 3
    min_eigen_value = 0.001
    poisson_ratio = 0.3

    mapdl.prep7()  # Enter preprocessor

    mapdl.r(r1=thickness)
    mapdl.et(1, "PLANE182", kop3=3, kop6=0)
    mapdl.rectng(0, length, 0, height)
    mapdl.mshkey(1)
    mapdl.mshape(0, "2D")
    mapdl.esize(mesh_size)
    mapdl.amesh("ALL")

    # Fixed edge
    mapdl.nsel("S", "LOC", "X", 0)
    mapdl.cm("FIXED_END", "NODE")

    # Load application node
    mapdl.nsel("S", "LOC", "X", length)
    mapdl.nsel("R", "LOC", "Y", height)
    mapdl.cm("LOAD_APPLICATION_POINT", "NODE")

    mapdl.finish()  # Exit preprocessor

    mapdl.slashsolu()  # Enter solution processor

    element_ids = mapdl.esel(
        "S", "CENT", "Y", 0, mesh_size
    )  # Select bottom row elements and store the ids

    # Generate quantities required to define the Young's modulus stochastic process
    cosine_frequency_list, cosine_eigen_values, cosine_constants = (
        evaluate_KL_cosine_terms(domain, correl_length_param, min_eigen_value)
    )
    sine_frequency_list, sine_eigen_values, sine_constants = evaluate_KL_sine_terms(
        domain, correl_length_param, min_eigen_value
    )

    simulation_results = np.zeros(no_of_simulations)

    for simulation in range(no_of_simulations):
        # Generate random variables and load needed for one realization of the process
        cosine_random_variables_set = np.random.normal(
            0, 1, size=len(cosine_frequency_list)
        )
        sine_random_variables_set = np.random.normal(
            0, 1, size=len(sine_frequency_list)
        )
        load = -np.random.normal(10, 2**0.5)  # Generate a random load

        material_property = 0  # Initialize material property ID
        for element_id in element_ids:
            material_property += 1
            mapdl.get("ELEMENT_ID", "ELEM", element_id, "CENT", "X")
            element_centroid_x_coord = mapdl.parameters["ELEMENT_ID"]
            mapdl.esel(
                "S", "CENT", "X", element_centroid_x_coord
            )  # Select all elements having this coordinate as centroid

            # Evaluate Young's modulus at this material point
            young_modulus_value = young_modulus_realization(
                cosine_frequency_list,
                cosine_eigen_values,
                cosine_constants,
                cosine_random_variables_set,
                sine_frequency_list,
                sine_eigen_values,
                sine_constants,
                sine_random_variables_set,
                domain,
                element_centroid_x_coord,
            )

            mapdl.mp(
                "EX", f"{material_property}", young_modulus_value
            )  # Define property ID and assign Young's modulus
            mapdl.mp(
                "NUXY", f"{material_property}", poisson_ratio
            )  # Assign poisson ratio
            mapdl.mpchg(
                material_property, "ALL"
            )  # Assign property to selected elements

        mapdl.allsel()

        mapdl.d("FIXED_END", lab="UX", value=0, lab2="UY")  # Apply fixed end BC
        mapdl.f("LOAD_APPLICATION_POINT", lab="FY", value=load)  # Apply load BC
        mapdl.solve()

        # Displacement probe point - where Uy results are to be extracted
        displacement_probe_point = mapdl.queries.node(length, 0, 0)
        displacement = mapdl.get_value("NODE", displacement_probe_point, "U", "Y")

        simulation_results[simulation] = displacement

        mapdl.mpdele("ALL", "ALL")
        if (simulation + 1) % 10 == 0:
            print(f"Completed {simulation + 1} simulations.")

    mapdl.exit()
    print()
    print("All simulations completed.")

    return simulation_results


# Run the simulations
import time

start = time.time()
simulation_results = run_simulations(4, 1, 0.2, 0.1, 5000)
end = time.time()
print(
    "Simulation took {} min {} s".format(
        int((end - start) // 60), int((end - start) % 60)
    )
)

# Perform statistical postprocessing and plot the PDF
import scipy.stats as stats

kde = stats.gaussian_kde(simulation_results)  # Kernel density estimate

fig, ax = plt.subplots()
fig.set_size_inches(15, 8)
x_eval = np.linspace(min(simulation_results), max(simulation_results), num=200)
ax.plot(x_eval, kde.pdf(x_eval), "r-", label="PDF of response $u$")
plt.xlabel("Displacement in (m)")
ax.legend()
plt.show()

# Proceed to evaluate the probability that the response u is less than 0.2 m
probability = kde.integrate_box_1d(-0.2, x_eval[-1])
print(f"The probability that u is less than 0.2 m is {probability:.0%}.")


# Multi-threaded approach
# Note that the number of instances should not be more than the number of available CPU cores on your PC
def run_simulations_threaded(
    mapdl, length, height, thickness, mesh_size, no_of_simulations, instance_identifier
):
    domain = [0, length]
    correl_length_param = 3
    min_eigen_value = 0.001
    poisson_ratio = 0.3

    mapdl.prep7()  # Enter preprocessor

    mapdl.r(r1=thickness)
    mapdl.et(1, "PLANE182", kop3=3, kop6=0)
    mapdl.rectng(0, length, 0, height)
    mapdl.mshkey(1)
    mapdl.mshape(0, "2D")
    mapdl.esize(mesh_size)
    mapdl.amesh("ALL")

    # Defined fixed edge
    mapdl.nsel("S", "LOC", "X", 0)
    mapdl.cm("FIXED_END", "NODE")

    # Load application node
    mapdl.nsel("S", "LOC", "X", length)
    mapdl.nsel("R", "LOC", "Y", height)
    mapdl.cm("LOAD_APPLICATION_POINT", "NODE")

    mapdl.finish()  # Exit preprocessor

    mapdl.slashsolu()  # Enter solution processor

    element_ids = mapdl.esel(
        "S", "CENT", "Y", 0, mesh_size
    )  # Select bottom row elements and store the IDs

    # Generate quantities required to define the Young's modulus stochastic process
    cosine_frequency_list, cosine_eigen_values, cosine_constants = (
        evaluate_KL_cosine_terms(domain, correl_length_param, min_eigen_value)
    )
    sine_frequency_list, sine_eigen_values, sine_constants = evaluate_KL_sine_terms(
        domain, correl_length_param, min_eigen_value
    )

    simulation_results = np.zeros(no_of_simulations)

    for simulation in range(no_of_simulations):
        # Generate random variables and the load needed for one realization of the process
        cosine_random_variables_set = np.random.normal(
            0, 1, size=len(cosine_frequency_list)
        )
        sine_random_variables_set = np.random.normal(
            0, 1, size=len(sine_frequency_list)
        )
        load = -np.random.normal(10, 2**0.5)  # Generate a random load

        material_property = 0  # Initialize material property ID
        for element_id in element_ids:
            material_property += 1
            mapdl.get("ELEMENT_ID", "ELEM", element_id, "CENT", "X")
            element_centroid_x_coord = mapdl.parameters["ELEMENT_ID"]
            mapdl.esel(
                "S", "CENT", "X", element_centroid_x_coord
            )  # Select all elements having this coordinate as centroid

            # Evaluate Young's modulus at this material point
            young_modulus_value = young_modulus_realization(
                cosine_frequency_list,
                cosine_eigen_values,
                cosine_constants,
                cosine_random_variables_set,
                sine_frequency_list,
                sine_eigen_values,
                sine_constants,
                sine_random_variables_set,
                domain,
                element_centroid_x_coord,
            )

            mapdl.mp(
                "EX", f"{material_property}", young_modulus_value
            )  # Define property ID and assign Young's modulus
            mapdl.mp(
                "NUXY", f"{material_property}", poisson_ratio
            )  # Assign Poisson ratio
            mapdl.mpchg(
                material_property, "ALL"
            )  # Assign property to selected elements

        mapdl.allsel()

        mapdl.d("FIXED_END", lab="UX", value=0, lab2="UY")  # Apply fixed end BC
        mapdl.f("LOAD_APPLICATION_POINT", lab="FY", value=load)  # Apply load BC
        mapdl.solve()

        # Displacement probe point - where Uy results are to be extracted
        displacement_probe_point = mapdl.queries.node(length, 0, 0)
        displacement = mapdl.get_value("NODE", displacement_probe_point, "U", "Y")

        simulation_results[simulation] = displacement

        mapdl.mpdele("ALL", "ALL")
        if (simulation + 1) % 10 == 0:
            print(
                f"Completed {simulation + 1} simulations in instance {instance_identifier}."
            )

    mapdl.exit()
    print()
    print(f"All simulations completed in instance {instance_identifier}.")

    return instance_identifier, no_of_simulations, simulation_results


def run_simulations_over_multple_instances(
    length, height, thickness, mesh_size, no_of_simulations, no_of_instances
):
    from pathlib import Path

    from ansys.mapdl.core import MapdlPool

    # Determine the number of simulations to run per instance
    if no_of_simulations % no_of_instances == 0:
        # Simulations can be split equally across instances
        simulations_per_instance = no_of_simulations // no_of_instances
        simulations_per_instance_list = [
            simulations_per_instance for i in range(no_of_instances)
        ]
    else:
        # Simulations cannot be split equally across instances
        simulations_per_instance = no_of_simulations // no_of_instances
        simulations_per_instance_list = [
            simulations_per_instance for i in range(no_of_instances - 1)
        ]
        remaining_simulations = no_of_simulations - sum(simulations_per_instance_list)
        simulations_per_instance_list.append(remaining_simulations)

    path = Path.cwd()
    pool = MapdlPool(no_of_instances, nproc=1, run_location=path, start_timeout=120)

    inputs = [
        (length, height, thickness, mesh_size, simulations, id + 1)
        for id, simulations in enumerate(simulations_per_instance_list)
    ]

    overall_simulation_results = pool.map(run_simulations_threaded, inputs)
    pool.exit()

    return overall_simulation_results


# Run the simulations over several instances
start = time.time()
simulation_results = run_simulations_over_multple_instances(4, 1, 0.2, 0.1, 5000, 10)
end = time.time()
print(
    "Simulation took {} min {} s".format(
        int((end - start) // 60), int((end - start) % 60)
    )
)

# Collect the results from each instance
combined_results = [result[2] for result in simulation_results]
combined_results = np.concatenate(combined_results)

# Calculate the probability
kde = stats.gaussian_kde(combined_results)  # Kernel density estimate
probability = kde.integrate_box_1d(-0.2, max(combined_results))
print(f"The probability that u is less than 0.2 m is {probability:.0%}")
