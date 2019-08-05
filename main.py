from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.core.properties import value
from bokeh.io import export_svgs
import csv
import math

def m_m_c_latency(c, arrival, service):
    utilization = arrival / (c * service)
    Erlang_value = 1 / (1 + (1 - utilization) * (math.factorial(c) / (c * utilization) ** c) * sum([(c * utilization) ** k / math.factorial(k) for k in range(c)]))
    
    return Erlang_value / (c * service - arrival) + 1 / service
     
    
if __name__ == "__main__":
    # prepare some data
    c = 2
    x = [i for i in range(1,100, 5)]
    y_m_m_1 = [m_m_c_latency(1, i/4, 100) for i in x]
    y_m_m_2 = [m_m_c_latency(2, i/2, 100) for i in x]
    y_m_m_4 = [m_m_c_latency(4, i, 100) for i in x]

    # Graphic Design in Bokeh

    # create a new plot with a title and axis labels

    TOOLTIPS = [
            ("index", "$index"),
            ("traffic", "$x"),
            ("cost", "$y"),
        ]

    p = figure(plot_width=600, plot_height=400, x_axis_label='Arrival Traffic (mb/s)', y_axis_label='Latency (sec)', tooltips=TOOLTIPS)

    # Default
    p.line(x, y_m_m_1, legend="M/M/1", line_width=2, line_color="red")
    p.line(x, y_m_m_2, legend="M/M/2", line_width=1, line_color="tomato")
    p.line(x, y_m_m_4, legend="M/M/4", line_width=1, line_color="orange")

    p.circle(x, y_m_m_1, legend="M/M/1", fill_color="red", line_color="red", size=7)
    p.x(x, y_m_m_2, legend="M/M/2", line_color="tomato", size=5)
    p.circle(x, y_m_m_4, legend="M/M/4", fill_color="white", line_color="orange", size=5)

    p.xaxis.axis_label_text_font_size = "15pt"
    p.yaxis.axis_label_text_font_size = "15pt"
    p.xaxis.major_label_text_font_size = "12pt"
    p.yaxis.major_label_text_font_size = "12pt"
    p.legend.location = "top_left"

    p.output_backend = "svg"
    export_svgs(p, filename="m_m_c_or_1.svg")

    with open('csv/m_m_c_or_1.csv', 'w', newline='') as csvfile:

        # space for delimiter
        writer = csv.writer(csvfile, delimiter=' ')

        writer.writerow(['Servers Number', 'M/M/1', 'M/M/2', 'M/M/4'])
        # writer.writerow(['Traffic', 'Total Cost of One Server Each Edge', 'Total Cost of Three Server Each Edge', 'Total Cost of Five Server Each Edge'])
        
        for i in range(len(x)):
            writer.writerow([x[i], y_m_m_1[i], y_m_m_2, y_m_m_4])
            # writer.writerow([xaxis_list[i], total_1_list[i], total_3_list[i], total_5_list[i]])