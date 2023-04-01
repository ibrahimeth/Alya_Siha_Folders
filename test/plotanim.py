import plotly.graph_objects as go
import plotly.express as ex
fig = go.Figure()

fig.add_trace(go.Indicator(
    value = 200,
    delta = {'reference': 160},
    gauge = {
        'axis': {'visible': False}},
    domain = {'row': 0, 'column': 0}))

fig.add_trace(go.Indicator(
    value = 120,
    gauge = {
        'shape': "bullet",
        'axis' : {'visible': False}},
    domain = {'x': [0.05, 0.5], 'y': [0.15, 0.35]}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = 300,
    domain = {'row': 0, 'column': 1}))

fig.add_trace(go.Indicator(
    mode = "delta",
    value = 40,
    domain = {'row': 1, 'column': 1}))

fig.update_layout(
    grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
    template = {'data' : {'indicator': [{
        'title': {'text': "Speed"},
        'mode' : "number+delta+gauge",
        'delta' : {'reference': 90}}]
                         }})

fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 450,
    title = {'text': "Speed"},
    domain = {'x': [0, 1], 'y': [0, 1]}
))
# x = [0, 1]
# y = [0, 1]

# ax = ex.line(x,y)
# ax.show()
# fig.show()

#!/usr/bin/python3
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import plotly.express as px


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button = QtWidgets.QPushButton('Plot', self)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        fig = go.Figure(go.Indicator(
            domain={'x': [0, 1], 'y': [0, 1]},
            value=450,
            mode="gauge+number+delta",
            title={'text': "Speed"},
            delta={'reference': 380},
            gauge={'axis': {'range': [None, 500]},
                'steps': [
                    {'range': [0, 250], 'color': "lightgray"},
                    {'range': [250, 400], 'color': "gray"}],
                    'threshold': {'line': {'color': "red", 'width': 100}, 'thickness': 0.75, 'value': 490}
                }))

        fig.update_layout(paper_bgcolor = "rgb(0,0,0)")
        df = px.data.tips()
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.exec()
