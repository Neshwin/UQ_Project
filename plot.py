import plotly.graph_objects as go
import plotly.offline as pyo

# Sample data (replace this with your actual data)
import pandas as pd
import numpy as np



fig = go.Figure()
dark_colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)',
               'rgb(214, 39, 40)', 'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
               'rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(188, 189, 34)']

# Create a stacked area plot for each column (except 'demand')
for i, column in enumerate(all_region2_data.columns[1:]):
# Create a stacked area plot for each column (except 'demand')
# for column in all_region2_data.columns[1:]:
    fig.add_trace(go.Scatter(
        x=all_region2_data.index, y=all_region2_data[column],
        # hoverinfo='x+y',
        # mode='lines',
        stackgroup='one',
        name=column,line=dict(width=0.5, color=dark_colors[i])
    ))

# Overlay 'demand' using a line plot
fig.add_trace(go.Scatter(
    x=all_region2_data.index, y=all_region2_data['demand'],
    hoverinfo='x+y',
    mode='lines',
    name='Demand',line=dict(width=2, color='black')
))
fig.update_layout(title_text='Region 2 Balance',
                  title_x=0.5  # Center the title
                  )
# Save the plot offline
pyo.plot(fig, filename='stacked_area_plot_demand_overlay_go.html')


fig = go.Figure()
dark_colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)',
               'rgb(214, 39, 40)', 'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
               'rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(188, 189, 34)']

# Create a stacked area plot for each column (except 'demand')
for i, column in enumerate(all_region1_data.columns[1:]):
# Create a stacked area plot for each column (except 'demand')
# for column in all_region2_data.columns[1:]:
    fig.add_trace(go.Scatter(
        x=all_region1_data.index, y=all_region1_data[column],
        # hoverinfo='x+y',
        # mode='lines',
        stackgroup='one',
        name=column,line=dict(width=0.5, color=dark_colors[i])
    ))

# Overlay 'demand' using a line plot
fig.add_trace(go.Scatter(
    x=all_region1_data.index, y=all_region1_data['demand'],
    hoverinfo='x+y',
    mode='lines',
    name='Demand',line=dict(width=2, color='black')
))
fig.update_layout(title_text='Region 1 Balance',
                  title_x=0.5  # Center the title
                  )
# Save the plot offline
pyo.plot(fig, filename='stacked_area_plot_demand_overlay1_go.html')
