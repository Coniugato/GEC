from contextvars import ContextVar
from omegaconf import DictConfig

# 遅延して初期化されるグローバルコンフィグ変数
_reporter_config_context: ContextVar[DictConfig] = ContextVar("cfg")