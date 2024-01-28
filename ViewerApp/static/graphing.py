from datetime import datetime, timedelta
import plotly.graph_objects as go

def getGraphHtml(user):
    devices = getDeviceIDs(user)
    times_lists = []
    energy_lists = []
    for device in devices:
        times_lists.append(getTimes(device))
    
    min_time =  times_lists[0][0]
    max_time = times_lists[0][len(times_lists[0]) - 1]
    for times in times_lists:
        min_time = min(min_time, times[0])
        max_time = max(max_time, times[len(times) - 1])
    
    energy_lists.append(getTimes(device))

    current_time =  min_time
    time_intervals = []
    while current_time < max_time:
        time_intervals.append(current_time)
        current_time += timedelta(minutes=5)

    
  
    
def index():
    # Times for the x-axis
    times = [
        datetime(2021, 1, 1, 9, 0),  # 9:00 AM
        datetime(2021, 1, 1, 10, 0), # 10:00 AM
        datetime(2021, 1, 1, 11, 0), # 11:00 AM
        datetime(2021, 1, 1, 12, 0), # 12:00 PM
        datetime(2021, 1, 1, 13, 0)  # 1:00 PM
    ]

    # Y-axis values
    y1 = [2, 3, 4, 5, 6]
    y2 = [1, 4, 7, 10, 13]

    trace1 = go.Scatter(x=times, y=y1, mode='lines', name='First Line')
    trace2 = go.Scatter(x=times, y=y2, mode='lines', name='Second Line')

    fig = go.Figure(data=[trace1, trace2])
    fig.update_layout(title='Plotly Time Series Example',
                      xaxis_title='Time',
                      yaxis_title='Values')

    # Convert the figures to HTML
    graph_html = plot(fig, output_type='div', include_plotlyjs=False)

    return render_template('graphing.html', graph_html=graph_html)

if __name__ == '__main__':
    