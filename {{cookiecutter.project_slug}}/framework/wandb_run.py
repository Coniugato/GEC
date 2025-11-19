import context

try:
    run = context._reporter_run_context.get()
except LookupError:
    raise Exception("FATAL: run (wandb run) was referenced in framework/wandb_init.py before the config was set in framework/hydraset.py. " \
            "Hint: Make sure never to import framework/wandb_init.py directly.")

