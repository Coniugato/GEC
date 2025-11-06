import mlflow
from omegaconf import OmegaConf, DictConfig
import os, socket
from utils import register_resolvers
from utils import _get_flat_dict, _process_dict_for_mlflow, _log_params_safely

register_resolvers()
syscfg_mlflow: DictConfig = OmegaConf.load("sysconf/mlflow_config.yaml")
syscfg_custom: DictConfig = OmegaConf.load("sysconf/custom.yaml")
syscfg_meta: DictConfig = OmegaConf.load("sysconf/meta_config.yaml")
experiment_name = syscfg_mlflow.get("experiment_name")
tracking_uri = syscfg_mlflow.get("tracking_uri")
run_name = syscfg_mlflow.get("run_name", "default_run")
auto_logging_cfg = syscfg_mlflow.get("auto_logging", {})
description = syscfg_meta.get("description", "No description provided.")

def experiment_exists(experiment_name: str) -> bool:
    experiment = mlflow.get_experiment_by_name(experiment_name)
    return experiment is not None

def create_experiment_if_not_exists(experiment_name: str) -> int:
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(experiment_name)
        return experiment_id
    else:
        return experiment.experiment_id
    
def set_experiment():
    mlflow.set_tracking_uri(tracking_uri)
    if not experiment_exists(experiment_name):
        create_experiment_if_not_exists(experiment_name)
    mlflow.set_experiment(experiment_name)

def init_mlflow_run(callname):
    set_experiment()
    system_metrics_enabled = auto_logging_cfg.get("system_metrics", False)
    return mlflow.start_run(run_name=f"{callname}_{run_name}", description=description, log_system_metrics=system_metrics_enabled)


def tag_config_all(cfg):
    flat_cfg_dict = _get_flat_dict(cfg)
    params_to_log = _process_dict_for_mlflow(flat_cfg_dict)
    _log_params_safely(params_to_log, tag=True)

def mlflow_standard_logging():
    dvc_exp_name = os.environ.get("DVC_EXP_NAME")
    mlflow.set_tag("dvc_experiment_name", dvc_exp_name 
    if dvc_exp_name is not None else "N/A")
    if auto_logging_cfg.get("config", False):
        from framework import reporter
        reporter.log_config_all()
    if auto_logging_cfg.get("location", False):
        mlflow.set_tag("host_name", socket.gethostname())
        mlflow.set_tag("current_working_directory", os.getcwd())
    tag_config_all(cfg=syscfg_custom)


    