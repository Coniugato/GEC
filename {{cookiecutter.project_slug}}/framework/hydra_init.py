import hydra
from omegaconf import DictConfig
import context
import mlflow
import mlflow_helper
import wandb_helper
import argparse
import utils
import wandb
import os


@hydra.main(config_path="../conf", config_name="config", version_base=None)
def hydra_init(cfg: DictConfig):
    context._reporter_config_context.set(cfg) 

    with wandb_helper.wandb_init(cfg, reinit=True) as run:
        run.log_code(".",
        exclude_fn=lambda path, root: any(
            os.path.relpath(path, root).startswith(exclude_dir)
            for exclude_dir in [".venv/", ".dvc/", ".git/"]
        ),)
        context._reporter_run_context.set(run)
        with mlflow_helper.init_mlflow_run(cfg.get("call")):
            mlflow_helper.mlflow_standard_logging()
            wandb_helper.wandb_standard_logging()
            utils.set_seed(cfg.get("seed"))

            import src.main as main
            print("================ Experiment Content ================")
            print("🧪Experiment Started!")
            if not hasattr(main, cfg.get("call")):
                raise Exception(f"FATAL: src/main.py does not have {cfg.get('call')} function.")
            print(f"Calling function: {cfg.get("call")}")
            print()
            try:
                getattr(main, cfg.get("call"))()
                print()
                print("✅ Experiment Finished!")
                print("====================================================")
            except BaseException as e:
                print()
                print("❌ Experiment Failed!")
                print("====================================================")
                raise e



if __name__ == "__main__":
    hydra_init()

"""
DataLoader(
        dataset=my_dataset,
        batch_size=cfg.params.batch_size,
        num_workers=cfg.params.num_workers, # (例: 4)
        worker_init_fn=worker_init_fn,     # <-- コレ
        generator=torch.Generator().manual_seed(cfg.seed) # (PyTorch 1.6+ 推奨)
    )
としなければいけないことに注意
"""