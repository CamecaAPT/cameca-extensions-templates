import typing
import numpy as np
from .pyapsuite_enums import *
from .pyapsuite_errors import *
from .pyapsuite_functions import *
import System
import Cameca.CustomAnalysis.Interface


class SectionDefinition:

    def __init__(self, data: np.ndarray, unit: str = "", rel_type_unrelated: bool = False, virtual: bool = False, extra_data: typing.Optional[bytes] = None) -> None:
        self.data = data
        self.unit = unit
        self.rel_type_unrelated = rel_type_unrelated
        self.virtual = virtual
        self.extra_data = extra_data

    @classmethod
    def string_section(cls, data: str, unit: str = "", virtual: bool = False, extra_data: typing.Optional[bytes] = None) -> "SectionDefinition":
        encoded_bytes = data.encode('utf8')
        byte_array = np.frombuffer(encoded_bytes, dtype=np.ubyte)
        # Raw byte content should consider each record size one byte and the number of unrelated records is the length of the content
        # A 1D array of bytes needs to be converted to a column vector of bytes. Promote to 2D and transpose to column
        column_array = np.atleast_2d(byte_array).T
        return cls(column_array, unit, True, virtual, extra_data)


class Section:
    
    def __init__(self, ion_data, name: str, functions) -> None:
        self._ion_data = ion_data
        self._name = name
        self._functions = functions

    @property
    def unit(self) -> str:
        return self._get_section_info().Unit
    
    @property
    def protected(self) -> bool:
        return self._get_section_info().IsProtected
    
    @property
    def virtual(self) -> bool:
        return self._get_section_info().IsVirtual
    
    @property
    def extra_data(self) -> bytes:
        return bytes(self._get_section_info().ExtraData)

    @extra_data.setter
    def extra_data(self, data: typing.Optional[bytes]) -> None:
        self._assert_not_protected()
        
        section_info = self._get_section_info()
        data = data if data is not None else bytes()
        section_info.UpdateExtraData(System.ReadOnlyMemory[System.Byte](System.Array[System.Byte](data)))

    @property
    def shape(self) -> tuple[int, int]:
        section_info = self._get_section_info()
        row_count = section_info.RecordCount
        values_pre_record = section_info.ValuesPerRecord
        return (row_count, values_pre_record)

    @property
    def dtype(self) -> np.dtype:
        section_type = self._get_section_info().Type
        return get_dtype(section_type)

    def _get_section_info(self) -> Cameca.CustomAnalysis.Interface.ISectionInfo:
        if not self._ion_data.Sections.ContainsKey(self._name):
            raise PyAPSuiteError("Section does not exist")
        return self._ion_data.Sections[self._name]
    
    def _assert_not_protected(self):
        if self.protected:
            raise PyAPSuiteError("Section is protected")
    
    def _assert_can_write(self):
        if not self.virtual and not self._ion_data.CanWrite:
            raise PyAPSuiteError("Section does not have write access")

    @property
    def data(self) -> np.ndarray:
        """Returns section data
        
        This is equivalent to an APT file section or a column of data in a POS file.
        """
        row_count, values_per_record = self.shape
        dtype = self.dtype
        section_data = np.empty(values_per_record * row_count, dtype=dtype)
    
        chunkOffset = 0
        enumerator = self._ion_data.CreateSectionDataEnumerator(self._name)
        while enumerator.MoveNext():
            chunk = enumerator.Current
            try:
                handle = chunk.ReadSectionData[System.Byte](self._name).Pin()
                pointer = self._functions["ToIntPtr"](handle).ToInt64()
                fill_array(
                    section_data,
                    dtype,
                    chunk.Length * values_per_record,
                    pointer,
                    chunkOffset * values_per_record)
            finally:
                handle.Dispose()
            chunkOffset += chunk.Length
        section_data.shape = (row_count, values_per_record)
        return section_data

    @data.setter
    def data(self, data: np.ndarray) -> None:
        self._assert_not_protected()

        _, val_per_record, *extra = data.shape
        if any(extra):
            raise PyAPSuiteError("Section data expects (n, m) numpy ndarray where n is record count and m is values per record")
        # Validate array types match section
        target_dtype = self.dtype
        if data.dtype != target_dtype:
            raise PyAPSuiteError(f"Section data expects {target_dtype} but got {data.dtype}")
        target_shape = self.shape
        if data.shape != target_shape:
            raise PyAPSuiteError(f"Section data expects {target_shape} but got {data.shape}")
        
        flattened = data.ravel(order='C')
        chunkOffset = 0
        enumerator = self._ion_data.CreateSectionDataEnumerator(self._name)
        while enumerator.MoveNext():
            try:
                chunk = enumerator.Current
                slice = flattened[chunkOffset:chunkOffset + chunk.Length * val_per_record].tobytes(order='C')
                net_buffer = System.ReadOnlyMemory[System.Byte](System.Array[System.Byte](slice))
                chunk.WriteSectionData[System.Byte](self._name, net_buffer)
                chunkOffset += chunk.Length
            finally:
                chunk.Dispose()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._name})"


class Sections:
    """
    Add or change section
    set section by key name with data
    if section exists, tries to update the data
    if section does not exists, adds as a new section
    if integrety check fails, raises an error (e.g. one to one by doesn't match ion count, unsupported data type, etc)
    if section is protected, raises an error

    Delete a section
    del from sections dictionary
    """

    def __init__(self, ion_data, services, functions, get_data_section_name, *args, **kwargs):
        self._ion_data = ion_data
        self._services = services
        self._functions = functions
        # This is a property of the context, but we want the property so it gets re-resolved on each call
        # We can't just resolve the name as it technically is dynamic (e.g. it changes is save as is called on analysis)
        self._get_data_section_name = get_data_section_name
        self._sections = { k: self._create_section(k) for k in self._ion_data.Sections.Keys }

    @property
    def analysis_data(self):
        """Alias for the specific data section convention that AP Suite expects

        AP Suite provides a DataSectionName that should be the default section used for saving analysis data.
        This is an alias to simplify interacting with the 'special' section.

        Because this section will never exist until the custom analysis is created, but loading data will likely
        want to check for existing data, handle the case where the section doesn't exist by returning None instead
        of throwing the typical exception

        `context.sections.analysis_data`
        should be equivalent to
        `context.sections[context.data_section_name]`
        """
        try:
            return self.__getitem__(self._get_data_section_name())
        except PyAPSuiteError:  # TODO: If a custom exception for sections not existing is added, update this
            return None
    
    @analysis_data.setter
    def analysis_data(self, value: typing.Union[np.ndarray, SectionDefinition]) -> None:
        return self.__setitem__(self._get_data_section_name(), value)


    def __getitem__(self, key: str) -> Section:
        self._prune_sections()
        if key in self._sections:
            return self._sections[key]
        elif key in self._get_add_available():
            if self._services["IReconstructionSections"].AddSectionsSync([key]):
                section = self._create_section(key)
                self._sections[key] = section
                return section
        raise PyAPSuiteError("Section does not exist") 
    
    def __setitem__(self, key: str, value: typing.Union[np.ndarray, SectionDefinition]) -> None:
        """Create a new section if not exists, or update the data if exists
        
        if not exists, try to create
        if  exists, try to upate (i.e. delete and replace)
        """
        # Given full SectionDefinition
        if isinstance(value, SectionDefinition):
            sec_def = value
        # Given only numpy array: infer default section values
        elif isinstance(value, np.ndarray):
            sec_def = SectionDefinition(value)
        else:
            raise ValueError("value must be a SectionDefinition or a numpy ndarray")
        
        if not self.can_write and not sec_def.virtual:
            return None
        
        # Collect data early to do some initial pre-vaidation
        # Add section
        record_count, values_per_record, *extra = sec_def.data.shape
        if any(extra) or record_count < 0 or values_per_record < 1:
            raise PyAPSuiteError("Section data expects (n, m) numpy ndarray where n is record count and m is values per record")

        rel_type_is_unrelated = self._ion_data.IonCount != record_count or sec_def.rel_type_unrelated

        dtype = sec_def.data.dtype
        type = get_system_type(dtype)
        # None for record count implies unrelated data section and the correct value will be deduced by AP Suite
        record_count = record_count if rel_type_is_unrelated else None
        data_type_bits = dtype.itemsize * 8
        unit = sec_def.unit
        is_virtual = sec_def.virtual

        section_info = self._get_section_info_safe(key)
        if section_info is not None:
            self._check_protection(section_info)
            self._check_can_write(section_info)
            self.__delitem__(key)

        self._ion_data.AddSection(key, type, record_count, data_type_bits, unit, values_per_record, is_virtual)
        section = self._create_section(key)
        self._sections[key] = section
        section.data = sec_def.data
        section.extra_data = sec_def.extra_data

    @property
    def can_write(self) -> bool:
        return self._ion_data.CanWrite

    @property
    def available(self) -> list[str]:
        add_available = self._get_add_available()
        return [x for x in self._ion_data.Sections.Keys] + add_available

    def _prune_sections(self):
        """Checks that the current section cache matches the ion_data instance, and prune stale entries"""
        current_keys = set(self._ion_data.Sections.Keys)
        for key in list(self._sections.keys()):
            if key not in current_keys:
                self._sections.pop(key, None)

    def _create_section(self, key):
        return Section(self._ion_data, key, self._functions)

    def _get_add_available(self) -> list[str]:
        reconSections = self._services["IReconstructionSections"]
        add_available = []
        if reconSections is not None and reconSections.IsAddSectionAvailable:
            add_available = [x.Name for x in reconSections.GetAvailableSectionsSync()]
        return add_available

    def __contains__(self, key: str):
        self._prune_sections()
        return key in self.available

    def __delitem__(self, key: str):
        """Tries to remove the section from the underlying APT data structure"""
        section_info = self._get_section_info(key)
        self._check_protection(section_info)
        if self._ion_data.DeleteSection(key):
            self._sections.pop(key, None)

    def _get_section_info_safe(self, key: str) -> typing.Optional[Cameca.CustomAnalysis.Interface.ISectionInfo]:
        return self._ion_data.Sections[key] if self._ion_data.Sections.ContainsKey(key) else None

    def _get_section_info(self, key: str) -> Cameca.CustomAnalysis.Interface.ISectionInfo:
        section_info = self._get_section_info_safe(key)
        if section_info is None:
            raise PyAPSuiteError("Section does not exist")
        return section_info

    def _check_protection(self, section_info: Cameca.CustomAnalysis.Interface.ISectionInfo):
        if section_info.IsProtected:
            raise PyAPSuiteError("Section is protected")

    def _check_can_write(self, section_info: Cameca.CustomAnalysis.Interface.ISectionInfo):
        if not section_info.IsVirtual and not self._ion_data.CanWrite:
            raise PyAPSuiteError("Section does not have write access")
        
    def __str__(self) -> str:
        return str(self.available)
