echo "RUNSH_START $(date +%H:%M:%S) pwd=$(pwd) a1=$1 a2=$2 a3=$3" >> /tmp/runsh.log 2>&1
python $1/code/main.py $2 $3 2>> /tmp/runsh.log
echo "RUNSH_END rc=$? $(date +%H:%M:%S)" >> /tmp/runsh.log 2>&1
