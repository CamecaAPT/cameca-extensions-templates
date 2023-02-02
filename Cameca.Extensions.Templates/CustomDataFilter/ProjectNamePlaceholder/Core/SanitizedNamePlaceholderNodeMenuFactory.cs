using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;
using Prism.Events;

namespace ProjectNamePlaceholder.Core;

internal class SanitizedNamePlaceholderNodeMenuFactory : AnalysisMenuFactoryBase
{
    public SanitizedNamePlaceholderNodeMenuFactory(IEventAggregator eventAggregator)
        : base(eventAggregator)
    {
    }

    protected override INodeDisplayInfo DisplayInfo => SanitizedNamePlaceholderNode.DisplayInfo;
    protected override string NodeUniqueId => SanitizedNamePlaceholderNode.UniqueId;
    public override AnalysisMenuLocation Location { get; } = AnalysisMenuLocation.DataFilter;
}