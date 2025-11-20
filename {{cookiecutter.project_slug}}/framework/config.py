import context
from omegaconf import DictConfig

class ContextAwareConfigProxy:
    def _get_active_cfg(self) -> DictConfig:
        try:
            return context._reporter_config_context.get()
        except LookupError:
            raise Exception("FATAL: config was referenced in framework/config.py before the config was set in framework/hydraset.py. " \
                    "Hint: Make sure never to import framework/config.py directly (or access 'cfg' outside of the active context).")


    def __getattr__(self, name):
        return getattr(self._get_active_cfg(), name)

    def __getitem__(self, key):
        return self._get_active_cfg()[key]

    def __contains__(self, key):
        return key in self._get_active_cfg()

    def __repr__(self):
        try:
            return repr(self._get_active_cfg())
        except:
            return "<ContextAwareConfigProxy: No active config>"

cfg = ContextAwareConfigProxy()

