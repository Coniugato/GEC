import wandb
from omegaconf import OmegaConf, DictConfig
import os, socket
import get_sysconfig as sysconfig
from utils import _get_flat_dict, _process_dict_for_mlflow, _log_params_safely

def wandb_init(cfg, reinit):
    cfg_flatten = _get_flat_dict(cfg)
    return wandb.init(
        project=sysconfig.project_name,
        config=cfg_flatten,
        reinit=reinit,
        name=sysconfig.run_name,
    )

def wandb_standard_logging():
    import reporter
    run = reporter.run
    dvc_exp_name = sysconfig.dvc_exp_name
    run.tags = run.tags + (["dvc_experiment_name:" + (dvc_exp_name 
    if dvc_exp_name is not None else "N/A")],)
    if sysconfig.auto_logging_cfg.get("config", False):
        cfg_dict = OmegaConf.to_container(sysconfig.syscfg_custom, resolve=True)
        run.config.update(cfg_dict, allow_val_change=True)
    #if sysconfig.auto_logging_cfg.get("location", False):
    #    run.tags = run.tags + (f"host_name:{sysconfig.hostname}",)
    #    run.tags = run.tags + (f"current_working_directory:{sysconfig.cwd}",)
    flat_cfg_dict = _get_flat_dict(sysconfig.syscfg_custom)
    for k, v in flat_cfg_dict.items():
        run.tags = run.tags + (f"{k}:{v}",)

