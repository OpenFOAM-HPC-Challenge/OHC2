# Working in this repository

Data, scripts and notebooks for the 2nd OpenFOAM HPC Challenge. The deliverable is
a citable dataset, so reproducibility matters more than elegance.

## Environment

Use **Python 3.12** and the pinned `requirements.txt`. Newer interpreters fail in
matplotlib's deepcopy path with `RecursionError`, which looks like a bug in the
notebooks but is not.

```bash
uv venv --python 3.12 .venv && uv pip install -r requirements.txt
MPLBACKEND=Agg python SWTrack.py   # headless smoke test
```

Run everything from the repository root; all data paths are relative to it.

## Never re-derive the challenge edition

`OHCParser.read_submissions_all_editions()` already sets an `Edition` column
(`"OHC1"` / `"OHC2"`). Use it. Contributor IDs and filename prefixes do **not**
encode the edition, and heuristics based on them silently match zero rows, so
plots come out empty instead of failing loudly.

```python
# BAD - matches nothing; IDs are "01".."20", filenames start with "NN_"
dfs["Edition"] = "OHC1"
dfs.loc[dfs["Contributor ID"] == "OHC2", "Edition"] = "OHC2"
df = dfs[dfs["File Name"].str.startswith("OHC2")]

# GOOD
df = dfs[dfs["Edition"] == "OHC2"]
```

## `Contributor ID` is not a stable type

Two traps, both of which produce wrong results rather than errors:

- IDs are **not unique across editions** — `10` and `15` exist in both OHC-1 and
  OHC-2 and refer to different people. Filter by `Edition` before grouping on them.
- The spreadsheet parser yields zero-padded strings (`"06"`), but `pd.read_json`
  turns them back into integers (`6`). Since
  `read_submissions_all_editions()` concatenates JSON-loaded OHC-1 rows with
  freshly parsed OHC-2 rows, the combined column mixes `int` and `str`. Sorting or
  comparing it then raises `TypeError: '<' not supported between instances of ...`.

Normalise before any sort, join or groupby on this column:

```python
df["Contributor ID"] = df["Contributor ID"].astype(str).str.zfill(2)
```

## Submission files

`submissions/` holds `.xlsm` files named `NN_<description> <Author>.xlsm`. Never
hardcode a submission filename — they have been renamed once already and broke
four call sites. Select by a data column (`Contributor ID`, `Contributor
Affiliation`) instead.

After any change to `OHCParser.py`, confirm the published JSON still reproduces:

```python
import OHCParser as op, pandas as pd

key = ["File Name", "Mesh", "Number of Nodes", "Number of CPU Cores"]

def norm(df):
    df = df.copy()
    df["Contributor ID"] = df["Contributor ID"].astype(str).str.zfill(2)
    return df.sort_values(key).reset_index(drop=True)

pd.testing.assert_frame_equal(
    norm(op.derive_metrics(op.read_submissions())),
    norm(pd.read_json("data_OHC2.json")),
    check_like=True, check_dtype=False,
)
```

## Notebooks and paired scripts

Every notebook is paired with a `.py` in jupytext percent format, and **the `.py`
is the source of truth**. Edit either side, then `jupytext --sync <name>.py`
before committing so the two cannot drift.

When committing a populated `.ipynb`, re-run it top to bottom first. Do not commit
notebooks containing error tracebacks or out-of-order execution counts — several
already do, and they are indistinguishable from genuine analysis failures.

## Figures

`op.save_fig` names must be unique within a `fig_folder`; duplicates overwrite each
other silently. Generated `figures_*/` directories are gitignored — never commit them.

## Licensing

Code is MIT, `submissions/` is CC BY 4.0, and `presentations/` is unlicensed and
owned by the respective authors. Keep `LICENSE`, `submissions/LICENSE`,
`CITATION.cff` and the README license section consistent when any of them changes.
