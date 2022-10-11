using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;
// using Cameca.CustomAnalysis.Utilities.Legacy;
using Prism.Ioc;
using Prism.Modularity;

namespace CustomAnalysisTemplate.Core;

/// <summary>
/// Public <see cref="IModule"/> implementation is the entry point for AP Suite to discover and configure the custom analysis
/// </summary>
public class CustomAnalysisTemplateModule : IModule
{
    public void RegisterTypes(IContainerRegistry containerRegistry)
    {
#pragma warning disable CS0618 // Type or member is obsolete
        containerRegistry.AddCustomAnalysisUtilities(options => options.UseLegacy = true);
#pragma warning restore CS0618 // Type or member is obsolete

        containerRegistry.Register<CustomAnalysisTemplateAnalysis>();
        containerRegistry.Register<object, CustomAnalysisTemplateNode>(CustomAnalysisTemplateNode.UniqueId);
        containerRegistry.RegisterInstance(CustomAnalysisTemplateNode.DisplayInfo, CustomAnalysisTemplateNode.UniqueId);
        containerRegistry.Register<IAnalysisMenuFactory, CustomAnalysisTemplateNodeMenuFactory>(nameof(CustomAnalysisTemplateNodeMenuFactory));
        containerRegistry.Register<object, CustomAnalysisTemplateViewModel>(CustomAnalysisTemplateViewModel.UniqueId);
    }

    public void OnInitialized(IContainerProvider containerProvider)
    {
        var extensionRegistry = containerProvider.Resolve<IExtensionRegistry>();
        extensionRegistry.RegisterAnalysisView<LegacyCustomAnalysisView, CustomAnalysisTemplateViewModel>(AnalysisViewLocation.Top);
    }
}
