# get CPU counts
cpus=$(cat /proc/cpuinfo | awk "/^processor/{print $3}" | wc -l)
pids=""
echo "Stressing $cpus CPUs for $duration seconds."
trap 'for p in $pids; do kill $p; done' 0

for i in $cpus
do
    while :
        do :
        done & pids="$pids $!";
done
sleep $duration
