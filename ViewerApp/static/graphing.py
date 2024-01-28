from datetime import datetime, timedelta
import plotly.graph_objects as go
from collections import Counter
from dataExtraction import getDevices
from plotly.offline import plot
from flask import Flask, render_template

class Graph():
    def __init__(self, user):
        self.devices = getDevices(user)
        self.timeslots = []
        for key in self.devices:
            self.devices[key] = sorted(self.devices[key],key=lambda x: x.time)
            for ci in self.devices[key]:
                self.timeslots.append(ci.time)
        self.timeslots = Counter(self.timeslots)
        self.timeslots = list(self.timeslots.keys())
     
        self.timeslots.sort() # all unique timeslots for x axis


        self.kwh_g = self.generate_graph(lambda x: x.kwh, "kWh")
        self.treesKilled_g = self.generate_graph(lambda x: x.treesKilled, "Trees Killed")
        self.cost_g = self.generate_graph(lambda x: x.cost, "Cost in Dollars")

        self.kwh_t = self.getTotal(lambda x: x.kwh)
        self.treesKilled_t = self.getTotal(lambda x: x.treesKilled)
        self.cost_t = self.getTotal(lambda x: x.cost)

        
    def generate_graph(self, func, value_name):
        data = []
        for device in self.devices:
            ci_list = self.devices[device]
            ylist = []
            i = 0
            for ci in ci_list:
                ylist.append(func(ci)) 
                """
                print(ci.time)
                print(self.timeslots[i])

                while ci.time != self.timeslots[i]:
                    ylist.append(None)
                    i += 1
                           
                i += 1
                """
            data.append(go.Scatter(x=self.timeslots, y=ylist, mode='lines', name=device))
        fig = go.Figure(data=data)
        fig.update_layout(title='', xaxis_title='Time', yaxis_title=value_name)
        graph_html = plot(fig, output_type='div', include_plotlyjs=False)

        return render_template('graphing.html', graph_html=graph_html)
    
    def getTotal(self, func):
        total = 0
        for device in self.devices:
            for ci in self.devices[device]:
                total += func(ci)
        return total