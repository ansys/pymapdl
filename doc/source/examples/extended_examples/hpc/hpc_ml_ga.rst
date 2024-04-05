.. _hpc_ml_ga_example:

==============================
Genetic Algorithms and PyMAPDL
==============================

This example aims also to show how to use PyMAPDL in an HPC cluster, to 
take advantage of multiple MAPDL instances to calculate each of the
genetic algorithm population solution.
To manage multiple MAPDL instances, it is recommended to use the
:py:class:`~ansys.mapdl.core.pool.MapdlPool` class which allows you
to run multiple jobs on the background.

Introduction
============

Genetic algorithms are optimization techniques inspired by the principles of natural
selection and genetics. They are used to find solutions to complex problems by mimicking
the process of natural selection to evolve potential solutions over successive generations.
In a genetic algorithm, a population of candidate solutions (chromosomes) undergoes a
series of operations, including selection, crossover, and mutation, to produce new
generations of solutions. The fittest chromosomes, which best satisfy the problem
constraints and objectives, are more likely to be selected for reproduction, thus
gradually improving the overall quality of solutions over time. Genetic algorithms are
particularly useful for solving problems where traditional methods are impractical or
inefficient, such as optimization, search, and machine learning tasks. They find
applications in various fields, including engineering, economics, biology, and computer science.

Problem definition
==================

In this example, a generic algorithm is used to calculate the force
required for a double clamped beam to deform a specific amount in its
center.

The beam model is the same as :ref:`ref_mapdl_beam`.
It is made of ``BEAM188`` elements which span for 2.2 meters,
and it fully clamped at both ends.

The PyMAPDL beam model is defined in ``calculate_beam`` as follows:

.. code-block:: python

    def calculate_beam(mapdl, force):
        # Initializing
        mapdl.clear()
        mapdl.prep7()

        # Define an I-beam
        mapdl.et(1, "BEAM188")
        mapdl.keyopt(1, 4, 1)  # transverse shear stress output

        # Material properties
        mapdl.mp("EX", 1, 2e7)  # N/cm2
        mapdl.mp("PRXY", 1, 0.27)  # Poisson's ratio

        # Beam properties in centimeters
        sec_num = 1
        mapdl.sectype(sec_num, "BEAM", "I", "ISection", 3)
        mapdl.secoffset("CENT")
        mapdl.secdata(15, 15, 29, 2, 2, 1)  # dimensions are in centimeters

        # Setting FEM model
        mapdl.n(1, 0, 0, 0)
        mapdl.n(12, 110, 0, 0)
        mapdl.n(23, 220, 0, 0)
        mapdl.fill(1, 12, 10)
        mapdl.fill(12, 23, 10)

        for node in mapdl.mesh.nnum[:-1]:
            mapdl.e(node, node + 1)

        # Define the boundary conditions
        # Allow movement only in the X and Z direction
        for const in ["UX", "UY", "ROTX", "ROTZ"]:
            mapdl.d("all", const)

        # constrain just nodes 1 and 23 in the Z direction
        mapdl.d(1, "UZ")
        mapdl.d(23, "UZ")

        # apply a -Z force at node 12
        mapdl.f(12, "FZ", force[0])

        # run the static analysis
        mapdl.run("/solu")
        mapdl.antype("static")
        mapdl.solve()

        # Extracting data
        UZ = mapdl.post_processing.nodal_displacement("Z")
        UZ_node_12 = UZ[12]

        return UZ_node_12

As it can be seen, this function returns the control parameter for this model, which is the displacement at the Z-direction on the node 12 (``UZ_node_12``).


Setting MAPDL pool
==================

The genetic algorithms are expensive regarding the amount of calculation needed to reach an optimal solution. As seen before, many simulations must be performed to select, crossover, and mutate
all the chromosomes across all the populations.
For this reason, to speed up the process, it is desirable to have as many MAPDL instances as possible, so
each one can calculate one chromosome fit function.

To manage multiple MAPDL instances, the best approach is to use :py:class:`~ansys.mapdl.core.pool.MapdlPool` class.

.. code-block:: python

    from ansys.mapdl.core import MapdlPool

    # Starting pool
    # Number of instances should be equal to number of CPUs
    # as set later in the ``sbatch`` command
    pool = MapdlPool(n_instances=10)
    print(pool)


Define deflection target
========================

Because this is a demonstration example, the target displacement is calculated 
using the beam function itself using a force of 22840 :math:`N/cm^2`.

.. code-block:: python

    # Calculate target displacement
    mapdl = pool[0]
    force = 22840  # N/cm2
    target_displacement = calculate_beam(pool[0], [force])
    print(f"Setting target to {target_displacement} for force {force}")


Genetic algorithm model
=======================

Introduction
------------

The library `PyGAD <pygad_docs_>`_ is used to configure the genetic algorithm.::

    PyGAD is an open-source Python library for building the genetic algorithm and optimizing machine learning algorithms.

    PyGAD supports different types of crossover, mutation, and parent selection operators.
    PyGAD allows different types of problems to be optimized using the genetic algorithm
    by customizing the fitness function. It works with both single-objective and
    multi-objective optimization problems.


Configuration
-------------

To configure the genetic algorithm, the following code is used:

.. code-block:: python

    # Setting GA model
    sol_per_pop = 20
    num_generations = 10
    num_parents_mating = 20
    num_genes = 1  # equal to the size of inputs/outputs.
    parallel_processing = ["thread", len(pool)]  # Number of parallel workers

    # Initial guess limits
    init_range_low = 10000
    init_range_high = 30000
    gene_type = int  # limit to ints

    # Extra configuration
    # https://blog.derlin.ch/genetic-algorithms-with-pygad
    parent_selection_type = "rws"
    keep_parents = 0  # No keeping parents.
    mutation_percent_genes = 30
    mutation_probability = 0.5


From the above code, the most import parameters are:

* **sol_per_pop**: Number of solutions (chromosomes) within the population.
* **num_generations**:  Number of genes in the solution/chromosome.
  In this case, because only one parameter is the simulated (deflection Z at node 12),
  this value is 1.
* **num_parents_mating**: Number of solutions to be selected as parents.
* **parent_selection_type**: The parent selection type. In this example, the ``rws`` type
  (for roulette wheel selection) is used. For more information regarding parent selection type,
  visit `Genetic algorithms with PyGAD: selection, crossover, mutation by Lucy Linder <ga_article_>`_ article.
* **parallel_processing**: This parameter set the number of parallel workers for the genetic
  algorithm and how these workers are created. They could be created as a ``"thread"`` or ``"process"``. In our example, these workers are created as thread and their amount is equal to the number of instances.

Helper functions
----------------

Additionally, for printing purposes, several helper functions are going to be defined:

.. code-block:: python

    import numpy as np


    # To calculate the fitness criteria model solution and target displacement
    def calculate_fitness_criteria(model_output):
        # we add a constant (target/1E8) here to avoid dividing by zero
        return 1.0 / (
            1 * (np.abs(model_output - target_displacement) + target_displacement / 1e10)
        )


    # To calculate the error in the model solution with respect to the target displacement.
    def calculate_error(model_output):
        # Just for visualization purposes.
        return 100.0 * (model_output - target_displacement) / target_displacement


    # This function is executed at the end of the fitness stage (all chromosomes are calculated),
    # and it is used to do some pretty printing.
    def on_fitness(pyga_instance, solution):
        # This attribute does not exist. It will be created after the GA class has been initialized.
        pyga_instance.igen += 1
        print(f"\nGENERATION {pyga_instance.igen}")
        print("=============")


Fitness function
----------------

Now all the helper functions are defined, the fitness function can be defined:

.. code-block:: python

    def fitness_func(ga_instance, solution, solution_idx):
        # Querying a free MAPDL instance
        mapdl, i = pool.next_available(return_index=True)
        mapdl.locked = True
        mapdl._busy = True

        # Perform chromosome simulation
        model_output = calculate_beam(mapdl, solution)

        # Releasing MAPDL instance
        mapdl.locked = False
        mapdl._busy = False

        # Calculate errors and criteria
        error_ = calculate_error(model_output)
        fitness_criteria = calculate_fitness_criteria(model_output)

        # Pretty print at each chromosome solution
        # The 'port' is printed so it can be observed how the GA is using all MAPDL instances
        print(
            f"MAPDL instance {i}(port: {mapdl.port})\tInput: {solution[0]:0.1f}\tOutputs: {model_output:0.7f}\tError: {error_:0.3f}%\tFitness criteria: {fitness_criteria:0.6f}"
        )

        return fitness_criteria

PyMAPDL and PyGAD evaluate each chromosome using this function in order to
evaluate how fit is it, and assign survival probability.

Mutation function
-----------------

To further demonstrate `PyGAD <pygad_docs_>`_ capabilities, in this example a custom mutation
function is used.

This custom mutation function does two things:

* **To each chromosomes** add a random value between the maximum and minimum of the population.
* **To two random chromosomes** additionally add a random percentage of the mean across all the
  population between -10% and 10%. The random chromosomes are selected independently.
  This is to reduce the possibility of the function to converge to a local minimal.

.. code-block:: python

    def mutation_func(offspring, ga_instance):
        average = offspring.mean()
        max_value = offspring.max() - average
        min_value = offspring.min() - average

        min_value = min([min_value, max_value, -1])
        max_value = max([min_value, max_value, +1])

        offspring[:, 0] += np.random.randint(min_value, high=max_value, size=offspring.size)

        for i in range(2):
            random_spring_idx = np.random.choice(range(offspring.shape[1]))
            sign = np.random.choice([-1, 1])
            offspring[random_spring_idx, 0] += sign * average * (0.1 * np.random.random())

        return offspring


Assembling model
----------------

Finally, the GA class is used to assemble all the parameters and functions
created to run the simulation

.. code-block:: python

    ga_instance = pygad.GA(
        # Main options
        sol_per_pop=sol_per_pop,
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        num_genes=num_genes,
        fitness_func=fitness_func,
        parallel_processing=parallel_processing,
        random_seed=2,  # to get reproducible results
        #
        # Mutation
        mutation_percent_genes=mutation_percent_genes,
        mutation_type=mutation_func,
        mutation_probability=mutation_probability,
        #
        # Parents
        keep_parents=keep_parents,
        parent_selection_type=parent_selection_type,
        #
        # Helpers
        on_fitness=on_fitness,
        gene_type=gene_type,
        init_range_low=init_range_low,
        init_range_high=init_range_high,
    )

    ga_instance.igen = 0  # To count the number of generations


Run simulation
==============

Once the model is set, the simulation can be started by using ``run()`` method:

.. code-block:: python

    import time

    t0 = time.perf_counter()

    ga_instance.run()

    t1 = time.perf_counter()
    print(f"Time spent (minutes): {(t1-t0)/60}")


Plot convergence
================

.. code-block:: python

    import os

    ga_instance.plot_fitness(label=["Applied force"], save_dir=os.getcwd())

    solution, solution_fitness, solution_idx = ga_instance.best_solution(
        ga_instance.last_generation_fitness
    )

    print(f"Parameters of the best solution : {solution[0]}")
    print(f"Fitness value of the best solution = {solution_fitness}")


Storing the model result
========================

The model can be stored in a file for later reuse:

.. code-block:: python

    from datetime import datetime

    # Saving the GA instance.
    # The filename to which the instance is saved. The name is without extension.
    formatted_date = datetime.now().strftime("%d-%m-%y")
    filename = f"ml_ga_beam_{formatted_date}"
    ga_instance.save(filename=filename)

Use the following code to load the model:

.. code-block:: python

    # Loading the saved GA instance.
    loaded_ga_instance = pygad.load(filename=filename)

    # Plot fitness function again
    loaded_ga_instance.plot_fitness()


Run the simulation on an HPC cluster using SLURM
================================================

In the previous steps, the PyMAPDL script has been created.
The final file can be found in this link
:download:`ml_ga_beam.py <ml_ga_beam.py>`.

To run the above script in an HPC environment, you need to
create a Python environment, install the packages and run
the mentioned script.

1. Login into your HPC cluster.
   For more information visit :ref:`ref_hpc_login`

2. Create a virtual environment which is accessible from
   the compute nodes.

   .. code-block:: console

      user@machine:~$ python3 -m venv /home/user/.venv

   If you have problems when creating the virtual environment
   or accessing it from the compute nodes,
   visit :ref:`ref_hpc_pymapdl_job`.

3. Install the requirements for this example given in
   :download:`requirements.txt <requirements.txt>`.

4. Create the bash script ``job.sh``:

   .. code-block:: bash

      #!/bin/bash
      #SBATCH --job-name=ml_ga_beam
      #SBATCH --time=01:00:00
      #SBATCH --time=1:00:00
      #SBATCH --partition=%your_partition_name%
      #SBATCH --output=output_%j.txt
      #SBATCH --error=error_%j.txt

      # Commands to run
      echo "Running simulation..."
      source /home/user/.venv/bin/activate  # Activate venv
      python ml_ga_beam.py
      echo "Done"

   Remember to replace ``%your_partition_name%`` with your cluster
   partition.

5. Run the bash script using `sbatch <slurm_sbatch_>`_ command:

   .. code-block::
    
      sbatch --nodes=1 --ntasks-per-node=10

   The preceding command allocates 10 cores for the job.
   For optimal performance, this value should be higher than the number
   of MAPDL instances that
   :py:class:`~ansys.mapdl.core.pool.MapdlPool` is creating.