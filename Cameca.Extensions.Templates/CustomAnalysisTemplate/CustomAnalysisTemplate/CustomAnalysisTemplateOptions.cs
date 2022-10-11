using Prism.Mvvm;

namespace CustomAnalysisTemplate;

public class CustomAnalysisTemplateOptions : BindableBase
{
    /* Example of a "Bindable" property. Properties of this form will notify the analysis that they have been changed.
    private int count;
    [Display(Name = "My Ion Count")]
    // [Display(AutoGenerateField = false)]  // An example of how to hide the property from the property editor
    public int Count
    {
        get => count;
        set => SetProperty(ref count, value);
    }
    //*/
}