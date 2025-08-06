# This Dockerfile builds the image used by agent qe installation tests
FROM quay.io/ocp-splat/govc:v0.30.7 as govc
FROM quay.io/centos/centos:stream9
ENV HOME /output

# TODO: Remove once OpenShift CI supports it out of the box (see https://access.redhat.com/articles/4859371)
RUN chmod g+w /etc/passwd && \
    echo 'echo default:x:$(id -u):$(id -g):Default Application User:${HOME}:/sbin/nologin\ >> /etc/passwd' > /usr/local/bin/fix_uid.sh && \
    chmod g+rwx /usr/local/bin/fix_uid.sh

RUN set -x; INSTALL_PKGS="bash bc bind-utils butane ca-certificates conntrack-tools coreos-installer diffutils \
        ethtool file findutils gawk git gzip hostname iperf3 ipmitool iproute iputils jq libvirt-client lsof make \
        mtr net-tools nmap-ncat nmstate openssh procps procps-ng python3.11 python3.11-pip python3.11-devel rsync shadow-utils socat strace \
        tar tcpdump tree util-linux wget which zip gcc-toolset-12 go-toolset openssl openssl-devel sshpass" && \
  mkdir -p ${HOME} && \
  dnf install --setopt=install_weak_deps=False --nodocs -y $INSTALL_PKGS && \
  dnf clean all && \
  rm -rf /var/cache/yum/*

RUN set -x; \
    OC_TAR_URL="https://mirror.openshift.com/pub/openshift-v4/$(uname -m)/clients/ocp/latest/openshift-client-linux.tar.gz" && \
    curl -L -q -o /tmp/oc.tar.gz "$OC_TAR_URL" && \
    tar -C /usr/bin/ -xvf /tmp/oc.tar.gz oc && \
    ln -sf /usr/bin/oc /usr/bin/kubectl && \
    rm -f /tmp/oc.tar.gz

COPY . .

RUN wget -O /usr/local/bin/yq \
  https://github.com/mikefarah/yq/releases/download/v4.30.4/yq_linux_$(uname -m \
    | sed 's/x86_64/amd64/;s/aarch64/arm64/') && \
  chmod +x /usr/local/bin/yq && \
  pip3.11 install --upgrade pip && \
  pip3.11 install --no-cache-dir -I -r images/prow-image/requirements.txt && \
  chmod -R g+rwx /output

RUN playwright install firefox
RUN ansible-galaxy collection install nutanix.ncp:2.1.1

COPY --from=govc /govc /bin/govc
