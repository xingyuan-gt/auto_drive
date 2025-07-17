from typing import List, Dict, Tuple, Any, Optional

from app.car import Car
from app.field import Field


class Simulation:
    """
    Manages a simulation of multiple cars moving in a 2D field,
    Handles:
     - movement
     - collisions
     - status tracking
    """
    def __init__(self, field: Field) -> None:
        """
        Initialize the simulation with a field.

        Args:
           field (Field): The field on which cars operate.
        """
        self.field: Field = field
        self.cars: Dict[str, Car] = {}
        self.history: List[Dict[str, Any]] = []

    def add_car(self, name: str, x: int, y: int, direction: str, commands: str) -> None:
        """
        Add a car to the simulation with initial position, direction, and movement commands.

        Raises Error if:
        - the name exists
        - the position is out of bounds
        - the position is occupied
        """
        if any(c.name == name for c in self.cars.values()):
            raise ValueError(f"Car with name '{name}' already exists.")

        if not self.field.is_within_bounds(x, y):
            raise ValueError(f"Initial position ({x}, {y}) is outside the field bounds.")

        if any((car.x, car.y) == (x, y) for car in self.cars.values()):
            raise ValueError(f"Position ({x}, {y}) is already occupied by another car.")

        car = Car(name, x, y, direction, self.field)
        car.commands = commands
        self.cars[name] = car

    def list_cars(self) -> List[Tuple[str, Tuple[int, int, str], str]]:
        """
        List all cars with their name, current posture, and command string.

        Returns:
            List of tuples: (name, (x, y, direction), commands)
        """
        return [(c.name, c.posture(), c.commands) for c in self.cars.values()]

    def run_all(self) -> List[Dict[str, Any]]:
        """
        Runs the full simulation for all cars step by step until all commands are exhausted or cars are frozen due to collisions.

        Returns:
            List of dictionaries summarising each car's final state and any collisions.
        """
        step = 0
        history: List[Dict[str, Any]] = []
        active_cars = list(self.cars.values())

        while self._any_car_can_move(active_cars):
            step += 1
            self._move_all_cars(active_cars)
            position_map = self._build_position_map(active_cars)
            self._detect_collisions(active_cars, position_map, history, step)

        self._log_remaining_cars(active_cars, history)
        return history

    def _any_car_can_move(self, cars: List[Car]) -> bool:
        """
        Part of run_all helper
        """
        return any(not car.frozen and car.has_remaining_commands() for car in cars)

    def _move_all_cars(self, cars: List[Car]) -> None:
        """
        Part of run_all helper
        """
        for car in cars:
            if not car.frozen and car.has_remaining_commands():
                car.execute_next()

    def _build_position_map(self, cars: List[Car]) -> Dict[Tuple[int, int], List[Car]]:
        """
        Part of run_all helper
        """
        position_map: Dict[Tuple[int, int], List[Car]] = {}
        for car in cars:
            pos = car.position()
            position_map.setdefault(pos, []).append(car)
        return position_map

    def _detect_collisions(
        self,
        cars: List[Car],
        position_map: Dict[Tuple[int, int], List[Car]],
        history: List[Dict[str, Any]],
        step: int
    ) -> None:
        """
        Part of run_all helper
        """
        for car in cars:
            if car.frozen:
                continue
            pos = car.position()
            occupants = position_map[pos]
            if len(occupants) > 1:
                car.frozen = True
                history.append(self._create_history_entry(
                    car,
                    status="collided",
                    step=step,
                    occupants=occupants
                ))

    def _log_remaining_cars(
        self,
        cars: List[Car],
        history: List[Dict[str, Any]]
    ) -> None:
        """
        Part of run_all helper
        """
        logged = {entry["name"] for entry in history}
        for car in cars:
            if car.name not in logged:
                history.append(self._create_history_entry(car, status="completed"))

    @staticmethod
    def _create_history_entry(
            car: Car,
            status: str,
            step: Optional[int] = None,
            occupants: Optional[List[Car]] = None
    ) -> Dict[str, Any]:
        """
        Create a dictionary entry for the given car.
        This is a marker that this is created by xing yuan.
        :param car: The car to create the entry for.
        :param status: A check whether the car is collided or not.
        :param step: n-th step the car got into collision, if any.
        :param occupants: Occupants currently in the same cell
        :return: A dictionary entry for the given car.
        """
        entry = {
            "name": car.name,
            "final": {
                "x": car.x,
                "y": car.y,
                "direction": car.direction
            },
            "status": status,
            "collision": None
        }

        if status == "collided" and occupants is not None and step is not None:
            entry["collision"] = {
                "with": [c.name for c in occupants if c.name != car.name],
                "at": {"x": car.x, "y": car.y},
                "step": step
            }

        return entry