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
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Prism.Ioc;
using Python.Runtime;
using System.ComponentModel;

namespace ProjectNamePlaceholder.Core;

[DefaultView(SanitizedNamePlaceholderViewModel.UniqueId, typeof(SanitizedNamePlaceholderViewModel))]
[NodeType(NodeType.DataFilter)]
[ObservableObject]
internal partial class SanitizedNamePlaceholderNode : StandardAnalysisNodeBase
{
    // This must be a unique Python module per extension, so using the module name should generally be safe
    // If there is a conflict with calling a different module, this name can be changed
    private const string EntryModuleName = "SanitizedNamePlaceholderModule";
    private const string EntryFunctionName = "main";

    private readonly IPyExecutor pyExecutor;
    private readonly INodeDataFilterProvider nodeDataFilterProvider;
    private readonly IContainerProvider containerProvider;

    public const string UniqueId = "ProjectNamePlaceholder.Core.SanitizedNamePlaceholderNode";

    public static INodeDisplayInfo DisplayInfo { get; } = new NodeDisplayInfo("DisplayNamePlaceholder");

    public AsyncRelayCommand RunScriptCommand { get; }
    public RelayCommand CancelScriptCommand { get; }
    public RelayCommand ClearOutputCommand { get; }

    private bool isClearOnRun = true;
    public bool IsClearOnRun
    {
        get => isClearOnRun;
        set => SetProperty(ref isClearOnRun, value);
    }

    public SanitizedNamePlaceholderNode(IPyExecutor pyExecutor, IContainerProvider containerProvider, IStandardAnalysisNodeBaseServices services, INodeDataFilterProvider nodeDataFilterProvider) : base(services)
    {
        this.pyExecutor = pyExecutor;
        this.nodeDataFilterProvider = nodeDataFilterProvider;
        this.containerProvider = containerProvider;

        RunScriptCommand = new AsyncRelayCommand(OnRunScript);
        CancelScriptCommand = new RelayCommand(RunScriptCommand.Cancel);
        ClearOutputCommand = new RelayCommand(ClearOutput);
    }

    protected override void OnAdded(NodeAddedEventArgs eventArgs)
    {
        if (nodeDataFilterProvider.Resolve(InstanceId) is { } nodeDataFilter)
        {
            nodeDataFilter.FilterDelegate = FilterDelegate;
        }
    }

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
                        DispatchAddOutputItem(loadState.Output);
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

    private void OnPropertiesChanged(object? sender, PropertyChangedEventArgs e)
    {
        DataStateIsValid = false;
    }

    protected override byte[]? GetSaveContent()
    {
        var serializedState = JsonSerializer.Serialize(new SanitizedNamePlaceholderSaveState
        {
            Output = string.Join("", OutputItems),
            Properties = Properties as SanitizedNamePlaceholderProperties
        });
        return Encoding.UTF8.GetBytes(serializedState);
    }

    protected async IAsyncEnumerable<ReadOnlyMemory<ulong>> FilterDelegate(IIonData ownerIonData, IProgress<double>? progress, [EnumeratorCancellation] CancellationToken token)
    {
        var captureMiddleware = new CaptureFilterIndices();
        await ExecutePython(new[] { captureMiddleware }, token);
        if (!captureMiddleware.HasResult)
        {
            yield return Array.Empty<ulong>();
            yield break;
        }

        foreach (var chunkIndices in captureMiddleware.Value ?? Enumerable.Empty<ReadOnlyMemory<ulong>>())
        {
            yield return chunkIndices;
        }
    }

    private void DispatchAddOutputItemPyCallback(object? value)
    {
        DispatchAddOutputItem(value?.ToString() ?? "");
    }

    private void ClearOutput()
    {
        Application.Current.Dispatcher.BeginInvoke(() =>
        {
            lock (outputItemsLock)
            {
                OutputItems.Clear();
            }
        });
    }

    /// <summary>
    /// Collection of strings from redirected stdout and stderr.
    /// Collection is used to support appending text instead of rebuilding immutable single string.
    /// This allows for updates to the displayed without replacement. Text can be selected while more
    /// is added at the same time.
    /// </summary>
    public ObservableCollection<string> OutputItems { get; } = new();


    private readonly object outputItemsLock = new();

    public void DispatchAddOutputItem(string value)
    {
        Application.Current.Dispatcher.BeginInvoke(() =>
        {
            lock (outputItemsLock)
            {
                OutputItems.Add(value);
            }
        });
    }

    private async Task OnRunScript(CancellationToken token)
    {
        try
        {
            await ExecutePython(Array.Empty<IPyExecutorMiddleware>(), token);
        }
        catch (PythonException)
        {
            // Expected when internal Python exception is raised
        }
    }

    public async Task ExecutePython(IEnumerable<IPyExecutorMiddleware> middleware, CancellationToken token)
    {
        if (IsClearOnRun)
        {
            ClearOutputCommand.Execute(null);
        }
        IIonData? ionData;
        try
        {
            ionData = await Services.IonDataProvider.GetOwnerIonData(InstanceId, cancellationToken: token);
            if (ionData is null)
            {
                return;
            }
        }
        catch (TaskCanceledException)
        {
            // Expected on cancellation
            DataStateIsValid = false;
            return;
        }

        var context = new APSuiteContextProvider(
            ionData,
            containerProvider,
            InstanceId);
        var entryFunction = new EntryFunctionDefinition(new[]
            {
                new ParameterDefinition("context", context),
            },
            functionName: EntryFunctionName);
        var executableModule = new LocalModuleExecutable(EntryModuleName, entryFunction);

        middleware = middleware.Concat(new IPyExecutorMiddleware[]
        {
            new StdstreamRedirect(DispatchAddOutputItemPyCallback),
        });

        DataStateIsValid = await pyExecutor.ExecuteAndPrintExceptions(executableModule, middleware, token); ;
    }
}