from google.cloud import storage
import pandas as pd

sc = storage.Client(project='rw-algotrader')

def _list_datasets(bucket):
    """Helper function for listing all objects inside a GCS bucket

    Args:
        bucket (str): Name of the bucket

    Returns:
        list: List of strings of objects inside the bucket
    """
    blobs = sc.list_blobs(bucket)
    datasets = [n.name for n in blobs]
    return datasets



def get_pod_meta(pod=None):
    """Gets metadata for rwlab research pods when pod=None returns metadata for all pods 

    Args:
        pod (str, optional): Pod name. Defaults to None.

    Raises:
        Exception: If pod doesn't exists raises exception

    Returns:
        dict: Dictionary of pod metadata
    
    Example:
        get_pod_meta('EquityFactors') 
    """

    pod_meta = {
        'EquityFactors':{
            'bucket':'equity_factors_research_pod',
            'datasets':_list_datasets('equity_factors_research_pod'),
            'essentials':'R1000_ohlc_1d.feather',
            'prices': 'R1000_ohlc_1d.feather'
        },
    }

    if pod is None:
        return pod_meta
    else:
        try:
            return pod_meta[pod]
        except KeyError:
            raise Exception(f"Error! No research pod named {pod}")


def list_pods():
    """Get the names of The Lab's Research Pods


    Returns:
        list: list of names of The Lab's Research Pods

    Example:
        list_pods()
    """
    return list(get_pod_meta().keys())


def transfer_pod_data(pod,path='.'):
    """Transfer all Research Pod data from Google Cloud to disk
    Requires authorisation. Set up prior with `rwlab_gc_auth`

    Args:
        pod (string): The name of the research pod. Options: "Equity Factors" (others TBA)
        path (str, optional): Path to the folder where data will be saved. Defaults to '.'.
    
    Examples:
        rwlab_gc_auth()
        transfer_pod_data("EquityFactors","./data")
    """
    pod_meta = get_pod_meta(pod)
    blobs = sc.list_blobs(pod_meta['bucket'])
    name_blob = {i.name:i for i in blobs}
    for k,v in name_blob.items():
        v.download_to_filename(f'{path}/{k}')
        print(f'{k} Successfully Transferred \n')



def transfer_lab_object(pod,gcs_object,path='.'):
    """Transfer a single object from data library 
    this is useful for reloading specific object rather than transferring all Research Pod objects.

    Args:
        pod (str): Nmae of the Research Pod
        gcs_object (str): Name of the object to transfer
        path (str, optional): Local path for saving object. Defaults to '.'.
    """
    
    pod_meta = get_pod_meta(pod)
    blobs = sc.list_blobs(pod_meta['bucket'])
    name_blob = {i.name:i for i in blobs}

    try:
        name_blob[gcs_object].download_to_filename(f'{path}/{gcs_object}')
        print(f'Successfully downloaded {gcs_object}')
    except KeyError:
        print(f"Error! {gcs_object} does not exist in {pod} research pod")



def get_prices_data_frame(pod,path='.'):
    """Transfers prices data from Research Pod data library and returns it as a pd.DataFrame

    Args:
        pod (str): The name of the Research Pod
        path (str, optional): The path to the local directory to save the transferred data. Defaults to '.'.
    
    Returns:
        pandas.DataFrame: returns prices dataframe from research pod data library 
    Examples:
    quicksetup('EquityFactors')
    prices.head()

    """
    
    pod_meta = get_pod_meta(pod)
    prices_file = pod_meta['prices']

    transfer_lab_object(pod,prices_file,path=path)

    prices = pd.read_feather(f'{path}/{prices_file}')
    prices['date'] = pd.to_datetime(prices['date'])
    
    return prices 

