echo "Filling Disk with $size MB of random data for $duration seconds."

nohup dd if=/dev/urandom of=/root/burn bs=1M count=$size iflag=fullblock
sleep $duration
rm /root/burn