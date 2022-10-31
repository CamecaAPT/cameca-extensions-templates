using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Threading;
using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;

namespace ProjectNamePlaceholder;

internal class SanitizedNamePlaceholderNode : DataFilterNodeBase
{
    public const string UniqueId = "ProjectNamePlaceholder.SanitizedNamePlaceholderNode";

    public static INodeDisplayInfo DisplayInfo { get; } = new NodeDisplayInfo("DisplayNamePlaceholder");

    public SanitizedNamePlaceholderNode(IDataFilterNodeBaseServices services) : base(services)
    {
    }

    protected override async IAsyncEnumerable<ReadOnlyMemory<ulong>> GetIndicesDelegate(IIonData ownerIonData, IProgress<double>? progress, [EnumeratorCancellation] CancellationToken token)
    {
        yield break;
    }
}