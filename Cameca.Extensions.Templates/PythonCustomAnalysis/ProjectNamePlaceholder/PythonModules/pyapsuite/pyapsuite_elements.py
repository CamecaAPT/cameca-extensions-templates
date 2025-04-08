class Isotope:
    def __init__(self, abundance: float, mass: float, mass_number: int) -> None:
        self.abundance = abundance
        self.mass = mass
        self.mass_number = mass_number
        
class Element:
    def __init__(self, atomic_number: int, name: str, symbol: str, molar_volume: float, atomic_radius: float, isotopes: list[Isotope]) -> None:
        self.atomic_number = atomic_number
        self.name = name
        self.symbol = symbol
        self.molar_volume = molar_volume
        self.atomic_radius = atomic_radius
        self.isotopes = isotopes
