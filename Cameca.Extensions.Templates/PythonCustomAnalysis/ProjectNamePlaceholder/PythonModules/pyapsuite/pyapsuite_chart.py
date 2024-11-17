import typing
import numpy as np
from .pyapsuite_colors import *
from .pyapsuite_errors import *
from .pyapsuite_functions import *
import System.Numerics
import Cameca.CustomAnalysis.Interface

class ChartObject:
    def __init__(self, visible: bool = True) -> None:
        self._visible = visible
        
    @property
    def visible(self) -> bool:
        return self._render_data.IsVisible if self._render_data is not None else self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        if self._render_data is not None:
            self._render_data.IsVisible = value
        self._visible = value

class Points(ChartObject):

    # Class level incrementing variable for cycling through default colors if not specified
    color_i = 0

    def __init__(self, positions: np.ndarray, color: typing.Optional[Color] = None, visible: bool = True) -> None:
        super().__init__(visible)
        _validate_positions(positions)
        self._positions = positions
        self._color = color if color is not None else Points._get_next_color()
        self._render_data: typing.Optional[Cameca.CustomAnalysis.Interface.IPointsRenderData] = None

    @classmethod
    def _from_render_data(cls, render_data: Cameca.CustomAnalysis.Interface.IPointsRenderData) -> "Points":
        """Create a Points instance from an existing IPointsRenderData object"""
        points = cls(
            _readonly_memory_as_np_pos(render_data.Positions),
            get_pyapsuite_color(render_data.Color),
            render_data.IsVisible
        )
        points._register_render_data(render_data)
        return points

    def _register_render_data(self, render_data: Cameca.CustomAnalysis.Interface.IPointsRenderData) -> None:
        """Internal method called when the points are added to the chart. Injects the IRenderData for propety updates"""
        self._render_data = render_data

    @property
    def color(self) -> Color:
        if self._render_data is not None:
            return get_pyapsuite_color(self._render_data.Color)
        else:
            return self._color
    
    @color.setter
    def color(self, value: Color) -> None:
        if self._render_data is not None:
            self._render_data.Color = get_net_color(value)
        self._color = value

    @property
    def positions(self) -> np.ndarray:
        if self._render_data is not None:
            return _readonly_memory_as_np_pos(self._render_data.Positions)
        return self._positions

    @positions.setter
    def positions(self, value: np.ndarray) -> None:
        _validate_positions(value)
        if self._render_data is not None:
            buffer = _np_pos_as_readonly_memory(value)
            self._render_data.Positions = buffer
        self._positions = value
    
    def __eq__(self, other) -> bool:
        """Two Points are equal if they both wrap the same backing chart object
        
        If not attached to a chart, then an Points instance is never equal to another.
        If attached to a chart, then the Points are equal if they both have the same name (key).
        """
        if self._render_data is None or other._render_data is None:
            return False
        return self._render_data.Name == other._render_data.Name

    @classmethod
    def _get_next_color(cls) -> Color:
        """Get the next color in the default color cycle"""
        color = FALLBACK_COLOR_DEFINITIONS[cls.color_i % len(FALLBACK_COLOR_DEFINITIONS)]
        cls.color_i += 1
        return color
    

class Spheres(Points):
    """Resolution is approximately the number of points around circumference of a sphere"""

    def __init__(self, positions: np.ndarray, color: typing.Optional[Color] = None, visible: bool = True, resolution: typing.Optional[int] = None, radius: typing.Optional[float] = None) -> None:
        super().__init__(positions, color, visible)
        self._render_data: typing.Optional[Cameca.CustomAnalysis.Interface.ISpheresRenderData] = None
        self._resolution = resolution
        self._radius = radius

    @classmethod
    def _from_render_data(cls, render_data: Cameca.CustomAnalysis.Interface.ISpheresRenderData) -> "Spheres":
        """Create a Points instance from an existing ISpheresRenderData object"""
        spheres = cls(
            _readonly_memory_as_np_pos(render_data.Positions),
            get_pyapsuite_color(render_data.Color),
            render_data.IsVisible,
            render_data.Resolution,
            render_data.Radius
        )
        spheres._register_render_data(render_data)
        return spheres

    def _register_render_data(self, render_data: Cameca.CustomAnalysis.Interface.ISpheresRenderData) -> None:
        """Internal method called when the points are added to the chart. Injects the IRenderData for propety updates"""
        self._render_data = render_data

    @property
    def resolution(self) -> int:
        return self._render_data.Resolution if self._render_data is not None else self._resolution
    
    @resolution.setter
    def resolution(self, value: int) -> None:
        if self._render_data is not None:
            self._render_data.Resolution = value
        self._radius = value

    @property
    def radius(self) -> float:
        return self._render_data.Radius if self._render_data is not None else self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if self._render_data is not None:
            self._render_data.Radius = value
        self._radius = value
    
    def __eq__(self, other) -> bool:
        """Two Points are equal if they both wrap the same backing chart object
        
        If not attached to a chart, then an Points instance is never equal to another.
        If attached to a chart, then the Points are equal if they both have the same name (key).
        """
        if self._render_data is None or other._render_data is None:
            return False
        return self._render_data.Name == other._render_data.Name

class Surface(ChartObject):

    # Class level incrementing variable for cycling through default colors if not specified
    color_i = 0

    def __init__(self, vertices: np.ndarray, indices: np.ndarray, color: typing.Optional[Color] = None, visible: bool = True) -> None:
        super().__init__(visible)
        _validate_positions(vertices)
        _validate_indices(indices)
        self._vertices = vertices
        self._indices = indices
        self._color = color if color is not None else Points._get_next_color()
        self._render_data: typing.Optional[Cameca.CustomAnalysis.Interface.ISurfaceRenderData] = None

    @classmethod
    def _from_render_data(cls, render_data: Cameca.CustomAnalysis.Interface.ISurfaceRenderData) -> "Surface":
        """Create a Surface instance from an existing ISurfaceRenderData object"""
        surface = cls(
            _readonly_memory_as_np_pos(render_data.SurfaceMesh.Vertices),
            _readonly_memory_as_np_ind(render_data.SurfaceMesh.Indices),
            get_pyapsuite_color(render_data.Color),
            render_data.IsVisible
        )
        surface._register_render_data(render_data)
        return surface

    def _register_render_data(self, render_data: Cameca.CustomAnalysis.Interface.ISurfaceRenderData) -> None:
        """Internal method called when the points are added to the chart. Injects the IRenderData for propety updates"""
        self._render_data = render_data

    @property
    def vertices(self) -> np.ndarray:
        if self._render_data is not None:
            return _readonly_memory_as_np_pos(self._render_data.SurfaceMesh.Vertices)
        return self._vertices

    @vertices.setter
    def vertices(self, value: np.ndarray) -> None:
        _validate_positions(value)
        if self._render_data is not None:
            net_ita = self._render_data.SurfaceMesh
            self._render_data.SurfaceMesh = Cameca.CustomAnalysis.Interface.IndexedTriangleArray(
                _np_pos_as_readonly_memory(value),
                net_ita.Indices,
            )
        self._vertices = value
        
    @property
    def indices(self) -> np.ndarray:
        if self._render_data is not None:
            return _readonly_memory_as_np_ind(self._render_data.SurfaceMesh.Indices)
        return self._indices

    @indices.setter
    def indices(self, value: np.ndarray) -> None:
        _validate_indices(value)
        if self._render_data is not None:
            net_ita = self._render_data.SurfaceMesh
            self._render_data.SurfaceMesh = Cameca.CustomAnalysis.Interface.IndexedTriangleArray(
                net_ita.Vertices,
                _np_ind_as_readonly_memory(value),
            )
        self._indices = value

    @property
    def color(self) -> Color:
        if self._render_data is not None:
            return get_pyapsuite_color(self._render_data.Color)
        else:
            return self._color
    
    @color.setter
    def color(self, value: Color) -> None:
        if self._render_data is not None:
            self._render_data.Color = get_net_color(value)
        self._color = value

    def __eq__(self, other) -> bool:
        """Two Surfaces are equal if they both wrap the same backing chart object
        
        If not attached to a chart, then an Surfaces instance is never equal to another.
        If attached to a chart, then the Surfaces are equal if they both have the same name (key).
        """
        if self._render_data is None or other._render_data is None:
            return False
        return self._render_data.Name == other._render_data.Name

class MainChart:

    def __init__(self, chart: Cameca.CustomAnalysis.Interface.IChart3D, render_data_factory: Cameca.CustomAnalysis.Interface.IRenderDataFactory) -> None:
        self._chart = chart
        self._render_data_factory = render_data_factory

    @property
    def _render_data_names(self) -> list[str]:
        return [x.Name for x in self._chart.DataSource]

    def __getitem__(self, key: str) -> ChartObject:
        for i, render_data in enumerate(self._chart.DataSource):
            if (render_data.Name == key):
                render_data = self._chart.DataSource[i]
                if isinstance(render_data, Cameca.CustomAnalysis.Interface.ISpheresRenderData):
                    return Spheres._from_render_data(render_data)
                elif isinstance(render_data, Cameca.CustomAnalysis.Interface.IPointsRenderData):
                    return Points._from_render_data(render_data)
                elif isinstance(render_data, Cameca.CustomAnalysis.Interface.ISurfaceRenderData):
                    return Surface._from_render_data(render_data)
                raise PyAPSuiteError("Unknown chart object type: %s" % type(render_data))
        raise PyAPSuiteError("Chart object does not exist: %s" % key) 
    
    def __setitem__(self, key: str, value: ChartObject) -> None:
        """Add objects to the main chart
        
        if not exists, try to create
        if  exists, delete and replace
        """
        if key in self._render_data_names:
            del self[key]
        render_data = self._create_render_data_from_chart_object(key, value)
        # Register the render data
        value._register_render_data(render_data)
        self._chart.DataSource.Add(render_data)
    
    def _create_render_data_from_chart_object(self, key: str, value: ChartObject) -> ChartObject:
        # Don't use isinstance as we need exact type, not inheritance support
        if type(value) == Spheres:
            net_spheres = self._render_data_factory.CreateSpheres()
            net_spheres.Name = key
            net_spheres.Color = get_net_color(value.color)
            net_spheres.Positions = _np_pos_as_readonly_memory(value.positions)
            net_spheres.IsVisible = value.visible
            if value.resolution is not None:
                net_spheres.Resolution = value.resolution
            if value.radius is not None:
                net_spheres.Radius = value.radius
            return net_spheres
        elif type(value) == Points:
            net_points = self._render_data_factory.CreatePoints()
            net_points.Name = key
            net_points.Color = get_net_color(value.color)
            net_points.Positions = _np_pos_as_readonly_memory(value.positions)
            net_points.IsVisible = value.visible
            return net_points
        elif type(value) == Surface:
            net_points = self._render_data_factory.CreateSurface()
            net_points.Name = key
            net_points.Color = get_net_color(value.color)
            net_points.SurfaceMesh = Cameca.CustomAnalysis.Interface.IndexedTriangleArray(
                _np_pos_as_readonly_memory(value.vertices),
                _np_ind_as_readonly_memory(value.indices),
            ) 
            net_points.IsVisible = value.visible
            return net_points
        raise PyAPSuiteError("Unknown chart object type: %s" % type(value))

    def __contains__(self, key: str):
        return key in self._render_data_names

    def __delitem__(self, key: str):
        """Tries to remove the render data from the chart by name"""
        found = False
        for i, render_data in enumerate(self._chart.DataSource):
            if (render_data.Name == key):
                found = True
                break
        if found:
            self._chart.DataSource[i].Dispose()
            self._chart.DataSource.RemoveAt(i)
    
    def __str__(self) -> str:
        """Return joined names of all the items render data in the chart"""
        return f"[{(', '.join(self._render_data_names))}]"

# Utiltiy functions for working with position arrays
def _validate_indices(indices: np.ndarray) -> None:
    if indices.dtype != np.int32:
        raise PyAPSuiteError("Indices must be of type np.float32: got %s" % indices.dtype)

def _validate_positions(positions: np.ndarray, label: str = "Positions") -> None:
    if positions.dtype != np.float32:
        raise PyAPSuiteError("%s must be of type np.float32: got %s" % (label, positions.dtype))
    if len(positions.shape) != 2 or positions.shape[1] != 3:
        raise PyAPSuiteError("%s shape must match (n, 3): got %s" % (label, str(positions.shape)))

def _readonly_memory_as_np_pos(buffer: System.ReadOnlyMemory[System.Numerics.Vector3]) -> np.ndarray:
    """Convert a read-only memory buffer to a numpy array"""
    count = buffer.Length
    np_pos = np.empty((count, 3), dtype=np.float32)
    fill_array_from_memory(np_pos, buffer)
    return np_pos

def _readonly_memory_as_np_ind(buffer: System.ReadOnlyMemory[System.Int32]) -> np.ndarray:
    """Convert a read-only memory buffer to a numpy array"""
    count = buffer.Length
    np_ind = np.empty(count, dtype=np.int32)
    fill_array_from_memory(np_ind, buffer)
    return np_ind


def _np_pos_as_readonly_memory(np_pos: np.ndarray) -> System.ReadOnlyMemory[System.Numerics.Vector3]:
    """Convert a numpy array to a read-only memory buffer"""
    _validate_positions(np_pos)
    length = np_pos.shape[0]
    arr = System.Array[System.Numerics.Vector3](length)
    for i in range(length):
        arr[i] = System.Numerics.Vector3(np_pos[i, 0], np_pos[i, 1], np_pos[i, 2])
    return System.ReadOnlyMemory[System.Numerics.Vector3](arr)

def _np_ind_as_readonly_memory(np_ind: np.ndarray) -> System.ReadOnlyMemory[System.Numerics.Vector3]:
    """Convert a numpy array to a read-only memory buffer"""
    _validate_indices(np_ind)
    length = np_ind.size
    arr = System.Array[System.Int32](length)
    for i in range(length):
        arr[i] = np_ind[i]
    return System.ReadOnlyMemory[System.Int32](arr)