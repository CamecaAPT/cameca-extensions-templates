The pyapsuite module in this folder is a copy of the real files provided by Cameca.CustomAnalysis.PythonCore.
They are provided only for easy of Python development, by allowing type information and autocomplete in editors such as VS Code.
When compiled, the files from the PythonCore dependency are included in the build output, NOT this copy. Do not modify the files in pyapsuite
and expect it to be included in the output. These files are not guarenteed to be up to date.
If Cameca.CustomAnalysis.PythonCore is updated and these appear to be out of date, replace them with the latest versions found at:
https://github.com/CamecaAPT/cameca-customanalysis-pythoncore/tree/main/Cameca.CustomAnalysis.PythonCore/PythonModules/pyapsuite