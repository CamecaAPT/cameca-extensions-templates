using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Cameca.CustomAnalysis.Interface.CustomAnalysis;
using Prism.Ioc;
using Prism.Modularity;

namespace CustomAnalysisTemplate
{
    [ModuleDependency("IvasModule")]
    public class CustomAnalysisTemplateModule : IModule
    {
        public void RegisterTypes(IContainerRegistry containerRegistry)
        {
            // Register any additional dependencies with the Unity IoC container
        }

        public void OnInitialized(IContainerProvider containerProvider)
        {
            var customAnalysisService = containerProvider.Resolve<ICustomAnalysisService>();

            customAnalysisService.Register<CustomAnalysisTemplateCustomAnalysis, CustomAnalysisTemplateOptions>(
                new CustomAnalysisDescription("CustomAnalysisTemplate", "AnalysisDisplayName", new Version()));
        }
    }
}
