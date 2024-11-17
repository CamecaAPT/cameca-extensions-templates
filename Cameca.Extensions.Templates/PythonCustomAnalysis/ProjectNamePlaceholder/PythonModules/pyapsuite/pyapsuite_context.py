import inspect
from .pyapsuite_models import *
from .pyapsuite_sections import *
from .pyapsuite_experiment import *
from .pyapsuite_elements import *
from .pyapsuite_errors import *
from .pyapsuite_chart import *
from .pyapsuite_grid3d import *
from .pyapsuite_colors import FALLBACK_COLOR_DEFINITIONS, Color
import Cameca.CustomAnalysis.Interface as Interface

class APSuiteContext:
	
    def __init__(self, ion_data: Cameca.CustomAnalysis.Interface.IIonData, services: dict[str, object], instance_id: System.Guid):
        # It would be really beneficial to have a way to create instances from raw files that can populate for development puposes
        # A custom IIonData could potentially be create from a file, and most services are optional anyways, so extension should function without
        self._ion_data = ion_data
        self._services = services
        self._instance_id = instance_id
        self._sections = Sections(self._ion_data, self._services, lambda: self.data_section_name)
        self.experiment = Experiment(self._services["IExperimentInfoResolver"])
        self.chart = MainChart(self._services["IChart3D"], self._services["IRenderDataFactory"])
        grid3DData = self._services["IGrid3DData"]
        grid3DParameters = self._services["IGrid3DParameters"]
        self.grid3d = Grid3D(grid3DData, grid3DParameters) if grid3DData is not None and grid3DParameters is not None else None

    @property
    def elements(self) -> list[Element]:
        if self._services["INodeElementDataSet"] is not None:
            set_id = self._services["INodeElementDataSet"].ElementDataSetId
            element_data_set = self._services["IElementDataSetService"].GetElementDataSet(set_id)
        else:
            element_data_set = self._services["IElementDataSetService"].GetDefaultElementDataSet()
        return [
            Element(
                x.AtomicNumber,
                x.Name,
                x.Symbol,
                x.MolarVolume,
                x.AtomicRadius,
                [Isotope(i.Abundance, i.Mass, i.MassNumber) for i in x.Isotopes]
            ) for x in element_data_set.Elements
        ]

    @property
    def filename(self) -> str:
        return self._ion_data.Filename

    @property
    def data_section_name(self) -> str:
        node_info = self._services["INodeInfo"]
        # This really shouldn't be possible in practice
        if node_info is None:
            raise PyAPSuiteError("Data section name is not available")
        return node_info.DataSectionName

    @property
    def ion_count(self) -> int:
        return self._ion_data.IonCount
    
    @property
    def extents(self) -> Extents:
        extents = self._ion_data.Extents
        return Extents(
            Vector3(extents.Min.X, extents.Min.Y, extents.Min.Z),
            Vector3(extents.Max.X, extents.Max.Y, extents.Max.Z),
        )
    
    @property
    def sections(self) -> Sections:
        return self._sections
    
    @property
    def colors(self) -> list[Color]:
        ranges = self._services["IMassSpectrumRangeManager"].GetRanges()
        ion_display_info = self._services["IIonDisplayInfo"]
        if ion_display_info is None:
            return [
                FALLBACK_COLOR_DEFINITIONS[i % len(FALLBACK_COLOR_DEFINITIONS)]
                for i in range(len(ranges))
            ]
        return [get_color(ion_display_info, x.Key) for x in ranges]
    
    @property
    def ions(self) -> list[IonInfo]:
        counts = self._ion_data.GetIonTypeCounts()
        return [
            IonInfo(
                ion.Name,
                get_ion_formula(ion.Formula),
                ion.Volume,
                counts[ion],
            )
            for ion in self._ion_data.Ions]

    @property
    def ion_ranges(self) -> list[IonRange]:
        ranges = self._services["IMassSpectrumRangeManager"].GetIonRanges()
        return [
            IonRange(
                r.Name,
                get_ion_formula(r.Formula),
                r.Volume,
                r.Min,
                r.Max,
                get_pyapsuite_color(r.Color)
            )
            for r in ranges
        ]

    @ion_ranges.setter
    def ion_ranges(self, ranges: list[IonRange]) -> None:
        net_ranges = System.Collections.Generic.List[Cameca.CustomAnalysis.Interface.IonTypeInfoRange]()
        for r in ranges:
            net_ranges.Add(Cameca.CustomAnalysis.Interface.IonTypeInfoRange(
                r.name,
                create_ion_formula(r.formula),
                float(r.volume),
                float(r.min),
                float(r.max),
                get_net_color(r.color)
            ))
        
        self._services["IMassSpectrumRangeManager"].SetIonRangesSync(net_ranges)

    @property
    def ranges(self) -> list[IonRanges]:
        """Deprecated: Use ion_ranges instead. This method does not correctly handle multiple unknown ions and has less functionality"""
        ranges = self._services["IMassSpectrumRangeManager"].GetRanges()
        return [
            IonRanges(
                pair.Value.Name, 
                get_ion_formula(pair.Key),
                pair.Value.Volume,
                [Range(r.Min, r.Max) for r in pair.Value.Ranges]
            )
            for pair in ranges
        ]

    @ranges.setter
    def ranges(self, ranges: list[dict[str, object]]) -> None:
        net_ranges = System.Collections.Generic.Dictionary[Interface.IonFormula, Interface.IonRangeDefinition]()
        for ion_type_ranges in ranges:
            name: str | None = ion_type_ranges["name"] if "name" in ion_type_ranges else None
            ion_formula = create_ion_formula(ion_type_ranges["formula"])
            volume: float | None = float(ion_type_ranges["volume"]) if "volume" in ion_type_ranges else None
            ion_range_list = create_range_list(ion_type_ranges["ranges"])
            ion_range_def = Interface.IonRangeDefinition(ion_range_list, name, volume)
            net_ranges.Remove(ion_formula)
            net_ranges.Add(ion_formula, ion_range_def)
        
        self._services["IMassSpectrumRangeManager"].SetRangesSync(net_ranges)
    
    @property
    def properties(self) -> typing.Optional[System.Object]:
        properties_service = self._services["INodeProperties"]
        if properties_service is None:
            return None
        properties_ = properties_service.Properties
        if properties_ is None:
            return None
        return properties_

    def __str__(self) -> str:
        idt = "  "
        str_lines = [
            f"{self.__class__.__name__}:",
        ]

        properties = []
        functions = []
        fields = []
        for member in dir(self):
            if member.startswith('_'):
                continue
            attr_type = getattr(type(self), member, None)
            if isinstance(attr_type, property):
                properties.append(member)
                continue
            if callable(attr_type):
                functions.append(f"{member}{inspect.signature(getattr(self, member))}")
                continue
            fields.append(member)

        if any(fields):
            str_lines.append(f"{idt}fields:")
            for x in fields:
                str_lines.append(f"{idt*2}{x}")
        if any(properties):
            str_lines.append(f"{idt}properties:")
            for x in properties:
                str_lines.append(f"{idt*2}{x}")
        if any(functions):
            str_lines.append(f"{idt}functions:")
            for x in functions:
                str_lines.append(f"{idt*2}{x}")
        return "\n".join(str_lines)

    def __repr__(self):
            return f"<{self.__class__.__name__}({id(self) & 0xFFFFFF})>"
    