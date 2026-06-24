python $1/code/main.py $2 $3 2>/tmp/served_stderr.log
ec=$?
cat /tmp/served_stderr.log >&2
exit $ec
