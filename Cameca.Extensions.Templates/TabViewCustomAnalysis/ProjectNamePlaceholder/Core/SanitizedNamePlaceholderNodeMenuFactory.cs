using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities.Legacy;
using Prism.Events;
using Prism.Services.Dialogs;

namespace ProjectNamePlaceholder.Core;

internal class SanitizedNamePlaceholderNodeMenuFactory : LegacyAnalysisMenuFactoryBase
{
    public SanitizedNamePlaceholderNodeMenuFactory(IEventAggregator eventAggregator, IDialogService dialogService)
        : base(eventAggregator, dialogService)
    {
    }

    protected override INodeDisplayInfo DisplayInfo => SanitizedNamePlaceholderNode.DisplayInfo;
    protected override string NodeUniqueId => SanitizedNamePlaceholderNode.UniqueId;
    public override AnalysisMenuLocation Location { get; } = AnalysisMenuLocation.Analysis;
}