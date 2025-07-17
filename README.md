# Auto Drive
This is a command-line simulation system for autonomous cars, built as part of **Xing Yuan's hiring task**. 
It models a grid-based environment where multiple cars can be added, each receiving a unique command string to move and
rotate.


## Problem Overview
The task is to simulate the behavior of multiple autonomous driving cars on a 2D rectangular field.  
The simulation must:

- Allow users to define a field of any size
- Add one or more uniquely named cars
- Accept command strings per car using:
  - `F`: Move forward
  - `L`: Turn left 90°
  - `R`: Turn right 90°
- Handle field boundary constraints (commands moving out-of-bounds are ignored)
- Process cars' commands concurrently, one step at a time
- Detect and report car-to-car collisions (same cell, same step)
- Provide a clean CLI experience



## Assumption
- A car cannot be placed outside the field or at an occupied position
- If two or more cars collide during a step, they are "frozen" and stop executing further commands
- Other cars that are not collided will continue the simulation
- Collision only counted at the end of the step.
- This also means there is a possibility that are side-by-side can "pass through" each other, achieving a swapping of position.
- Command sequences may be of different lengths; shorter sequences complete earlier while others continue



## Project Structure
The project is organized into two main folders:

- app/: contains the core application logic
- tests/: contains all unit and integration test cases

The application entry point is main.py, which invokes the SimulationCLI class. Based on user input, the Field, Car, and Simulation components are instantiated accordingly. Once setup is complete, the simulation executes the defined commands and displays the resulting states or collisions to the user through the CLI interface.



## Installation \& Usage
###  Python Version
Build with Python **3.11+**
###  Dependencies
Only non-standard dependency is:
  - `pytest==8.4.1` 
  - `pytest-cov==6.2.1`
### Running the Application
From the root directory:
```bash
python -m app.main
```
Or install the project and run via CLI:
```bash
pip install -e .
auto-drive
```


## Testing
Code coverage is reported at 95%, with the remaining 5% corresponding to the main.py launcher and intentional early-exit branches (e.g., menu option [0] Exit) which are not meaningful to test.

All tests are written using pytest. To run them at project root folder:
```bash
pytest --cov=app tests/
```
Tests cover:
- Car turning, moving, and boundaries
- Field bounds checking
- Simulation step logic and collision detection
- End-to-end CLI simulation (via mocked input)
- Invalid entry for CLI
---