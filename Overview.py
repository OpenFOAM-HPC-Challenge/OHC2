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
import os
import OHCParser as op
import datetime
import traceback
from scipy.optimize import curve_fit
import pathlib
import matplotlib.pyplot as plt

# %%
dfs = op.read_submissions() # OHC2 only
dfs = op.derive_metrics(dfs)

# Sort columns ans save the DataFrame to a JSON file with pretty printing
# dfs = dfs.reindex(sorted(dfs.columns), axis=1)
# dfs.to_json("data.json", orient="records", lines=False, indent=4)

# %%
df_hardware = dfs[dfs["Track"] == "Hardware Track"]
df_software = dfs[dfs["Track"] == "Software Track"]

fig_folder = "figures_overview"
doSaveFig = False  # Set to True to save figures

# %%
# olympic swimming pool 50m*25m*2m 2.5e6 l water
V = 2.5e6 #l water
cp = 4.184  # kJ / kg⋅K
dT = 80 #K,
rho = 1 #kg/l
# 1kJ = 0.0002778 kWh
e = V * rho * dT * cp * 0.0002778

# %%
dfs.columns

# %% [markdown]
# # Results

# %%
# some statistics
print(f"""
total number of valid entries: {len(dfs)},
hardware track entries {len(df_hardware)},
software track entries {len(df_software)} ,
processesed {len(set(dfs['CPU Family']))} CPU families with {len(set(dfs['CPU Submodel']))} CPU Submodels,
-------------------
break-down by CPU Family: {df_hardware["CPU Family"].value_counts()}
-------------------
max nodes {max(dfs['Number of Nodes'])},
mmax cores {max(dfs['Number of CPU Cores'])},
min wall clc {min(dfs['Run Wall-Clock Time [s]'])},
min time step {min(dfs['Time per Iteration [s]'])},
min energy {min(dfs['Energy-To-Solution [kWh]'])} [kWh],
max energy {max(dfs['Energy-To-Solution [kWh]'])} [kWh],
total reported energy consumption {sum(dfs['Energy-To-Solution [kWh]'])} kWh, bringing {sum(dfs['Energy-To-Solution [kWh]'])/e} olympic swimming pools worth of water to a boil
decomposition methods {set(dfs["Decomposition Method"])},
renumbering methods {set(dfs["Renumbering Method"])}
network {set(dfs["Network Interconnect"])},
""")

# %%
fig, ax = plt.subplots()
sb.scatterplot(dfs, x="Number of Nodes", y="FVOPS", ax=ax)#, hue="Track")
ax.set(xscale="log", yscale="log", title=" Hardware + Software Track")
#sb.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
fig = ax.get_figure()
op.save_fig(fig, fig_folder, "FVOPSAllsubs", doSaveFig)

# %%
fig, ax = plt.subplots()
sb.scatterplot(dfs, x="Number of Nodes", y="FVOPS", hue="Track", ax=ax)
ax.set(xscale="log", yscale="log", title=" Hardware + Software Track")
sb.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
fig = ax.get_figure()
op.save_fig(fig, fig_folder, "FVOPSAllsubsByTrack", doSaveFig)

# %%
fig, ax = plt.subplots()
sb.scatterplot(dfs, x="Number of Nodes", y="FVOPS", hue="Software Optimization Category", style="Track", ax=ax)
ax.set(xscale="log", yscale="log", title=" Hardware + Software Track")
sb.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
fig = ax.get_figure()
op.save_fig(fig, fig_folder, "FVOPSAllsubsByType", doSaveFig)

# %%
fig, ax = plt.subplots()
sb.scatterplot(dfs, x="Number of Nodes", y="Energy per Iteration [J]", hue="Track", ax=ax)
ax.set(xscale="log", yscale="log", title=" Hardware + Software Track")
sb.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
fig = ax.get_figure()
op.save_fig(fig, fig_folder, "FVOPSAllsubsEnergyPerIteration", doSaveFig)


