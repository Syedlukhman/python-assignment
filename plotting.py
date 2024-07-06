from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import column, row
import numpy as np
import pandas as pd

class Plot:
    def __init__(self, ssd_sums, test_results):
        self.ssd_sums = ssd_sums  # Sum of squared differences for training and ideal functions
        self.test_results = test_results  # Test results data

    def ssd_plot(self, ssd_sums, title):
        # Convert SSD values to logarithmic scale for better visualization
        ssd_log = np.log10(list(ssd_sums.values()))
        min_ssd_value = min(ssd_log)
        
        # Assign colors to the bars: green for the minimum SSD, red for others
        colors = ['green' if ssd == min_ssd_value else 'red' for ssd in ssd_log]
        
        # Create a ColumnDataSource for the SSD data
        ssd_source_log = ColumnDataSource(data=dict(
            ideal_funcs=list(ssd_sums.keys()), 
            ssd=ssd_log, 
            colors=colors
        ))
        
        # Create a bar plot using Bokeh
        p = figure(
            x_range=list(ssd_sums.keys()), 
            title=title, 
            width=700, 
            height=350, 
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )
        
        # Add vertical bars to the plot
        p.vbar(
            x='ideal_funcs', 
            top='ssd', 
            width=0.9, 
            source=ssd_source_log, 
            line_color='white', 
            fill_color='colors'
        )
        
        # Add hover tool to show details on hover
        hover = HoverTool()
        hover.tooltips = [("Ideal Function", "@ideal_funcs"), ("Log10(SSD)", "@ssd{0,0.00}")]
        p.add_tools(hover)
        
        # Rotate x-axis labels for better readability
        p.xaxis.major_label_orientation = "vertical"
        
        return p

    def scatter_test_results(self, df_test_results):
        # Generate random colors for each data point
        np.random.seed(42)
        colors = ['#' + ''.join([np.random.choice(list('0123456789ABCDEF')) for _ in range(6)]) for _ in range(len(df_test_results))]
        df_test_results['color'] = colors
        
        # Create a scatter plot using Bokeh
        p_test = figure(
            title="Test Results Scatter Plot", 
            width=700, 
            height=350, 
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )
        
        # Add scatter points to the plot
        p_test.scatter(
            x='X (test func)', 
            y='Y (test func)', 
            size=10, 
            color='color', 
            alpha=0.7, 
            legend_field='No. of ideal func', 
            source=ColumnDataSource(df_test_results)
        )
        
        # Set legend title
        p_test.legend.title = 'No. of ideal func'
        
        # Add hover tool to show details on hover
        hover_test = HoverTool()
        hover_test.tooltips = [
            ("X (test func)", "@{X (test func)}"), 
            ("Y (test func)", "@{Y (test func)}"), 
            ("Delta Y (test func)", "@{Delta Y (test func)}")
        ]
        p_test.add_tools(hover_test)
        
        return p_test

    def plotting(self):
        # Title for the SSD plots
        title = 'Sum of Squared Differences of Training Functions - Ideal Functions'
        
        # Create SSD plots for each training function
        plots = [self.ssd_plot(self.ssd_sums[key], f"{title} - {key}") for key in self.ssd_sums]
        
        # Convert test results to a DataFrame
        df_test_results = pd.DataFrame(self.test_results)
        
        # Create a scatter plot for the test results
        scatter_plot = self.scatter_test_results(df_test_results)
        
        # Combine all plots into a single layout
        combined_plots = column(row(plots), scatter_plot)
        
        # Output the plots to an HTML file
        output_file('plots.html')
        save(combined_plots)
        
        # Display the plots in a browser
        show(combined_plots)
