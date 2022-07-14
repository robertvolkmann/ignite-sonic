FROM scratch

ADD rootfs.tar /

# Check config_samples.py and rc.local to understand the default_sku behavior
RUN echo 'onie_platform=x86_64-kvm_x86_64-r0' > /host/machine.conf \
 && mkdir -p /var/platform \
 && echo $(jq '.DEVICE_METADATA.localhost.type = "ToRRouter"' /etc/sonic/init_cfg.json) > /etc/sonic/init_cfg.json \
 && echo 'Force10-S6000 l1' > /usr/share/sonic/device/x86_64-kvm_x86_64-r0/default_sku
