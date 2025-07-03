# I don't get why this isn't working, as I verify that os.getenv("PYTHON_NET_MODE")
# is set by the extension, but it still tries to import the .NET assemblies
# Commenting out does stop my crash, which I think is caused by clasing import of .NET assemblies
# Removing this block does stop being able to run directly from Python to test,
# but that currently doesn't work well anyways without the required CSharp component
# So not supporting that right now is probably fine unless some shims are added later

# import os
# if os.getenv("PYTHON_NET_MODE") != "CSharp":
#     import pathlib
#     # Relative path, needs to point at the root extension directory with .runtimeconfig.json and Cameca.CustomAnalysis.Interface.dll
#     extension_root = pathlib.Path(__file__).parent.parent.parent
#     import pythonnet
#     # Need to call load 'coreclr' to load .NET Core instead of framework before calling import clr
#     # Must set runtime_config from the extension diretory to target correct runtime version for importing .NET assemblies
#     runtimeconfig_path = next(map(str, extension_root.glob("*.runtimeconfig.json")), None)
#     pythonnet.load('coreclr', runtime_config=runtimeconfig_path)
#     # Update path for .NET assemblies for adding references
#     import sys
#     # sys.path.insert(0, str(extension_root))
#     sys.path.append(str(extension_root))
#     import clr
#     clr.AddReference("Cameca.CustomAnalysis.Interface")

import clr
clr.AddReference("Cameca.CustomAnalysis.PythonCoreLib")
import Cameca.CustomAnalysis.PythonCoreLib

from .pyapsuite_chart import (ChartObject, Surface, Points, Spheres, MainChart)
from .pyapsuite_colors import (Color, FALLBACK_COLOR_DEFINITIONS)
from .pyapsuite_context import (APSuiteContext)
from .pyapsuite_elements import (Isotope, Element)
from .pyapsuite_enums import (AquisitionMode, InstrumentModel, InvizoBeamMode, LaserBand)
from .pyapsuite_errors import (PyAPSuiteError)
from .pyapsuite_experiment import (Experiment)
from .pyapsuite_functions import (get_color, get_pyapsuite_color, get_net_color)
from .pyapsuite_models import (IonInfo, Range, IonRanges, Vector3, Extents, IonRange)
from .pyapsuite_sections import (Section, Sections, SectionDefinition)