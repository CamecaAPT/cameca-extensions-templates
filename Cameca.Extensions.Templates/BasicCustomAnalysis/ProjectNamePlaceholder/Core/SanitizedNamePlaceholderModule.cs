﻿using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;
using Prism.Ioc;
using Prism.Modularity;

namespace ProjectNamePlaceholder;

/// <summary>
/// Public <see cref="IModule"/> implementation is the entry point for AP Suite to discover and configure the custom analysis
/// </summary>
public class SanitizedNamePlaceholderModule : IModule
{
    public void RegisterTypes(IContainerRegistry containerRegistry)
    {
        containerRegistry.AddCustomAnalysisUtilities(options => options.UseStandardBaseClasses = true);

        containerRegistry.Register<object, SanitizedNamePlaceholder>(SanitizedNamePlaceholder.UniqueId);
        containerRegistry.RegisterInstance(SanitizedNamePlaceholder.DisplayInfo, SanitizedNamePlaceholder.UniqueId);
        containerRegistry.Register<IAnalysisMenuFactory, SanitizedNamePlaceholderMenuFactory>(nameof(SanitizedNamePlaceholderMenuFactory));
        containerRegistry.Register<object, SanitizedNamePlaceholderViewModel>(SanitizedNamePlaceholderViewModel.UniqueId);
    }

    public void OnInitialized(IContainerProvider containerProvider)
    {
        var extensionRegistry = containerProvider.Resolve<IExtensionRegistry>();

        extensionRegistry.RegisterAnalysisView<SanitizedNamePlaceholderView, SanitizedNamePlaceholderViewModel>(AnalysisViewLocation.Default);
    }
}
