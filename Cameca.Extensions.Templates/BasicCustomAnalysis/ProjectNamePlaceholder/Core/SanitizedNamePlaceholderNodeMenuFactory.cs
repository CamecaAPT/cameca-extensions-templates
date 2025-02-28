using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;
using Prism.Events;

namespace ProjectNamePlaceholder;

internal class SanitizedNamePlaceholderMenuFactory : AnalysisMenuFactoryBase
{
    public SanitizedNamePlaceholderMenuFactory(IEventAggregator eventAggregator)
        : base(eventAggregator)
    {
    }

    protected override INodeDisplayInfo DisplayInfo => SanitizedNamePlaceholder.DisplayInfo;
    protected override string NodeUniqueId => SanitizedNamePlaceholder.UniqueId;
    public override AnalysisMenuLocation Location { get; } = AnalysisMenuLocation.Analysis;
}