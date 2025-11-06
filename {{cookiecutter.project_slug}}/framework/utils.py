# framework/seed_utils.py 
# (シード固定ロジックを別ファイルに切り出すことを推奨)
import random
import numpy as np
import torch
import os
import logging
from omegaconf import OmegaConf
import datetime
import glob
import uuid
from importlib import metadata
import mlflow
from omegaconf import DictConfig, ListConfig, OmegaConf
from typing import Any, Dict


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed) 
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        logging.info(f"Set seed {seed} for random, numpy, torch, and CuDNN.")
    else:
        logging.info(f"Set seed {seed} for random, numpy, and torch (CPU).")

def worker_init_fn(worker_id: int):
    worker_seed = torch.initial_seed() % 2**32
    np.random.seed(worker_seed)
    random.seed(worker_seed)



def register_resolvers():
    # current time resolver
    def get_current_time(format_str: str = "%Y-%m-%d_%H-%M-%S") -> str:
        return datetime.datetime.now().strftime(format_str)
    OmegaConf.register_new_resolver("now", get_current_time, replace=True)

    # current working directory resolver
    OmegaConf.register_new_resolver("cwd", os.getcwd, replace=True)

    # glob resolver
    # Returns a sorted list of file paths matching the given pattern
    def glob_files(pattern: str) -> list[str]:
        return sorted(list(glob.glob(pattern, recursive=True)))
    OmegaConf.register_new_resolver("glob", glob_files, replace=True)

    # uuid resolver
    def get_uuid() -> str:
        return str(uuid.uuid4())
    OmegaConf.register_new_resolver("uuid", get_uuid, replace=True)

    # python package version resolver
    def get_package_version(package_name: str) -> str:
        try:
            return metadata.version(package_name)
        except metadata.PackageNotFoundError:
            return f"{package_name}_not_found"
    OmegaConf.register_new_resolver("version", get_package_version, replace=True)


def _get_flat_dict(cfg: DictConfig, prefix: str = "") -> Dict[str, Any]:
    items: Dict[str, Any] = {}
    for k, v in cfg.items():
        new_key = f"{prefix}{k}" if prefix else k
        
        if isinstance(v, DictConfig):
            items.update(_get_flat_dict(v, prefix=f"{new_key}."))
        else:
            items[new_key] = v     
    return items

def _process_value_for_mlflow(v: Any) -> Any:
    # [ND]もし他にmlflowに記録可能な型があればここに追加
    if isinstance(v, (str, int, float, bool)):
        return v
    if v is None:
        return "None"
    try:
        return OmegaConf.to_yaml(v, resolve=True).strip()
    except:
        return str(v)

def _process_dict_for_mlflow(d: Dict[str, Any]) -> Dict[str, Any]:
    params_to_log = {}
    for k, v in d.items():
        params_to_log[k] = _process_value_for_mlflow(v)
    return params_to_log

def _log_params_safely(params_to_log: Dict[str, Any], tag=False):
    try:
        if tag:
             mlflow.set_tags(params_to_log)
        else:
            mlflow.log_params(params_to_log, bulk_logging=True)       
    except TypeError:
        try:
            if tag:
                mlflow.set_tags(params_to_log)
            else:
                mlflow.log_params(params_to_log)
        except Exception as e_fallback:
            print(f"[Warning] Bulk logging failed: {e_fallback}. Attempting individual logging...")
            count = 0
            for k, v in params_to_log.items():
                try:
                    if tag:
                        mlflow.set_tag(k, v)
                    else:
                        mlflow.log_param(k, v)
                    count += 1
                except Exception as e_individual:
                    print(f"[Error] Failed to log param '{k}' (value: {str(v)[:50]}...): {e_individual}")