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
    # x = [2**i for i in range(6)]
    x = [i for i in range(1,20)]
    # y_m_m_c = [m_m_c_latency(i, x[-2]*i/x[-1], 1) for i in x]
    y_m_m_c = [m_m_c_latency(i,90*i, 100) for i in x]

    # Graphic Design in Bokeh

    # create a new plot with a title and axis labels

    TOOLTIPS = [
            ("index", "$index"),
            ("traffic", "$x"),
            ("cost", "$y"),
        ]

    p = figure(plot_width=600, plot_height=400, x_axis_label='Servers Number', y_axis_label='Latency (sec)', tooltips=TOOLTIPS)

    # Default
    p.line(x, y_m_m_c, legend="M/M/c", line_width=2)
    # p.line(xaxis_list, total_normal_list, legend="Normal distribution", line_width=1, line_color="tomato")
    # p.line(xaxis_list, total_fog_CP_list, legend="Fog CP value", line_width=1, line_color="orange")

    p.circle(x, y_m_m_c, legend="M/M/c", size=7)
    # p.x(xaxis_list, total_normal_list, legend="Normal distribution", line_color="tomato", size=5)
    # p.circle(xaxis_list, total_fog_CP_list, legend="Fog CP value", fill_color="white", line_color="orange", size=5)

    # p.line(xaxis_list, total_1_list, legend="One Server Each Edge", line_width=2, line_color="red")
    # p.line(xaxis_list, total_3_list, legend="Three Server Each Edge", line_width=1, line_color="tomato")
    # p.line(xaxis_list, total_5_list, legend="Five Server Each Edge", line_width=1, line_color="orange")

    # p.circle(xaxis_list, total_1_list, legend="One Server Each Edge", fill_color="red", line_color="red", size=7)
    # p.x(xaxis_list, total_3_list, legend="Three Server Each Edge", line_color="tomato", size=5)
    # p.circle(xaxis_list, total_5_list, legend="Five Server Each Edge", fill_color="white", line_color="orange", size=5)

    p.xaxis.axis_label_text_font_size = "15pt"
    p.yaxis.axis_label_text_font_size = "15pt"
    p.xaxis.major_label_text_font_size = "12pt"
    p.yaxis.major_label_text_font_size = "12pt"
    p.legend.location = "top_right"

    p.output_backend = "svg"
    export_svgs(p, filename="server_num.svg")

    with open('csv/server_num.csv', 'w', newline='') as csvfile:

        # space for delimiter
        writer = csv.writer(csvfile, delimiter=' ')

        writer.writerow(['Servers Number', 'Latency'])
        # writer.writerow(['Traffic', 'Total Cost of One Server Each Edge', 'Total Cost of Three Server Each Edge', 'Total Cost of Five Server Each Edge'])
        
        for i in range(len(x)):
            writer.writerow([x[i], y_m_m_c[i]])
            # writer.writerow([xaxis_list[i], total_1_list[i], total_3_list[i], total_5_list[i]])