using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;

namespace ProjectNamePlaceholder;

[DefaultView(SanitizedNamePlaceholderViewModel.UniqueId, typeof(SanitizedNamePlaceholderViewModel))]
internal class SanitizedNamePlaceholderNode : StandardAnalysisNodeBase
{
    public const string UniqueId = "ProjectNamePlaceholder.SanitizedNamePlaceholderNode";
    
    public static INodeDisplayInfo DisplayInfo { get; } = new NodeDisplayInfo("DisplayNamePlaceholder");

    public SanitizedNamePlaceholderNode(IStandardAnalysisNodeBaseServices services)
        : base(services)
    {
    }
}