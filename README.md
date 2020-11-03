# rwPtools

The goal of `rwPtools` is to make it easy to access The Lab’s datasets
and get started with research using the python language.


## What is The Lab?

The Lab is [Robot Wealth’s](https://robotwealth.com/) portal for
collaborative research.

It is organized around **Research Pods,** which contain data, ideas,
research and peer-reviewed edges for a given market question.

For example:

  - in the *Equity Factor Research Pod* we look at the question: "*What
    factors predict the relative performance of stocks in the Russell
    1000 index?"*
  - In the *Global Risk Premia Research Pod* we look at the question:
    “*What is the most effective way to get paid for taking on global
    market risks?*”
    

**The Lab serves three purposes:**

1.  It gets you hands-on with the research effort. As well as
    contributing, you’ll learn a ton in the process.
2.  It scales the research effort by enabling community contribution.
3.  It makes the fruits of that scaled research effort available to the
    entire Robot Wealth community.
    
    
## Install and load

The easiest way to install and load `rwPtools` and its dependencies is
via `pip`:

``` bash
pip install git+https://github.com/RWLab/rwPtools
```

## Quickstart: Set up for working on a Research Pod

After installing and loading `rwPtools`, the quickest way to set up a
session for working on a particular Research Pod is:

### 1\. Authorise to the data library

``` python
from rwptools.auth import authenticate
authenticate()
```
When you call the function you will be taken through an interactive authentication flow, simply pick the email address you've signed up to RobotWealth with

### 2\. List The Lab’s Research Pods

``` python
from rwptools.rwlab_gcs import list_pods
list_pods()
>> ["EquityFactors"]
```

### 3\. Load essential Pod data

This transfers price data from the data library to `path` and returns it.

**IMPORTANT: It overwrites any local object  at `path` with the
Research Pod prices file name.**

Requires that you have authorised to the data library prior.

``` python
from rwptools.rwlab_gcs import get_prices_data_frame

prices = get_prices_data_frame('EquityFactors')
prices.head()
```
This transfers the essential data that you always need to `path` (ohlc,
metadata), overwriting any existing local Pod objects.

Requires that you’ve already authorised to the relevant GCS bucket.

### 4\. See all data objects associated with a Pod

``` python
from rwptools.rwlab_gcs import get_pod_meta
get_pod_meta(pod = "EquityFactors")
{'bucket': 'equity_factors_research_pod',
 'datasets': ['R1000_fundamentals_1d.feather',
  'R1000_metadata.feather',
  'R1000_ohlc_1d.feather'],
 'essentials': 'R1000_ohlc_1d.feather',
 'prices': 'R1000_ohlc_1d.feather'}
```
This outputs a dictionary of all the data objects you can transfer for a Pod.


### 5\. Load specific additional Pod data objects

``` python
from rwptools.rwlab_gcs import transfer_lab_object
transfer_lab_object(pod = "EquityFactors", gcs_object = "R1000_ohlc_1d.feather", path = ".")
```

This transfers a specifc object to `path`, overwriting any existing
local instance of that object.

Requires that you’ve already authorised to the relevant data library
