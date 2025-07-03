using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text.Json;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.PythonCore;
using Cameca.CustomAnalysis.Utilities;
using CommunityToolkit.Mvvm.Input;
using Prism.Ioc;
using Python.Runtime;
using System.ComponentModel;
using ProjectNamePlaceholder.Core;
using Microsoft.Extensions.Logging;
using CommunityToolkit.Mvvm.ComponentModel;
using System.Windows.Input;

namespace ProjectNamePlaceholder;

[DefaultView(SanitizedNamePlaceholderViewModel.UniqueId, typeof(SanitizedNamePlaceholderViewModel))]
//[NodeType(NodeType.Analysis)]
internal partial class SanitizedNamePlaceholder : BasicCustomAnalysisBase<SanitizedNamePlaceholderProperties>
{
    // This must be a unique Python module per extension, so using the module name should generally be safe
    // If there is a conflict with calling a different module, this name can be changed
    private const string EntryModuleName = "SanitizedNamePlaceholderModule";
    private const string EntryFunctionName = "main";
    public const string UniqueId = "ProjectNamePlaceholder.Core.SanitizedNamePlaceholderNode";

    private readonly object outputLock = new();
    private readonly PythonService python;
    private readonly IContainerProvider containerProvider;
    private readonly ILogger<SanitizedNamePlaceholder> logger;

    public static INodeDisplayInfo DisplayInfo { get; } = new NodeDisplayInfo("DisplayNamePlaceholder");

    public ICommand UpdateCancelCommand { get; }

    [ObservableProperty]
    private bool clearOnRun = true;

    /// <summary>
    /// Collection of strings from redirected stdout and stderr.
    /// Collection is used to support appending text instead of rebuilding immutable single string.
    /// This allows for updates to the displayed without replacement. Text can be selected while more
    /// is added at the same time.
    /// </summary>
    public ObservableCollection<string> OutputItems { get; } = new();

    public SanitizedNamePlaceholder(
        IStandardAnalysisFilterNodeBaseServices services,
        ResourceFactory resourceFactory,
        PythonService pythonService,
        IContainerProvider containerProvider,
        ILogger<SanitizedNamePlaceholder> logger)
        : base(services, resourceFactory)
    {
        this.python = pythonService;
        this.containerProvider = containerProvider;
        this.logger = logger;
        UpdateCancelCommand = UpdateCommand.CreateCancelCommand();
    }

    protected override Task<bool> Update(CancellationToken cancellationToken) => ExecuteMainPythonFunction(cancellationToken);

    private void ProcessMainPythonFunctionResults(PyObject? results)
    {
        // TODO: Use return value of the main python function here
    }

    [RelayCommand]
    public void ClearOutput()
    {
        Application.Current.Dispatcher.BeginInvoke(() =>
        {
            lock (outputLock)
            {
                OutputItems.Clear();
            }
        });
    }

    private void OnPropertiesChanged(object? sender, PropertyChangedEventArgs e)
    {
        // Invalidates the analysis when any properties value changes
        // Can be removed if properties do not affect the analysis, or can be made more granular
        // by using PropertyChangedEventArgs.PropertyName to contintionally invalidate based on the changed property
        DataStateIsValid = false;
    }

    /// <summary>
    /// Override GetSaveContent to serialize the properties object, but also to save the diplayed output results
    /// </summary>
    protected override byte[]? GetSaveContent()
    {
        var serializedState = JsonSerializer.Serialize(new SanitizedNamePlaceholderSaveState
        {
            Output = string.Join("", OutputItems),
            Properties = Properties,
        });
        return Encoding.UTF8.GetBytes(serializedState);
    }

    /// <summary>
    /// Override OnCreated to restore the properties object and restore the saved text output when loading the analysis
    /// </summary>
    protected override void OnCreated(NodeCreatedEventArgs eventArgs)
    {
        if (eventArgs is { Trigger: Cameca.CustomAnalysis.Interface.EventTrigger.Load, Data: { } loadData })
        {
            try
            {
                if (JsonSerializer.Deserialize<SanitizedNamePlaceholderSaveState>(loadData) is { } loadState)
                {
                    if (loadState.Output is not null)
                    {
                        WriteToOutput(loadState.Output);
                    }
                    if (loadState.Properties is SanitizedNamePlaceholderProperties loadProperties)
                    {
                        Properties = loadProperties;
                    }
                }
            }
            catch (JsonException) { }
            catch (NotSupportedException) { }
        }
        if (Properties is not SanitizedNamePlaceholderProperties properties)
        {
            properties = new SanitizedNamePlaceholderProperties();
            Properties = properties;
        }
        properties.PropertyChanged += OnPropertiesChanged;
    }

    /// <summary>
    /// Callback wrapping <see cref="WriteToOutput(string)"/> supporting nullable objects to pass to Python StdOut capture
    /// </summary>
    /// <param name="value"></param>
    private void WriteToOutputPyCallback(object? value) => WriteToOutput(value?.ToString() ?? "");

    private void WriteToOutput(string value)
    {
        Application.Current.Dispatcher.BeginInvoke(() =>
        {
            lock (outputLock)
            {
                OutputItems.Add(value);
            }
        });
    }

    private async Task<bool> ExecuteMainPythonFunction(CancellationToken cancellationToken)
    {
        if (ClearOnRun)
        {
            ClearOutput();
        }

        try
        {
            var ionData = await Resources.GetIonData(cancellationToken: cancellationToken);
            if (ionData is null)
            {
                return false;
            }

            // Standard context object exposing application data to Python script
            var context = new APSuiteContextProvider(
                ionData,
                containerProvider,
                Id,
                Resources);

            var results = await python
                .MapPythonFunction(EntryModuleName, EntryFunctionName)
#if DEBUG
                //.SetReloadOnCall(true)
#endif
                .SetStdStreamCallback(WriteToOutputPyCallback)
                .SetParameters(context)
                .Call(cancellationToken);


            ProcessMainPythonFunctionResults(results);
            return true;
        }
        catch (OperationCanceledException)
        {
            // Do nothing
        }
        catch (PythonException pyEx)
        {
            logger.LogError(pyEx, pyEx.Message);
            if (DataState != null)
            {
                DataState.IsErrorState = true;
            }
        }
        return false;
    }
}