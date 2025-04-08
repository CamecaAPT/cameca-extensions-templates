using System.ComponentModel.DataAnnotations;
using CommunityToolkit.Mvvm.ComponentModel;

namespace ProjectNamePlaceholder;

public partial class SanitizedNamePlaceholderProperties : ObservableObject
{
    /* Example of a "Bindable" property. Properties of this form will notify the analysis that they have been changed.
    [ObservableProperty]
    [field: Display(Name = "Ion Count", AutoGenerateField = true)]  // AutoGenerateField = false can be used to avoid creating the property in Property controls or Tables
    private int count;
    //*/
}