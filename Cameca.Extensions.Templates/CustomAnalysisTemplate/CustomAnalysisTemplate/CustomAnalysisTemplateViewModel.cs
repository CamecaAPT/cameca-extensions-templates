using Cameca.CustomAnalysis.Utilities;

namespace CustomAnalysisTemplate;

internal class CustomAnalysisTemplateViewModel : AnalysisViewModelBase<CustomAnalysisTemplateNode>
{
    public const string UniqueId = "CustomAnalysisTemplate.CustomAnalysisTemplateViewModel";

    public CustomAnalysisTemplateViewModel(IAnalysisViewModelBaseServices services) : base(services)
    {
    }
}