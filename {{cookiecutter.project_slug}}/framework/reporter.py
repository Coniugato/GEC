from omegaconf import OmegaConf
import config as __reporter_internal_config__
import mlflow as __reporter_internal_mlflow__
import reporter_helper as __reporter_internal_helper__
import wandb_run as __reporter_internal_wandb__

# 後で自動化しても良いかも
if hasattr(__reporter_internal_mlflow__, "cfg"):
    raise Exception("FATAL: mlflow module already has attribute 'cfg'. This may cause conflicts."
                    "Check framework/reporter.py and try changing the property name.")
cfg = __reporter_internal_config__.cfg
run = __reporter_internal_wandb__.run


if hasattr(__reporter_internal_mlflow__, "log_config"):
    raise Exception("FATAL: mlflow module already has attribute 'log_config'. This may cause conflicts."
                    "Check framework/reporter.py and try changing the property name.")
if hasattr(__reporter_internal_mlflow__, "log_config_all"):
    raise Exception("FATAL: mlflow module already has attribute 'log_config_all'. This may cause conflicts."
                    "Check framework/reporter.py and try changing the property name.")
log_config = __reporter_internal_helper__.log_config
log_config_all = __reporter_internal_helper__.log_config_all

import mlflow as mlflow 
import wandb as wandb
