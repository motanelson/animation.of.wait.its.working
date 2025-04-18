printf "\033c\033[43;30m\n"
sudo qemu-system-x86_64 -m 2G -boot c -hda llvmx86.img -net tap -net nic 
