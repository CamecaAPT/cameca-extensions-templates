from typing import TypeVar, Generic
from .pyapsuite_colors import Color

T = TypeVar('T', int, float)

# Type alias: ion formulas are represended as a dictionary of element names and counts
IonFormula = dict[str, int]

class Vector3(Generic[T]):
    def __init__(self, x: T, y: T, z: T):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return _std_str(self)


class Extents:
    def __init__(self, min: Vector3[float], max: Vector3[float]):
        self.min = min
        self.max = max

    def __str__(self) -> str:
        return _std_str(self)

class IonInfo:
    def __init__(self, name: str, formula: IonFormula, volume: float, count: int):
        self.name = name
        self.formula = formula
        self.volume = volume
        self.count = count

    def __str__(self) -> str:
        return _std_str(self)


class Range:
    def __init__(self, min: float, max: float):
        self.min = min
        self.max = max

    def __str__(self) -> str:
        return _std_str(self)


class IonRanges:
    def __init__(self, name: str, formula: IonFormula, volume: float, ranges: list[Range]):
        self.name = name
        self.formula = formula
        self.volume = volume
        self.ranges = ranges

    def __str__(self) -> str:
        return _std_str(self)

class IonRange:
    def __init__(self, name: str, formula: IonFormula, volume: float, min: float, max: float, color: Color):
        self.name = name
        self.formula = formula
        self.volume = volume
        self.min = min
        self.max = max
        self.color = color

    def __str__(self) -> str:
        return _std_str(self)


def _std_str(instance) -> str:
    attrs = ','.join(
        f"{k}={v!r}"
        for k, v in vars(instance).items()
        if not k.startswith('_')
    )
    return f"{instance.__class__.__name__}({attrs})"