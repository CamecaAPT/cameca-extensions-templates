using System;
using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;
using Prism.Ioc;
using Prism.Modularity;

namespace CustomAnalysisTemplate;

public class CustomAnalysisTemplateModule : IModule
{
    public void RegisterTypes(IContainerRegistry containerRegistry)
    {
        containerRegistry.AddCustomAnalysisUtilities(options => options.UseStandardBaseClasses = true);

        containerRegistry.Register<object, CustomAnalysisTemplateNode>(CustomAnalysisTemplateNode.UniqueId);
        containerRegistry.RegisterInstance(CustomAnalysisTemplateNode.DisplayInfo, CustomAnalysisTemplateNode.UniqueId);
        containerRegistry.Register<IAnalysisMenuFactory, CustomAnalysisTemplateNodeMenuFactory>(nameof(CustomAnalysisTemplateNodeMenuFactory));
        containerRegistry.Register<object, CustomAnalysisTemplateViewModel>(CustomAnalysisTemplateViewModel.UniqueId);
    }

    public void OnInitialized(IContainerProvider containerProvider)
    {
        var extensionRegistry = containerProvider.Resolve<IExtensionRegistry>();
        extensionRegistry.RegisterAnalysisView<CustomAnalysisTemplateView, CustomAnalysisTemplateViewModel>(AnalysisViewLocation.Default);
    }
}
