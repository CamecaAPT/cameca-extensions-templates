using System.Collections;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Windows.Controls;
using System.Windows;

namespace ProjectNamePlaceholder.Core.Controls;

internal class AppendingTextBox : TextBox
{
    public static readonly DependencyProperty AppendScrollBehaviorProperty = DependencyProperty.Register(
        nameof(AppendScrollBehavior), typeof(AppendScrollBehavior), typeof(AppendingTextBox), new PropertyMetadata(default(AppendScrollBehavior)));

    public AppendScrollBehavior AppendScrollBehavior
    {
        get => (AppendScrollBehavior)GetValue(AppendScrollBehaviorProperty);
        set => SetValue(AppendScrollBehaviorProperty, value);
    }

    public static readonly DependencyProperty ItemsSourceProperty = DependencyProperty.Register(
        nameof(ItemsSource), typeof(IEnumerable), typeof(AppendingTextBox), new FrameworkPropertyMetadata(default(IEnumerable), FrameworkPropertyMetadataOptions.AffectsRender, PropertyChangedCallback));

    private static void PropertyChangedCallback(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is not AppendingTextBox self) return;
        if (e.OldValue is INotifyCollectionChanged oldNotifier)
        {
            oldNotifier.CollectionChanged -= self.OnCollectionChanged;
        }

        if (e.NewValue is IEnumerable<string> enumerable)
        {
            self.Text = string.Join("", enumerable);
        }

        if (e.NewValue is INotifyCollectionChanged newNotifier)
        {
            newNotifier.CollectionChanged += self.OnCollectionChanged;
        }
    }

    private void OnCollectionChanged(object? sender, NotifyCollectionChangedEventArgs e)
    {
        if (e.Action is NotifyCollectionChangedAction.Reset)
        {
            Text = "";
            return;
        }

        if (e.Action is not NotifyCollectionChangedAction.Add || e.NewItems is null)
        {
            return;
        }

        if (e.NewItems?.GetEnumerator() is not { } enumerator)
            return;

        while (enumerator.MoveNext())
        {
            var wasScrolledToBottom = IsScrolledToBottom();
            if (enumerator.Current is string current)
            {
                AppendText(current);
            }

            if (AppendScrollBehavior is AppendScrollBehavior.AlwaysToBottom || AppendScrollBehavior is AppendScrollBehavior.FollowBottom && wasScrolledToBottom)
            {
                UpdateLayout();
                ScrollToVerticalOffset(double.MaxValue);
            }
        }
    }

    private const double ScrollToBottomTolerance = 10d;

    private bool IsScrolledToBottom() => (VerticalOffset + ViewportHeight) >= (ExtentHeight - ScrollToBottomTolerance);

    public IEnumerable ItemsSource
    {
        get => (IEnumerable)GetValue(ItemsSourceProperty);
        set => SetValue(ItemsSourceProperty, value);
    }
}
