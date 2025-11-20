#!/bin/bash
MAIN_REPO_PATH=$(git rev-parse --show-toplevel)
EXP_NAME="exp-$(date +%Y%m%d%H%M%S)"
ORIGINAL_BRANCH=$(git rev-parse --abbrev-ref HEAD)
git add -A
python $MAIN_REPO_PATH/framework/dvc_queue.py --action enqueue --name $EXP_NAME --repo .
JOB_SCRIPT_CONTENT=$(cat batch_setting.sh)$(cat <<EOF


cd ${MAIN_REPO_PATH}
source ${MAIN_REPO_PATH}/.venv/bin/activate
python $MAIN_REPO_PATH/framework/dvc_queue.py --action run_one --id ${EXP_NAME} --repo .
EOF
)

JOB_SCRIPT=$(cat ./batch_setting.sh)$'\n'"$JOB_SCRIPT_CONTENT"

touch __job__temporary__.sh
echo "$JOB_SCRIPT" > __job__temporary__.sh
chmod +x __job__temporary__.sh

chmod +x ./batch_run.sh
HPC_JOB_ID=$(./batch_run.sh __job__temporary__.sh)
rm __job__temporary__.sh

echo "Submitted job: $HPC_JOB_ID (Exp: $EXP_NAME)"