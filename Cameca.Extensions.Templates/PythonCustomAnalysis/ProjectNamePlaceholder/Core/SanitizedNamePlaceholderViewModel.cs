using CommunityToolkit.Mvvm.Input;
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using System.Threading;
using System.Windows;
using Cameca.CustomAnalysis.PythonCore;
using Python.Runtime;
using Cameca.CustomAnalysis.Utilities;
using Cameca.CustomAnalysis.Interface;
using System;

namespace ProjectNamePlaceholder.Core;

internal class SanitizedNamePlaceholderViewModel : AnalysisViewModelBase<SanitizedNamePlaceholderNode>
{
    public const string UniqueId = "Cameca.CustomAnalysis.SanitizedNamePlaceholder.Core.SanitizedNamePlaceholderViewModel";

    public SanitizedNamePlaceholderNode NodeProxy => Node;

    public SanitizedNamePlaceholderViewModel(IAnalysisViewModelBaseServices services) : base(services)
    {
    }
}
