import context
from omegaconf import DictConfig

try:
    cfg: DictConfig = context._reporter_config_context.get()
except LookupError:
    raise Exception("FATAL: config was referenced in framework/config.py before the config was set in framework/hydraset.py. " \
            "Hint: Make sure never to import framework/config.py directly.")
    #cfg = OmegaConf.create({}) # 空のConfigでフォールバック
