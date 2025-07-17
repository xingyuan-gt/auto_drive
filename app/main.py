from app.field import Field
from app.simulation import Simulation

def start_simulation():
    print("Welcome to Auto Driving Car Simulation!")
    width, height = map(int, input("Please enter the width and height of the simulation field in x y format: ").split())
    field = Field(width, height)
    sim = Simulation(field)

    while True:
        print("\nYour current list of cars are:")
        cars = sim.list_cars()
        for name, pos, cmds in cars:
            print(f"- {name}, ({pos[0]},{pos[1]}) {pos[2]}, {cmds}" if cmds else f"- {name}, ({pos[0]},{pos[1]}) {pos[2]}")

        print("\nPlease choose from the following options:")
        print("[1] Add a car to field")
        print("[2] Run simulation")
        print("[0] Exit")

        choice = input("> ")

        if choice == "1":
            name = input("Please enter the name of the car: ").strip()
            x, y, direction = input(f"Please enter initial position of car {name} in x y Direction format: ").split()
            direction = direction.upper()
            if direction not in ["N", "S", "E", "W"]:
                print("Invalid direction.")
                continue
            commands = input(f"Please enter the commands for car {name}: ").strip().upper()
            sim.add_car(name, int(x), int(y), direction, commands)
            print(f"Car {name} added.")

        elif choice == "2":
            print("\nYour current list of cars are:")
            for name, pos, cmds in sim.list_cars():
                print(f"- {name}, ({pos[0]},{pos[1]}) {pos[2]}, {cmds}")
            print("\nRunning simulation...\n")

            results = sim.run_all()

            print("After simulation, the result is:")
            for r in results:
                if r["status"] == "collided":
                    print(
                        f"- {r['name']}, collides with {', '.join(r['collision']['with'])} at ({r['collision']['at']['x']},{r['collision']['at']['y']}) at step {r['collision']['step']}")
                else:
                    print(f"- {r['name']}, ({r['final']['x']},{r['final']['y']}) {r['final']['direction']}")

            print("\nPlease choose from the following options:")
            print("[1] Start over")
            print("[2] Exit")
            next_choice = input("> ")
            if next_choice == "1":
                start_simulation()  # recursively restart
                return
            else:
                print("Thank you for running the simulation. Goodbye!")
                return

        elif choice == "0":
            print("Thank you for running the simulation. Goodbye!")
            return

        else:
            print("Invalid option.")

if __name__ == "__main__":
    start_simulation()
