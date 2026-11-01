# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.3
#   kernelspec:
#     display_name: py3.12 (3.12.3)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Prolog

# %%
import pandas as pd
import seaborn as sb
import mplcursors
import matplotlib.pyplot as plt
from ipywidgets import Dropdown, interact, ToggleButton

## The interactive matplotlib widget uses the ipympl (https://matplotlib.org/ipympl/) backend by default.
## The backend may be installed via:
## `pip install ipympl`

# %%
# Load the data from a JSON file produced from the submissions
# This load is significantly faster than parsing the submission sheets
df = pd.read_json("data_OHC2.json")

# all available data
df.columns

# %%
# an example how to filter / select a specific subset of the data
# here only keep fine mesh
# df = df[df["Mesh"] == "fine"]

# %% [markdown]
# # Plot Examples

# %%
fig, ax = plt.subplots()
sb.scatterplot(df,x="Number of CPU Cores", y="Run Wall-Clock Time [s]", hue="CPU Model", style="Mesh", ax=ax)
ax.set(xscale="log", yscale="log", title=" Hardware Track")
sb.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
fig = ax.get_figure()

# %%
fig, ax = plt.subplots()
sb.boxplot(
    df, x="Energy per Iteration [J]", y="CPU Model", hue="CPU Model",
    whis=[0, 100], width=.6, palette="vlag", ax=ax
)
sb.stripplot(df, x="Energy per Iteration [J]", y="CPU Model", size=4, color=".3", ax=ax)


# %% [markdown]
# # Interactive scatter with annotations

# %%
# %matplotlib ipympl
# # %matplotlib widget  # use this if ipympl is not available

# %%
def show_annotation(sel):
    row = df.iloc[sel.index]  # selected row from the dataframe
    sel.annotation.set_text(f"""
CPU: {row['CPU Model']}-{row['CPU Submodel']}
Last-Level Cache: {row['Last-Level Cache']}
Mesh: {row['Mesh']}
Track: {row['Track']}
Software Optimization Category: {row['Software Optimization Category']}
Number of CPU Cores: {row['Number of CPU Cores']}
Number of Nodes: {row['Number of Nodes']}
Time per Iteration: {row['Time per Iteration [s]']} [s]
Energy per Iteration: {row['Energy per Iteration [J]']} [J]
Contributor ID: {row['Contributor ID']}
""")
    sel.annotation.get_bbox_patch().set(fc="lightsalmon", alpha=0.9)

def draw_scatter(x,y,color,logX,logY):
    plt.clf()
    g = sb.scatterplot(df,x=x, y=y, hue=color)
    cursor = mplcursors.cursor([ax.collections[0] for ax in [g]], hover=mplcursors.HoverMode.Transient)
    cursor.connect("add", show_annotation)
    if logX:
        g.set(xscale="log")
    if logY:
        g.set(yscale="log")
    plt.show()

dd1 = Dropdown(options=df.columns, value='Energy-To-Solution [kWh]', description='X-Axis: ')
dd2 = Dropdown(options=df.columns, value='Time-To-Solution [h]', description='Y-Axis: ')
dd3 = Dropdown(options=df.columns, value='Track', description='Color: ')
logX = ToggleButton(value=True, description='Log x-scale')
logY = ToggleButton(value=True, description='Log y-scale')

interact(draw_scatter, x=dd1, y=dd2, color=dd3, logX=logX, logY=logY)


