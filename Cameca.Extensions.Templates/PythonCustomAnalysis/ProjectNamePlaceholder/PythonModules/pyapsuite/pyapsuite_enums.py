import enum

class AquisitionMode(enum.Enum):
	Unknown = 0
	Voltage = 1
	Laser = 2
	VPlusL = 3
	FIM = 4

class InstrumentModel(enum.Enum):
	Unknown = 0
	Alpha = 1
	Beta = 2
	LEAP3000 = 3
	LEAP3000X = 4
	LEAP3000Si = 5
	LEAP3000XSi = 6
	LEAP3000HR = 7
	LEAP3000XHR = 8
	LEAP4000S = 9
	LEAP4000XS = 10
	LEAP4000R = 11
	LEAP4000XR = 12
	LEAP5000S = 13
	LEAP5000XS = 14
	LEAP5000R = 15
	LEAP5000XR = 16
	INVIZO6000 = 17
	EIKOS = 18
	EIKOSX = 19
	EIKOSUV = 20
	LEAP6000R = 21
	LEAP6000XR = 22
	ONS_3DAP = 10000
	FLEXTAP_Deg8 = 20000
	FLEXTAP_Deg12 = 20001
	FLEXTAP_Deg15 = 20002
	FLEXTAP_Deg18 = 20003
	FLEXTAP_Deg20 = 20004
	FLEXTAP_Deg22 = 20005
	FLEXTAP_Deg25 = 20006
	FLEXTAP_Deg28 = 20007
	FLEXTAP_Deg30 = 20008
	FLEXTAP_Deg4 = 20009
	LAWATAP = 20010

class InvizoBeamMode(enum.Enum):
	NotApplicable = -2
	Variable = -1
	Unknown = 0
	Lower = 1
	Upper = 2
	Dual = 3
	None_ = 4

class LaserBand(enum.Enum):
	Unknown = -1
	Band_532 = 0
	Band_400 = 1
	Band_355 = 2
	EikosBand_355 = 3
	Band_258 = 5

class LaserPowerRange(enum.Enum):
	Unknown = -1
	ExtraLow = 0
	Low = 1
	Medium = 2
	High = 3
	Automatic = 4
