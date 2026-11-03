# 2nd OpenFOAM HPC Challenge (OHC-2)

This repository contains the data, scripts and notebooks that were used to analyze the results of the 2nd OpenFOAM HPC Challenge (OHC-2). The results were presented at the OHC-2 mini-symposium, held July 1-2, 2026 in Guimarães, Portugal as part of the 21st OpenFOAM Workshop.

<!-- TODO(OHC-2): add Zenodo DOI badge and any other release details once available. -->

## OHC-2 Overview
The challenge was aimed at evaluating the efficiency, scalability, and performance of OpenFOAM on various hardware platforms, with and without software enhancements, using a standardized industrial test case (DrivAer). The challenge included two tracks:
  - **Hardware Track:** Participants simulated the case using standard (unmodified) OpenFOAM v2512, on any supported hardware.
  - **Software Track:** Participants could use custom solvers and code optimizations, provided the mesh and physical modeling correspond to the original setup.

A detailed description of the challenge is provided in the [introductory presentation](OHC-2_Introduction.pdf).
<!-- TODO(OHC-2): add link to the OHC-2 manuscript once published. -->

## DrivAer Case
The challenge focused on simulation of external flow over a static version of the DrivAer automotive model. The model consists of a full car geometry, with closed coolings and a complex underbody, without considering wheel rotation. A detailed description of the test case may be found in the repository[^DrivAerCase] of the HPC Technical Committee.

## Data Analysis
Submissions were originally given in the form of Excel files. These files were parsed with [python utilities](OHCParser.py), and the results were visualized in a set of Jupyter notebooks.
Several metrics of interest (time-to-solution, energy-to-solution, FVOPS, etc) were analyzed. See the HPC TC repository[^HPCTC] for a detailed description of the metrics.

## OHC-DATA
The results of all OHC rounds are also collected in [OHC-DATA](https://github.com/OpenFOAM-HPC-Challenge/OHC-DATA), a single dataset that also includes results submitted after the workshops. This repository holds the OHC-2 data as it was analyzed for the workshop, so individual values in OHC-DATA may differ where results were added or corrected later. OHC-DATA also provides the scripts to run the benchmark and to contribute new results.

## Repository Structure

- [OHC-2_Introduction.pdf](OHC-2_Introduction.pdf): Full challenge description, rules, metrics, and data submission guidelines.
- [OHC-2_HW-track.pdf](OHC-2_HW-track.pdf): Summary of hardware track analysis (presentation)
- [OHC-2_SW-track.pdf](OHC-2_SW-track.pdf): Summary of software track analysis (presentation)
- [Overview.ipynb](Overview.ipynb): Jupyter notebook producing submission statistics
- [HWTrack.ipynb](HWTrack.ipynb): Jupyter notebook used to analyse hardware track submissions
- [SWTrack.ipynb](SWTrack.ipynb): Jupyter notebook used to analyse software track submissions
- [Interactive.ipynb](Interactive.ipynb): Jupyter notebook providing an interactive plot for custom data analysis, [click for demonstration](https://colab.research.google.com/drive/1adJGbMC4VwWhiD31JNCRvXBWWno_dYxF?usp=sharing)
- [OHCParser.py](OHCParser.py): Data parsing and metric calculation utilities
- [data_OHC1.json](data_OHC1.json): The OHC-1 submissions, exported from the previous edition's parse (the OHC-1 spreadsheets are not part of this repository)
- [data_OHC2.json](data_OHC2.json): JSON file produced from the raw xls submissions (used to accelerate data loading in the Interactive.ipynb notebook)
- [submissions](submissions): Raw submissions (excel sheets, logs, input files, etc)
- [presentations](presentations): Participant presentations
- [requirements.txt](requirements.txt): Python packages needed to run the notebooks

## Getting Started

- If this is your first encounter with OHC, please start by reading [OHC-2_Introduction.pdf](OHC-2_Introduction.pdf), to get familiar with the challenge aims and scope.

- If you're interested in the main conclusions and analysis presented in the workshop, please see [OHC-2_HW-track.pdf](OHC-2_HW-track.pdf) and [OHC-2_SW-track.pdf](OHC-2_SW-track.pdf), for the hardware and software tracks, respectively.

- If you would like to dive deeper into the data analysis that was done as part of the workshop, please see the individual Jupyter notebooks in the main folder (best viewed from within VS code). The notebooks are known to work with python 3.12. Install the environment with `pip install -r requirements.txt` and run the notebooks from the repository root. They also run on Python 3.14 with current package versions (e.g. pandas 3.0, matplotlib 3.11); the pinned versions in `requirements.txt` do not install on 3.14, so install the same packages without the version pins there.

- Finally, if you wish to conduct custom analysis of the data, it is recommended to use [Interactive.ipynb](Interactive.ipynb) (best viewed from within VS code).

- If you want to run the benchmark on your own hardware and contribute the results, see [OHC-DATA](https://github.com/OpenFOAM-HPC-Challenge/OHC-DATA).

## Working with Jupytext

Every notebook is paired with a plain Python script in
[Jupytext](https://jupytext.readthedocs.io) percent format (`# %%` marks a cell).
Develop in whichever side you prefer — both are editable — but **the `.py` file
is the source of truth when diffing and reviewing**, because notebook diffs are
dominated by re-encoded output blobs. During the development it's OK to commit only the `.py` file.  When the analysis is finalised, the clean populated `.ipynb` notebook should be committed as well.

### Setup in bash
```bash
jupytext --sync HWTrack.py                             # propagate after editing either side
jupytext --set-formats ipynb,py:percent <notebook>     # pair a notebook that is not paired yet
```

`--sync` picks the direction by modification time, so sync before switching
sides. Note that a `.py` produced by a bare `jupytext --to py` is only a one-way
export: without the pairing metadata that `--set-formats` writes, the two files
drift apart silently.

### Setup in VS Code
Install the **Jupytext Sync** extension along with the Python and Jupyter
extensions — it keeps the pair in sync on save, so the commands above are only
needed outside the editor. Make sure that the files are paired via the
appropriate commands of the extension. Select the same interpreter for the
workspace and for the notebook kernel, otherwise the two views resolve imports
differently.

Edits to [OHCParser.py](OHCParser.py) are not picked up by a running kernel; add
`%load_ext autoreload` and `%autoreload 2` before the imports, or reload with
`importlib.reload(op)`.

## License
### Source Code
The source code of the parser and the Jupyter notebooks is licensed under the MIT license.

### Submissions Data
All submissions data (folder "submissions") is licensed under CC BY 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0/. For citation, we suggest to provide a link to this repository.

### Presentations
The presentations (folder "presentations") are not covered by any specific license. For further guidance, please reach out to the respective author.

## Questions/Comments

If you have any questions regarding the data, or comments that may help us better prepare for the next occasion of OHC, please feel free to post an issue or contact us at hpc-tc-group@googlegroups.com.

## Citation

Please cite this repo as
``` bibtex
@dataset{ohc2,
  author       = {Lesnik, Sergey and
                  Olenik, Gregor and
                  Wasserman, Mark},
  title        = {2nd OpenFOAM HPC Challenge},
  year         = 2026,
  publisher    = {Zenodo},
  note         = {DOI to be assigned},
}
```
<!-- TODO(OHC-2): update author list, year, and add the Zenodo DOI/url once the OHC-2 dataset is published. -->

[^DrivAerCase]: https://develop.openfoam.com/committees/hpc/-/tree/develop/incompressible/simpleFoam/occDrivAerStaticMesh
[^HPCTC]: https://develop.openfoam.com/committees/hpc#key-performance-indicators
