using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Cameca.CustomAnalysis.Interface.CustomAnalysis;
using Cameca.CustomAnalysis.Interface.IonData;
using Cameca.CustomAnalysis.Interface.View;

namespace CustomAnalysisTemplate
{
    internal class CustomAnalysisTemplateCustomAnalysis : ICustomAnalysis<CustomAnalysisTemplateOptions>
    {
        public IIonData Run(IIonData ionData, IAnalysisTreeNode parentNode, CustomAnalysisTemplateOptions options, IViewBuilder viewBuilder)
        {
            // TODO: Perform custom analysis 

            return ionData;
        }
    }
}
