using Cameca.CustomAnalysis.Utilities;

namespace ProjectNamePlaceholder;

internal class SanitizedNamePlaceholderViewModel : AnalysisViewModelBase<SanitizedNamePlaceholderNode>
{
    public const string UniqueId = "ProjectNamePlaceholder.SanitizedNamePlaceholderViewModel";

    public SanitizedNamePlaceholderViewModel(IAnalysisViewModelBaseServices services)
        : base(services)
    {
    }
}