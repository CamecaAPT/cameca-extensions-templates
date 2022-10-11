using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;
using Cameca.CustomAnalysis.Utilities.Legacy;

namespace CustomAnalysisTemplate.Core;

[DefaultView(CustomAnalysisTemplateViewModel.UniqueId, typeof(CustomAnalysisTemplateViewModel))]
internal class CustomAnalysisTemplateNode : LegacyCustomAnalysisNodeBase<CustomAnalysisTemplateAnalysis, CustomAnalysisTemplateOptions>
{
    public const string UniqueId = "CustomAnalysisTemplate.CustomAnalysisTemplateNode";
    
    public static INodeDisplayInfo DisplayInfo { get; } = new NodeDisplayInfo("AnalysisDisplayName");

    public CustomAnalysisTemplateNode(IStandardAnalysisNodeBaseServices services, CustomAnalysisTemplateAnalysis analysis)
        : base(services, analysis)
    {
    }
}