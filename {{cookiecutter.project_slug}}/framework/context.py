from contextvars import ContextVar
from omegaconf import DictConfig

_reporter_config_context: ContextVar[DictConfig] = ContextVar("cfg")
_reporter_run_context: ContextVar = ContextVar("run")