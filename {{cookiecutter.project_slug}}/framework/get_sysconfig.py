from utils import register_resolvers
from utils import _get_flat_dict, _process_dict_for_mlflow, _log_params_safely
import os, socket
from omegaconf import OmegaConf, DictConfig

register_resolvers()
syscfg_report: DictConfig = OmegaConf.load("sysconf/report_config.yaml")
syscfg_custom: DictConfig = OmegaConf.load("sysconf/custom.yaml")
syscfg_meta: DictConfig = OmegaConf.load("sysconf/meta_config.yaml")
project_name = syscfg_report.get("project_name")
#特に指定がなければ合わせる
mlflow_experiment_name = syscfg_report.get("mlflow_experiment_name", project_name)
if mlflow_experiment_name is None:
    mlflow_experiment_name = project_name
tracking_uri = syscfg_report.get("tracking_uri")
run_name = syscfg_report.get("run_name", "default_run")
auto_logging_cfg = syscfg_report.get("auto_logging", {})
description = syscfg_meta.get("description", "No description provided.")

dvc_exp_name = os.environ.get("DVC_EXP_NAME")
hostname = socket.gethostname()
cwd = os.getcwd()