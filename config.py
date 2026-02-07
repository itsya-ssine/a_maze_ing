from typing import Dict, Tuple


type ConfigDict = Dict[str, object]


def read_config(path: str) -> ConfigDict:
    raw: Dict[str, str] = {}

    try:
        with open(path, "r", encoding="utf-8") as file:
            for i, line in enumerate(file, start=1):
                try:
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue

                    if "=" not in line:
                        raise ValueError(
                            f"Invalid format at line {i}"
                        )

                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    if not key or not value:
                        raise ValueError(
                            f"Empty key or value at line {i}"
                        )

                    raw[key] = value

                except ValueError as exc:
                    raise RuntimeError(str(exc)) from exc

    except OSError as exc:
        raise RuntimeError(
            f"Unable to open configuration file: {exc}"
        ) from exc

    _validate_required_keys(raw)
    return _convert_config(raw)


def _validate_required_keys(config: Dict[str, str]) -> None:
    required_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    for key in required_keys:
        if key not in config:
            raise RuntimeError(f"Missing mandatory key: {key}")


def _convert_config(raw: Dict[str, str]) -> ConfigDict:
    try:
        width: int = int(raw["WIDTH"])
        height: int = int(raw["HEIGHT"])
    except ValueError as exc:
        raise RuntimeError("WIDTH and HEIGHT must be integers") from exc

    entry: Tuple[int, int] = _parse_coordinates(raw["ENTRY"], "ENTRY")
    exit_: Tuple[int, int] = _parse_coordinates(raw["EXIT"], "EXIT")

    output_file: str = raw["OUTPUT_FILE"]

    perfect: bool
    value = raw["PERFECT"].lower()
    if value == "true":
        perfect = True
    elif value == "false":
        perfect = False
    else:
        raise RuntimeError("PERFECT must be True or False")

    return {
        "WIDTH": width,
        "HEIGHT": height,
        "ENTRY": entry,
        "EXIT": exit_,
        "OUTPUT_FILE": output_file,
        "PERFECT": perfect,
    }


def _parse_coordinates(value: str, name: str) -> Tuple[int, int]:
    try:
        x_str, y_str = value.split(",")
        return int(x_str), int(y_str)
    except (ValueError, AttributeError) as exc:
        raise RuntimeError(
            f"{name} must be in format x,y"
        ) from exc
