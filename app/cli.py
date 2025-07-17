from app.field import Field
from app.simulation import Simulation


class SimulationCLI:
    """CLI interface for running an Auto Driving Car Simulation."""
    def __init__(self) -> None:
        """Initialize with an empty simulation instance."""
        self.sim: Simulation | None = None

    def start(self) -> None:
        """Start the CLI by creating a field and entering the simulation loop."""
        print("Welcome to Auto Driving Car Simulation!")
        self.create_field()
        self.simulation_loop()

    def create_field(self) -> None:
        """Prompt user to input field dimensions and initialize the simulation field."""
        while True:
            try:
                width, height = map(int, input("Please enter the width and height of the simulation field in x y "
                                               "format: ").split())
                field = Field(width, height)
                self.sim = Simulation(field)
                return
            except ValueError:
                print("Invalid format. Please enter two integers.")

    def simulation_loop(self) -> None:
        """
        Main user interaction loop for adding cars and running simulations.
        Once the simulation is run, the simulation has to reset, therefore breaking the loop
        Because it is a loop, any input error can reset and not exit the programme
        """
        while True:
            self.print_car_list()
            print("\nPlease choose from the following options:")
            print("[1] Add a car to field")
            print("[2] Run simulation")
            print("[0] Exit")
            choice = input("> ").strip()

            if choice == "1":
                self.add_car()
            elif choice == "2":
                self.run_simulation()
                break
            elif choice == "0":
                print("Thank you for running the simulation. Goodbye!")
                break
            else:
                print("Invalid option.")

    def print_car_list(self) -> None:
        """
        Print a list of all cars currently in the simulation.
        """
        print("\nYour current list of cars are:")
        for name, pos, cmds in self.sim.list_cars():
            print(f"- {name}, ({pos[0]},{pos[1]}) {pos[2]}, {cmds}")

    def add_car(self) -> None:
        """
        Prompt the user to add a new car with position, direction, and commands.
        Any input error will exit back to simulation loop
        """
        # Safeguard
        # if not self.sim:
        #     print("Simulation not initialized.")
        #     return

        # Name check
        name = input("Please enter the name of the car: ").strip()
        if name in self.sim.cars:
            print(f"Car with name '{name}' already exists.")
            return

        # Position input check
        try:
            x_str, y_str, direction = input(f"Please enter initial position of car {name} in x y Direction format: ").split()
            x, y = int(x_str), int(y_str)
        except ValueError:
            print("Invalid input. Format must be: x y D (e.g., 1 2 N)")
            return

        # Direction input check
        direction = direction.upper()
        if direction not in ["N", "S", "E", "W"]:
            print("Invalid direction.")
            return

        # Bounds check
        if not self.sim.field.is_within_bounds(x, y):
            print(f"Position ({x},{y}) is outside the field bounds.")
            return

        # Check if position is occupied
        if (x, y) in [car.position()[:2] for car in self.sim.cars.values()]:
            print(f"Position ({x},{y}) is already occupied by another car.")
            return

        # Command string check
        commands = input(f"Please enter the commands for car {name}: ").strip().upper()
        if not all(c in "FLR" for c in commands):
            print("Commands must only contain F, L, R.")
            return

        # Add car
        try:
            self.sim.add_car(name, x, y, direction, commands)
            print(f"Car {name} added.")
        except ValueError as e:
            print(f"Failed to add car: {e}")


    def run_simulation(self) -> None:
        """
        Run the simulation and display the results of car movements and collisions.
        """
        self.print_car_list()
        print("\nRunning simulation...\n")

        results = self.sim.run_all()

        print("After simulation, the result is:")
        for r in results:
            if r["status"] == "collided":
                print(
                    f"- {r['name']}, collides with {', '.join(r['collision']['with'])} at ({r['collision']['at']['x']},{r['collision']['at']['y']}) at step {r['collision']['step']}")
            else:
                print(f"- {r['name']}, ({r['final']['x']},{r['final']['y']}) {r['final']['direction']}")

        self.post_simulation_options()

    def post_simulation_options(self) -> None:
        """Prompt user to either restart or exit after simulation is completed."""
        while True:
            print("\nPlease choose from the following options:")
            print("[1] Start over")
            print("[2] Exit")
            next_choice = input("> ")
            if next_choice == "1":
                self.start()  # re-init and restart
                return
            elif next_choice == "2":
                print("Thank you for running the simulation. Goodbye!")
                return
            else:
                print("Invalid option.")