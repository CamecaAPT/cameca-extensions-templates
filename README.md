# Cameca.Extensions.Templates

.NET templates for creating extensions for CAMECA AP Suite

## How to install
1. Ensure that the .NET SDK is install (either through Visual Studio Installer or [Microsoft .NET installer website](https://dotnet.microsoft.com/en-us/download/dotnet))
2. Run `dotnet new --install Cameca.Extensions.Templates --nuget-source https://www.myget.org/F/cameca-extensions-dev/api/v3/index.json`

## How to use
1. View installed templates with `dotnet new --list`
2. Select a template to install (e.g. `analysis`)
3. Run `dotnet new analysis --help` to view options for the template
4. Run `dotnet new analysis --name "MyCustomAnalysisName"` along with any additional parameters for the template
5. Implement the custom analysis in the `ICustomAnalysis.Run()` method

| :warning: Visual Studio Support |
|:--------------------------------|
|Templates may or may not be available in the New Project dialog in Visual Studio. Visual Studio 2022 should provide display these templates by default. Visual Studio 2019 may display the templates depending on version, currently selected preview options, and .NET SDK version. If the templates are not available in Visual Studio, extra steps beyond the current scope of these instructions may be necessary to have them appear.|

## Preview Feed
To install templates still in development, use `--nuget-source https://www.myget.org/F/cameca-extensions-dev-preview/api/v3/index.json`

|:warning: WARNING |
|:-----------------|
|Packages from the preview feed are unstable and should be used for development only. All public APIs are subject to change.|
