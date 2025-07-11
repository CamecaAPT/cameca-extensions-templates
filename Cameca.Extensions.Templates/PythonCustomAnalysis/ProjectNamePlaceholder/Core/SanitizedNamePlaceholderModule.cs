﻿using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;
using Cameca.CustomAnalysis.PythonCore;
using Prism.Ioc;
using Prism.Modularity;

namespace ProjectNamePlaceholder.Core;

/// <summary>
/// Public <see cref="IModule"/> implementation is the entry point for AP Suite to discover and configure the custom analysis
/// </summary>
public class SanitizedNamePlaceholderModule : IModule
{
    public void RegisterTypes(IContainerRegistry containerRegistry)
    {
        containerRegistry.RegisterPythonDistribution();

        containerRegistry.AddCustomAnalysisUtilities(options => options.UseStandardBaseClasses = true);

        containerRegistry.Register<object, SanitizedNamePlaceholder>(SanitizedNamePlaceholder.UniqueId);
        containerRegistry.RegisterInstance(SanitizedNamePlaceholder.DisplayInfo, SanitizedNamePlaceholder.UniqueId);
        containerRegistry.Register<IAnalysisMenuFactory, SanitizedNamePlaceholderNodeMenuFactory>(nameof(SanitizedNamePlaceholderNodeMenuFactory));
        containerRegistry.Register<object, SanitizedNamePlaceholderViewModel>(SanitizedNamePlaceholderViewModel.UniqueId);
    }

    public void OnInitialized(IContainerProvider containerProvider)
    {
        var extensionRegistry = containerProvider.Resolve<IExtensionRegistry>();
        extensionRegistry.RegisterAnalysisView<SanitizedNamePlaceholderView, SanitizedNamePlaceholderViewModel>(AnalysisViewLocation.Bottom);

        containerProvider.InitializePythonDistribution("DisplayNamePlaceholder - Python Options");
    }
}
