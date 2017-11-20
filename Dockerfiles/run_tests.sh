#!/bin/bash -xe

CONTAINER=$1
LINCHPINDIR=$2
shift; shift
DRIVERS=$*

function clean_up {
    set +e
    docker kill $CONTAINER
    docker rm $CONTAINER
}

trap clean_up EXIT SIGHUP SIGINT SIGTERM

# Pull latest example topolgies
if [ -d "lp_test_workspace" ]; then
    pushd lp_test_workspace && git pull
    popd
else
    git clone https://github.com/herlo/lp_test_workspace.git
fi

# Pull down duffy-ansible-module
if [ -d "duffy-ansible-module" ]; then
    pushd duffy-ansible-module && git pull
    popd
else
    git clone https://github.com/CentOS-PaaS-SIG/duffy-ansible-module.git
fi

docker run --privileged -d -v $LINCHPINDIR:/workdir/ \
    -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name $CONTAINER $CONTAINER
docker exec -it $CONTAINER /root/linchpin-install.sh
for i in $DRIVERS; do
    if [ "$i" = "duffy" -a ! -e "duffy.key" ]; then
        (>&2 echo "WARN: skipping duffy test since duffy.key is missing")
        continue
    fi
    docker exec -it $CONTAINER /root/linchpin-test.sh $i
done
