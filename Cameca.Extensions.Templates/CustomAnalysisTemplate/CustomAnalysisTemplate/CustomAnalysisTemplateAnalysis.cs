using Cameca.CustomAnalysis.Interface;
using Cameca.CustomAnalysis.Utilities.Legacy;

namespace CustomAnalysisTemplate;

public class CustomAnalysisTemplateAnalysis : ICustomAnalysis<CustomAnalysisTemplateOptions>
{
    /* Services defined by the Cameca.CustomAnalysis.Interface APS can be injected into the constructor for later use.
    private readonly IIsosurfaceAnalysis analysis;

    public CustomAnalysisTemplateAnalysis(IIsosurfaceAnalysis analysis)
    {
        this.analysis = analysis;
    }
    //*/

    /// <summary>
    /// Main custom analysis execution method.
    /// </summary>
    /// <remarks>
    /// Use <paramref name="ionData"/> as the data source for your calculation.
    /// Configurability in AP Suite can be implemented by creating editable properties in the options object. Access here with <paramref name="options"/>.
    /// Render your results with a variety of charts or tables by passing your final data to <see cref="IViewBuilder"/> methods.
    /// e.g. Create a histogram by calling <see cref="IViewBuilder.AddHistogram2D"/> on <paramref name="viewBuilder"/>
    /// </remarks>
    /// <param name="ionData">Provides access to mass, position, and other ion data.</param>
    /// <param name="options">Configurable options displayed in the property editor.</param>
    /// <param name="viewBuilder">Defines how the result will be represented in AP Suite</param>
    public void Run(IIonData ionData, CustomAnalysisTemplateOptions options, IViewBuilder viewBuilder)
    {
        // TODO: Add custom analysis logic
    }
}