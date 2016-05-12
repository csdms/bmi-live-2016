# BMI: Live!

In this step,
we've refactored the **run_heat.py** script,
making two significant changes:

1. The heat diffusion model has been extracted from the script and
   placed into its own class, `HeatSolver`, in its own module,
   **heat.py**.
1. Likewise, the solver for the diffusion equation has been moved
   from the script into its own module, **solve_2d.py**.

We keep the **run_heat.py** script,
but it now uses an instance of the `HeatSolver` class.

Run the script with

    $ python run_heat.py

Does the refactored code produce the same result
as the initial example?
