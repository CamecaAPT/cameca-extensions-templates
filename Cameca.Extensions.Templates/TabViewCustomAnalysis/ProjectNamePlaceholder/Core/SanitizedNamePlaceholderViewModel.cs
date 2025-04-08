using System;
using Cameca.CustomAnalysis.Utilities;
using Cameca.CustomAnalysis.Utilities.Legacy;

namespace ProjectNamePlaceholder.Core;

internal class SanitizedNamePlaceholderViewModel
    : LegacyCustomAnalysisViewModelBase<SanitizedNamePlaceholderNode, SanitizedNamePlaceholderAnalysis, SanitizedNamePlaceholderProperties>
{
    public const string UniqueId = "ProjectNamePlaceholder.SanitizedNamePlaceholderViewModel";

    public SanitizedNamePlaceholderViewModel(IAnalysisViewModelBaseServices services, Func<IViewBuilder> viewBuilderFactory)
        : base(services, viewBuilderFactory)
    {
    }
}