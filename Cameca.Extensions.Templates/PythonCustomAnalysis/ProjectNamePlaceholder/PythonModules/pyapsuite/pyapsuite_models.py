# Type alias: ion formulas are represended as a dictionary of element names and counts
IonFormula = dict[str: int]

class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class Extents:
    def __init__(self, min: Vector3, max: Vector3):
        self.min = min
        self.max = max

class IonInfo:
    def __init__(self, name: str, formula: IonFormula, volume: float, count: int):
        self.name = name
        self.formula = formula
        self.volume = volume
        self.count = count


class Range:
    def __init__(self, min: float, max: float):
        self.min = min
        self.max = max


class IonRanges:
    def __init__(self, name: str, formula: IonFormula, volume: float, ranges: list[Range]):
        self.name = name
        self.formula = formula
        self.volume = volume
        self.ranges = ranges