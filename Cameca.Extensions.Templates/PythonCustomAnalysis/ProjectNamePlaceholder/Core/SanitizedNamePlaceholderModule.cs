using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;
using Cameca.CustomAnalysis.PythonCore;
using Prism.Ioc;
using Prism.Modularity;
using System.Reflection;
using System.IO;

namespace ProjectNamePlaceholder.Core;

/// <summary>
/// Public <see cref="IModule"/> implementation is the entry point for AP Suite to discover and configure the custom analysis
/// </summary>
public class SanitizedNamePlaceholderModule : IModule
{
    public void RegisterTypes(IContainerRegistry containerRegistry)
    {
        var envFilePath = Path.Join(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), "environment.yml");
        containerRegistry.RegisterAnacondaDistribution(envFilePath: envFilePath, fallbackToBase: true);

        containerRegistry.AddCustomAnalysisUtilities(options => options.UseStandardBaseClasses = true);

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
