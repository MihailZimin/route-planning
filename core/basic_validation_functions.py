"""Basic validation functions for core geometry objects."""


class BasicValidationFunctions:
    """
    Class with basic validation functions.
    """

    X_MAX_COORDS: float = 1000.0
    X_MIN_COORDS: float = 0.0
    Y_MAX_COORDS: float = 1000.0
    Y_MIN_COORDS: float = 0.0
    MIN_RADIUS: float = 0.0
    MAX_RADIUS: float = 1000.0

    @staticmethod
    def check_radius(radius: float | object) -> None:
        """
        Check radius correctness.

        Args:
            radius: radius of geometry object (circle or arc)

        Raises:
            ValueError if data is incorrect.

        """
        error_msg = ""
        if not isinstance(radius, (int, float)):
            error_msg += f"radius: {radius} is not a number\n"
        else:
            if radius < BasicValidationFunctions.MIN_RADIUS:
                error_msg += (
                    f"radius is lower than lower bound: {radius} < {BasicValidationFunctions.MIN_RADIUS}"
                )
            if radius > BasicValidationFunctions.MAX_RADIUS:
                error_msg += (
                    f"radius is upper than upper bound: {radius} > {BasicValidationFunctions.MAX_RADIUS}"
                )

        if error_msg:
            raise ValueError(error_msg)

    @staticmethod
    def check_coord(coord: float | object, label: str) -> None:
        """
        Check coordinate correctness.

        Args:
            coord: x or y coordinates
            label: coord name (x or y)


        Raises:
            ValueError if data is incorrect.

        """
        error_msg = ""
        if not isinstance(coord, (int, float)):
            error_msg += f"{label} coordinate: '{coord}' is not a number\n"
        else:
            if coord < BasicValidationFunctions.X_MIN_COORDS:
                error_msg += (
                    f"{label} coordinate is lower than lower bound: "
                    f"{coord} < {BasicValidationFunctions.X_MIN_COORDS}\n"
                )
            if coord > BasicValidationFunctions.X_MAX_COORDS:
                error_msg += (
                    f"{label} coordinate is upper than upper bound: "
                    f"{coord} > {BasicValidationFunctions.X_MAX_COORDS}\n"
                )

        if error_msg:
            raise ValueError(error_msg)
