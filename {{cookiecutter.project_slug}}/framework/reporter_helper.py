import mlflow
from omegaconf import DictConfig, OmegaConf
import config as __reporter_internal_config__
from utils import _get_flat_dict, _process_dict_for_mlflow, _process_value_for_mlflow, _log_params_safely
cfg = __reporter_internal_config__.cfg

def log_config_all(cfg=cfg):
    flat_cfg_dict = _get_flat_dict(cfg)
    params_to_log = _process_dict_for_mlflow(flat_cfg_dict)
    _log_params_safely(params_to_log)

def log_config(name: str, cfg=cfg):
    sentinel = object() 
    value = OmegaConf.select(cfg, name, default=sentinel)
    
    if value is sentinel:
        print(f"[Warning] Key '{name}' not found in config. Skipping logging.")
        return

    if isinstance(value, DictConfig):
        flat_dict = _get_flat_dict(value, prefix=f"{name}.")
        params_to_log = _process_dict_for_mlflow(flat_dict)
        
        _log_params_safely(params_to_log)
        print(f"Successfully logged {len(params_to_log)} nested parameters for '{name}'.")
       
    else:
        processed_value = _process_value_for_mlflow(value)
        mlflow.log_param(name, processed_value)
        print(f"Successfully logged parameter '{name}'.")
