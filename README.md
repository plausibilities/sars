## SARS

In progress

<br>
<br>
<br>
<br>

## Development Notes

### Environment

The environment

```
conda create --prefix ~/Anaconda3/envs/uncertainty
```

The installations are

```bash
conda install -c anaconda pymc3 # installs: python, theano, arviz, numpy, pandas
conda install -c anaconda seaborn # installs: matplotlib
conda install -c anaconda python-graphviz # installs: graphviz
conda install -c anaconda pywin32 jupyterlab nodejs # installs: requests, urllib3
pip install dotmap


# For norms & testing
conda install -c anaconda pytest coverage pylint pytest-cov

# Upgrading PyMC3
pip install --upgrade pymc3==3.9.3

```

### Requirements

For project *sars*

```bash
conda activate uncertainty
pip freeze -r docs/filter.txt > requirements.txt
```

and

```bash
pylint --generate-rcfile > .pylintrc
```
