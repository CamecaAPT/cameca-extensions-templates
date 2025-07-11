﻿using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;
using Cameca.CustomAnalysis.Utilities.Legacy;

namespace ProjectNamePlaceholder.Core;

[DefaultView(SanitizedNamePlaceholderViewModel.UniqueId, typeof(SanitizedNamePlaceholderViewModel))]
internal class SanitizedNamePlaceholderNode : LegacyCustomAnalysisNodeBase<SanitizedNamePlaceholderAnalysis, SanitizedNamePlaceholderProperties>
{
    public const string UniqueId = "ProjectNamePlaceholder.SanitizedNamePlaceholderNode";
    
    public static INodeDisplayInfo DisplayInfo { get; } = new NodeDisplayInfo("DisplayNamePlaceholder");

    public SanitizedNamePlaceholderNode(IStandardAnalysisNodeBaseServices services, SanitizedNamePlaceholderAnalysis analysis, ResourceFactory resourceFactory)
        : base(services, analysis, resourceFactory)
    {
    }
}