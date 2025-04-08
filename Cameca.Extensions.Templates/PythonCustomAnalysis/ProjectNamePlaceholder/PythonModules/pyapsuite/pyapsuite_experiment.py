import typing
from .pyapsuite_enums import *
import Cameca.CustomAnalysis.Interface


T = typing.TypeVar("T")
class Experiment:

    def __init__(self, exp_info_resolver: Cameca.CustomAnalysis.Interface.IExperimentInfoResolver) -> None:
        self._exp_info_resolver = exp_info_resolver
    
    @property
    def filename(self) -> typing.Optional[str]:
        return self._exp_info_resolver.ExperimentFileName if self._exp_info_resolver is not None else None
    
    @property
    def analysis_pressure(self) -> typing.Optional[float]:
        return self._get(lambda x: x.AnalysisPressure)

    @property
    def aperture_name(self) -> typing.Optional[str]:
        return self._get(lambda x: x.ApertureName)

    @property
    def atom_probe_id(self) -> typing.Optional[int]:
        return self._get(lambda x: x.AtomProbeId)

    @property
    def atom_probe_name(self) -> typing.Optional[str]:
        return self._get(lambda x: x.AtomProbeName)

    @property
    def calibration_file_name(self) -> typing.Optional[str]:
        return self._get(lambda x: x.CalibrationFileName)

    @property
    def comments(self) -> typing.Optional[str]:
        return self._get(lambda x: x.Comments)

    @property
    def delta_tofcorr_sigma(self) -> typing.Optional[float]:
        return self._get(lambda x: x.DeltaTOFCorrSigma)

    @property
    def detector_efficiency(self) -> typing.Optional[float]:
        return self._get(lambda x: x.DetectorEfficiency)

    @property
    def elapsed_time_sec(self) -> typing.Optional[int]:
        return self._get(lambda x: x.ElapsedTimeSec)

    @property
    def flight_path(self) -> typing.Optional[float]:
        return self._get(lambda x: x.FlightPath)

    @property
    def hit_finding_version(self) -> typing.Optional[str]:
        return self._get(lambda x: x.HitFindingVersion)

    @property
    def invizo_beam_mode(self) -> typing.Optional[InvizoBeamMode]:
        val = self._get(lambda x: x.InvizoBeamMode)
        return InvizoBeamMode(val) if val is not None else None

    @property
    def instrument_model_number(self) -> typing.Optional[InstrumentModel]:
        val = self._get(lambda x: x.InstrumentModelNumber)
        return InstrumentModel(val) if val is not None else None

    @property
    def laser_band_num(self) -> typing.Optional[LaserBand]:
        val = self._get(lambda x: x.LaserBandNum)
        return LaserBand(val) if val is not None else None

    @property
    def laser_energy_normalization(self) -> typing.Optional[float]:
        return self._get(lambda x: x.LaserEnergyNormalization)

    @property
    def laser_power_range(self) -> typing.Optional[LaserPowerRange]:
        val = self._get(lambda x: x.LaserPowerRange)
        return LaserPowerRange(val) if val is not None else None

    @property
    def las_root_version(self) -> typing.Optional[str]:
        return self._get(lambda x: x.LasRootVersion)

    @property
    def last_run_laser_energy_pj(self) -> typing.Optional[float]:
        return self._get(lambda x: x.LastRunLaserEnergyPJ)

    @property
    def last_run_voltage(self) -> typing.Optional[float]:
        return self._get(lambda x: x.LastRunVoltage)

    @property
    def las_version(self) -> typing.Optional[str]:
        return self._get(lambda x: x.LasVersion)

    @property
    def max_aperture_amplitude(self) -> typing.Optional[float]:
        return self._get(lambda x: x.MaxApertureAmplitude)

    @property
    def mcp_efficiency(self) -> typing.Optional[float]:
        return self._get(lambda x: x.McpEfficiency)

    @property
    def mesh_efficiency(self) -> typing.Optional[float]:
        return self._get(lambda x: x.MeshEfficiency)

    @property
    def name(self) -> typing.Optional[str]:
        return self._get(lambda x: x.Name)

    @property
    def project_name(self) -> typing.Optional[str]:
        return self._get(lambda x: x.ProjectName)

    @property
    def pulse_frequency(self) -> typing.Optional[float]:
        return self._get(lambda x: x.PulseFrequency)

    @property
    def results(self) -> typing.Optional[str]:
        return self._get(lambda x: x.Results)

    @property
    def run_end_reason(self) -> typing.Optional[str]:
        return self._get(lambda x: x.RunEndReason)

    @property
    def run_number(self) -> typing.Optional[int]:
        return self._get(lambda x: x.RunNumber)

    @property
    def specimen_condition(self) -> typing.Optional[str]:
        return self._get(lambda x: x.SpecimenCondition)

    @property
    def specimen_name(self) -> typing.Optional[str]:
        return self._get(lambda x: x.SpecimenName)

    @property
    def specimen_temperature(self) -> typing.Optional[float]:
        return self._get(lambda x: x.SpecimenTemperature)

    @property
    def start_date(self) -> typing.Optional[str]:
        return self._get(lambda x: x.StartDate)

    @property
    def start_time(self) -> typing.Optional[str]:
        return self._get(lambda x: x.StartTime)

    @property
    def stream_version(self) -> typing.Optional[int]:
        return self._get(lambda x: x.StreamVersion)

    @property
    def t0estimate(self) -> typing.Optional[float]:
        return self._get(lambda x: x.T0Estimate)

    @property
    def target_pulse_fraction(self) -> typing.Optional[float]:
        return self._get(lambda x: x.TargetPulseFraction)

    @property
    def user_acq_mode(self) -> typing.Optional[AquisitionMode]:
        val = self._get(lambda x: x.UserAcqMode)
        return AquisitionMode(val) if val is not None else None

    def refresh(self) -> None:
        if self._exp_info_resolver is not None:
            self._exp_info_resolver.Refresh()

    def _get(self, accessor: typing.Callable[[Cameca.CustomAnalysis.Interface.IExperimentInfo], T]) -> typing.Optional[T]:
        if self._exp_info_resolver is None:
            return None
        info = self._exp_info_resolver.ExperimentInfo
        if info is None:
            return None
        return accessor(info)