import typing
import numpy as np
from .pyapsuite_colors import Color
from .pyapsuite_models import IonFormula
import System.Collections.Generic
import Cameca.CustomAnalysis.Interface
import Cameca.CustomAnalysis.PythonCoreLib


def get_ion_formula(ion_forumla: Cameca.CustomAnalysis.Interface.IonFormula) -> IonFormula:
    return { component.Key: component.Value for component in ion_forumla }

def get_color(
        ion_display_info: Cameca.CustomAnalysis.Interface.IIonDisplayInfo,
        ion_type_info: Cameca.CustomAnalysis.Interface.IIonTypeInfo) -> typing.Optional[Color]:
    if ion_display_info is None:
        return None
    net_color = ion_display_info.GetColor(ion_type_info)
    return get_pyapsuite_color(net_color);

def get_net_color(color: Color) -> System.Windows.Media.Color:
    return System.Windows.Media.Color.FromScRgb(color[3], color[0], color[1], color[2])

def get_pyapsuite_color(color: System.Windows.Media.Color) -> Color:
    return (color.ScR, color.ScG, color.ScB, color.ScA)

def create_ion_formula(formula: dict[str, int]) -> Cameca.CustomAnalysis.Interface.IonFormula:
    components = System.Collections.Generic.List[Cameca.CustomAnalysis.Interface.IonFormula.Component]()
    for (atom, count) in formula.items():
        components.Add(Cameca.CustomAnalysis.Interface.IonFormula.Component(atom, count))
    return Cameca.CustomAnalysis.Interface.IonFormula(components)


def create_range_list(ranges: list[dict[str, float]]) -> System.Collections.Generic.List[Cameca.CustomAnalysis.Interface.Range]:
    range_list = System.Collections.Generic.List[Cameca.CustomAnalysis.Interface.Range]()
    for range_dict in ranges:
        min_ = float(range_dict["min"])
        max_ = float(range_dict["max"])
        range_list.Add(Cameca.CustomAnalysis.Interface.Range(min_, max_))
    return range_list


def get_dtype(system_type: System.Type) -> np.dtype:
    if system_type == System.Type.GetType("System.Single"):
        return np.float32
    if system_type == System.Type.GetType("System.Float"):
        return np.float64
    if system_type == System.Type.GetType("System.Byte"):
        return np.uint8
    if system_type == System.Type.GetType("System.SByte"):
        return np.int8
    if system_type == System.Type.GetType("System.Int16"):
        return np.int16
    if system_type == System.Type.GetType("System.UInt16"):
        return np.uint16
    if system_type == System.Type.GetType("System.Int32"):
        return np.int32
    if system_type == System.Type.GetType("System.UInt32"):
        return np.uint32
    if system_type == System.Type.GetType("System.Int64"):
        return np.int64
    if system_type == System.Type.GetType("System.UInt64"):
        return np.uint64
    
    raise ValueError(f"Unsupported System type: {system_type}")

def get_system_type(dtype: np.dtype) -> System.Type:
    if dtype == np.float32:
        return System.Single
    if dtype == np.float64:
        return System.float
    if dtype == np.uint8:
        return System.Byte
    if dtype == np.int8:
        return System.SByte
    if dtype == np.int16:
        return System.Int16
    if dtype == np.uint16:
        return System.UInt16
    if dtype == np.int32:
        return System.Int32
    if dtype == np.uint32:
        return System.UInt32
    if dtype == np.int64:
        return System.Int64
    if dtype == np.uint64:
        return System.UInt64
    
    raise ValueError(f"Unsupported numpy dtype: {dtype}")

    
def fill_array(array: np.ndarray, dtype: np.dtype, buffer_length: int, lng_ptr: int, chunk_offset: int) -> None:
    ctype = np.ctypeslib.as_ctypes_type(dtype)
    ptr = (ctype * buffer_length).from_address(lng_ptr)
    buffer_ = np.ctypeslib.as_array(ptr)
    array[chunk_offset:chunk_offset + buffer_length] = buffer_

    
def fill_array_from_memory(array: np.ndarray, memory):
    stash_shape = array.shape
    flattened = array.reshape(-1)
    dtype=array.dtype
    try:
        handle = memory.Pin()
        pointer = Cameca.CustomAnalysis.PythonCoreLib.Unsafe.ToIntPtr(handle).ToInt64()
        fill_array(
            flattened,
            dtype,
            flattened.size,
            pointer,
            0)
    finally:
        handle.Dispose()
    array = flattened.reshape(stash_shape)