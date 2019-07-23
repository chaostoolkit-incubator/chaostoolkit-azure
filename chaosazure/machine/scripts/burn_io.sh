#Script for BurnIO Chaos Monkey

cat << EOF > /tmp/loop.sh
while [ true ];
do
    sudo dd if=/dev/urandom of=/root/burn bs=32K count=1024 iflag=fullblock
done
EOF

chmod +x /tmp/loop.sh
timeout --preserve-status $duration /tmp/loop.sh
sudo rm /root/burn
sudo rm /tmp/loop.sh