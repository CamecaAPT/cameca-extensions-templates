using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities;

namespace CustomAnalysisTemplate;

[DefaultView(CustomAnalysisTemplateViewModel.UniqueId, typeof(CustomAnalysisTemplateViewModel))]
internal class CustomAnalysisTemplateNode : StandardAnalysisNodeBase
{
    public const string UniqueId = "CustomAnalysisTemplate.CustomAnalysisTemplateNode";
    
    public static INodeDisplayInfo DisplayInfo { get; } = new NodeDisplayInfo("AnalysisDisplayName");

    public CustomAnalysisTemplateNode(IStandardAnalysisNodeBaseServices services) : base(services)
    {
    }
}