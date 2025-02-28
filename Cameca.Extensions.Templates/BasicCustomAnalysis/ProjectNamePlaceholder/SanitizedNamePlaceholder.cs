using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;
using System.Threading;
using System.Threading.Tasks;

namespace ProjectNamePlaceholder;

[DefaultView(SanitizedNamePlaceholderViewModel.UniqueId, typeof(SanitizedNamePlaceholderViewModel))]
internal partial class SanitizedNamePlaceholder : BasicCustomAnalysisBase<SanitizedNamePlaceholderProperties>
{
    public const string UniqueId = "ProjectNamePlaceholder.SanitizedNamePlaceholder";
    
    public static INodeDisplayInfo DisplayInfo { get; } = new NodeDisplayInfo("DisplayNamePlaceholder");

    public SanitizedNamePlaceholder(IStandardAnalysisFilterNodeBaseServices services, ResourceFactory resourceFactory)
        : base(services, resourceFactory)
    {
    }

    protected override Task<bool> Update(CancellationToken cancellationToken)
    {
        return base.Update(cancellationToken);
    }
}