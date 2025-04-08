using Cameca.CustomAnalysis.Utilities;

namespace ProjectNamePlaceholder.Core;

internal class SanitizedNamePlaceholderViewModel : AnalysisViewModelBase<SanitizedNamePlaceholderNode>
{
    public const string UniqueId = "Cameca.CustomAnalysis.SanitizedNamePlaceholder.Core.SanitizedNamePlaceholderViewModel";

    public SanitizedNamePlaceholderNode NodeProxy => Node;

    public SanitizedNamePlaceholderViewModel(IAnalysisViewModelBaseServices services) : base(services)
    {
    }
}
