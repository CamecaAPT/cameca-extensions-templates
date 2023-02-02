using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;
using Cameca.CustomAnalysis.Utilities.Legacy;
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
#pragma warning disable CS0618 // Type or member is obsolete
        containerRegistry.AddCustomAnalysisUtilities(options => options.UseLegacy = true);
#pragma warning restore CS0618 // Type or member is obsolete

        containerRegistry.Register<SanitizedNamePlaceholderAnalysis>();
        containerRegistry.Register<object, SanitizedNamePlaceholderNode>(SanitizedNamePlaceholderNode.UniqueId);
        containerRegistry.RegisterInstance(SanitizedNamePlaceholderNode.DisplayInfo, SanitizedNamePlaceholderNode.UniqueId);
        containerRegistry.Register<IAnalysisMenuFactory, SanitizedNamePlaceholderNodeMenuFactory>(nameof(SanitizedNamePlaceholderNodeMenuFactory));
        containerRegistry.Register<object, SanitizedNamePlaceholderViewModel>(SanitizedNamePlaceholderViewModel.UniqueId);
    }

    public void OnInitialized(IContainerProvider containerProvider)
    {
        var extensionRegistry = containerProvider.Resolve<IExtensionRegistry>();
        extensionRegistry.RegisterAnalysisView<LegacyCustomAnalysisView, SanitizedNamePlaceholderViewModel>(AnalysisViewLocation.Top);
    }
}
