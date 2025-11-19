import argparse
from pathlib import Path
from dvc.repo import Repo
from dvc.repo.experiments.queue.base import BaseStashQueue
from dvc.repo.experiments.executor.local import TempDirExecutor
from dvc.repo.experiments.executor.base import ExecutorInfo, TaskStatus

def parse_params(params_str):
    if not params_str:
        return None
    out = {}
    parts = params_str.split(",")
    for p in parts:
        if ":" in p:
            path, override = p.split(":", 1)
            out.setdefault(path, []).append(override)
        else:
            out.setdefault("params.yaml", []).append(p)
    return out

def find_entry_by_id(queue, exp_id: str):
    matches = []
    for entry in queue.iter_queued():
        if entry.name == exp_id or (entry.stash_rev and entry.stash_rev.startswith(exp_id)):
            matches.append(entry)
    if not matches:
        return None
    if len(matches) > 1:
        return matches
    return matches[0]

def cmd_enqueue(repo_path: Path, name, params, targets):
    repo_path = repo_path.resolve()
    params_dict = parse_params(params)
    targets_arg = None if not targets else [targets]
    with Repo(str(repo_path)) as repo:
        q = repo.experiments.tempdir_queue
        entry = q.put(params=params_dict, targets=targets_arg, name=name)
        print("Queued in tempdir_queue:", entry.stash_rev, entry.name)

def cmd_list(repo_path: Path):
    repo_path = repo_path.resolve()
    with Repo(str(repo_path)) as repo:
        q = repo.experiments.tempdir_queue
        queued = [(e.stash_rev, e.name) for e in q.iter_queued()]
        if not queued:
            print("tempdir_queue: no queued entries")
        else:
            print("tempdir_queue queued entries:")
            for rev, nm in queued:
                print(f"  {rev}  name={nm}")

def cmd_run_one(repo_path, exp_id, remove_after_run=True):

    repo_path = repo_path.resolve()
    with Repo(str(repo_path)) as repo:
        q = repo.experiments.tempdir_queue
        found = find_entry_by_id(q, exp_id)
        if found is None:
            print(f"No queued experiment found for '{exp_id}' in tempdir_queue.")
            return 1
        if isinstance(found, list):
            print(f"Ambiguous match for '{exp_id}':")
            for e in found:
                print(f"  {e.stash_rev}  name={e.name}")
            return 2
        entry = found
        print(f"Found queued entry: stash_rev={entry.stash_rev}, name={entry.name}")

        executor = BaseStashQueue.init_executor(repo.experiments, entry, TempDirExecutor, location="manual-run")
        infofile = q.get_infofile_path(entry.stash_rev)

        try:
            executor_info = ExecutorInfo.load_json(infofile)
        except Exception:
            executor_info = executor.info
        print("Before reproduce:", executor_info.status)

        exec_result = executor.reproduce(info=executor.info, rev=entry.stash_rev, infofile=infofile, log_level=20, log_errors=True)

        try:
            executor_info = ExecutorInfo.load_json(infofile)
            print("After reproduce:", executor_info.status)
        except Exception:
            print("After reproduce: infofile not found/loaded")

        if not exec_result or not getattr(exec_result, "exp_hash", None):
            print("Experiment reproduce failed or produced no exp_hash")
            executor.cleanup(infofile)
            return 3

        BaseStashQueue.collect_executor(repo.experiments, executor, exec_result)

        if remove_after_run:
            try:
                q.remove([entry.stash_rev])
            except Exception:
                pass

        executor.cleanup(infofile)
        print("Done.")
        return 0

def cmd_run_all(repo_path: Path):
    from dvc.repo import Repo
    repo_path = repo_path.resolve()
    with Repo(str(repo_path)) as repo:
        q = repo.experiments.tempdir_queue
        results = q.reproduce()
        print("Reproduce results:", results)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True, help="Path to repo")
    p.add_argument("--action", required=True, choices=["enqueue", "list", "run_one", "run_all"])
    p.add_argument("--name", help="Name for enqueue")
    p.add_argument("--params", help="params overrides, comma-separated like 'params.yaml:foo=1,other:bar=2'")
    p.add_argument("--targets", help="targets (single) for enqueue")
    p.add_argument("--id", help="name or stash_rev prefix for run_one")
    args = p.parse_args()

    repo_path = Path(args.repo)
    if args.action == "enqueue":
        cmd_enqueue(repo_path, name=args.name, params=args.params, targets=args.targets)
    elif args.action == "list":
        cmd_list(repo_path)
    elif args.action == "run_one":
        if not args.id:
            print("run_one needs --id")
            return
        cmd_run_one(repo_path, args.id)
    elif args.action == "run_all":
        cmd_run_all(repo_path)

if __name__ == "__main__":
    main()