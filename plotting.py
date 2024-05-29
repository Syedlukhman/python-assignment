from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import column, row
import numpy as np
import pandas as pd

class Plot:
    def __init__(self, ssd_sums, test_results):
        self.ssd_sums = ssd_sums
        self.test_results = test_results

    def ssd_plot(self, ssd_sums, title):
        ssd_log = np.log10(list(ssd_sums.values()))
        min_ssd_value = min(ssd_log)
        colors = ['green' if ssd == min_ssd_value else 'red' for ssd in ssd_log]
        ssd_source_log = ColumnDataSource(data=dict(ideal_funcs=list(ssd_sums.keys()), ssd=ssd_log, colors=colors))
        p = figure(x_range=list(ssd_sums.keys()), title=title, width=700, height=350, tools="pan,wheel_zoom,box_zoom,reset,save")
        p.vbar(x='ideal_funcs', top='ssd', width=0.9, source=ssd_source_log, line_color='white', fill_color='colors')
        hover = HoverTool()
        hover.tooltips = [("Ideal Function", "@ideal_funcs"), ("Log10(SSD)", "@ssd{0,0.00}")]
        p.add_tools(hover)
        p.xaxis.major_label_orientation = "vertical"
        return p

    def scatter_test_results(self, df_test_results):
        np.random.seed(42)
        colors = ['#' + ''.join([np.random.choice(list('0123456789ABCDEF')) for _ in range(6)]) for _ in range(len(df_test_results))]
        df_test_results['color'] = colors
        p_test = figure(title="Test Results Scatter Plot", width=700, height=350, tools="pan,wheel_zoom,box_zoom,reset,save")
        p_test.scatter(x='X (test func)', y='Y (test func)', size=10, color='color', alpha=0.7, legend_field='No. of ideal func', source=ColumnDataSource(df_test_results))
        p_test.legend.title = 'No. of ideal func'
        hover_test = HoverTool()
        hover_test.tooltips = [("X (test func)", "@{X (test func)}"), ("Y (test func)", "@{Y (test func)}"), ("Delta Y (test func)", "@{Delta Y (test func)}")]
        p_test.add_tools(hover_test)
        return p_test

    def plotting(self):
        title = 'Sum of Squared Differences of Training Functions - Ideal Functions'
        plots = [self.ssd_plot(self.ssd_sums[key], f"{title} - {key}") for key in self.ssd_sums]
        df_test_results = pd.DataFrame(self.test_results)
        scatter_plot = self.scatter_test_results(df_test_results)
        combined_plots = column(row(plots), scatter_plot)
        output_file('plots.html')
        save(combined_plots)
        show(combined_plots)
