import context
class ContextAwareRunProxy:
    def _get_active_run(self):
        try:
            return context._reporter_run_context.get()
        except LookupError:
            raise Exception("FATAL: run (wandb run) was referenced in framework/wandb_init.py before the config was set in framework/hydraset.py. " \
                    "Hint: Make sure never to import framework/wandb_init.py directly (or access 'run' outside of the active context).")

    def __getattr__(self, name):
        return getattr(self._get_active_run(), name)

    def __setattr__(self, name, value):
        setattr(self._get_active_run(), name, value)

run = ContextAwareRunProxy()