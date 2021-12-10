from plotly import offline
import plotly.graph_objs as go
import pandas as pd

# Read the data
data = pd.read_csv('./fingerprints.csv', header=None)

d = data[0] #website name
x = data[1] #sizes of total incoming packets
y = data[5] #number of incoming packets
z = data[2] #number of packets

xt = []
yt = []
zt = []
data = []

for i in range(0, len(x)):
    if i == len(x) - 1 or d[i] != d[i + 1]:
        data.append(go.Scatter3d(x=xt, y=yt, z=zt, mode='markers', \
            marker=dict(), name=d[i]))

        xt = []
        yt = []
        zt = []
    else:
        xt.append(x[i])
        yt.append(y[i])
        zt.append(z[i])

layout = go.Layout(margin=dict(l=0, r=0, b=0, t=0))

fig = go.Figure(data=data, layout=layout)
offline.plot(fig, filename='graphs/graph2.html', auto_open=False)
print("Graph plotted succesfully, check graphs/graph.html")
