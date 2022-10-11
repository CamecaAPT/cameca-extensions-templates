using System;
using Cameca.CustomAnalysis.Utilities;
using Cameca.CustomAnalysis.Utilities.Legacy;

namespace CustomAnalysisTemplate.Core;

internal class CustomAnalysisTemplateViewModel
    : LegacyCustomAnalysisViewModelBase<CustomAnalysisTemplateNode, CustomAnalysisTemplateAnalysis, CustomAnalysisTemplateOptions>
{
    public const string UniqueId = "CustomAnalysisTemplate.CustomAnalysisTemplateViewModel";

    public CustomAnalysisTemplateViewModel(IAnalysisViewModelBaseServices services, Func<IViewBuilder> viewBuilderFactory)
        : base(services, viewBuilderFactory)
    {
    }
}