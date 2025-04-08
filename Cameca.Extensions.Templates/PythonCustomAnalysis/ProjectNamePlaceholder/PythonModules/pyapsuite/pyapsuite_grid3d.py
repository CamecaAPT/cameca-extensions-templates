import numpy as np
from .pyapsuite_models import Vector3, Extents
from .pyapsuite_functions import fill_array_from_memory
import Cameca.CustomAnalysis.Interface

class Grid3D:

    def __init__(self, grid_data: Cameca.CustomAnalysis.Interface.IGrid3DData, grid_parameters: Cameca.CustomAnalysis.Interface.IGrid3DParameters):
        self._grid_data = grid_data
        self._grid_parameters = grid_parameters
    
    @property
    def voxel_size(self) -> Vector3[float]:
        net = self._grid_parameters.VoxelSize
        return Vector3[float](net.X, net.Y, net.Z)
    
    @property
    def delocalization(self) -> Vector3[float]:
        net = self._grid_parameters.Delocalization
        return Vector3[float](net.X, net.Y, net.Z)
    
    @property
    def erode_by_delocalization(self) -> bool:
        return self._grid_parameters.ErodeByDelocalization
    
    @property
    def do_first_pass_deloc(self) -> bool:
        return self._grid_parameters.DoFirstPassDeloc
    
    @property
    def num_voxels(self) -> Vector3[int]:
        net = self._grid_data.NumVoxels
        return Vector3[int](net[0], net[1], net[2])
    
    @property
    def voxel_size(self) -> Vector3[float]:
        net = self._grid_data.VoxelSize
        return Vector3[float](net[0], net[1], net[2])
    
    @property
    def grid_delta(self) -> Vector3[float]:
        net = self._grid_data.GridDelta
        return Vector3[float](net[0], net[1], net[2])
    
    @property
    def grid_range(self) -> Extents:
        net = self._grid_data.GridRange
        return Extents(
            Vector3[float](net.GetValue(0, 0), net.GetValue(1, 0), net.GetValue(2, 0)),
            Vector3[float](net.GetValue(0, 1), net.GetValue(1, 1), net.GetValue(2, 1))
        )

    def get_for_ion_index(self, ion_index: int) -> np.ndarray:
        buffer = self._grid_data.GetDataForIon(ion_index)
        count = buffer.Length
        np_pos = np.empty(count, dtype=np.float32)
        fill_array_from_memory(np_pos, buffer)
        num_voxels = self._grid_data.NumVoxels
        return np_pos.reshape((num_voxels[2], num_voxels[1], num_voxels[0])).transpose(2, 1, 0)
