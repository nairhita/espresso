#!/bin/bash --login 
# Copyright (C) 2013 Olaf Lenz
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
DIR=`dirname $0`
source $DIR/common.sh

start "BUILD"
# DEFAULTS
[ -z "$myconfig" ] && myconfig="default"
[ -z "$build_procs" ] && build_procs=4
[ -z "$make_params" ] && make_params=""

make_params="-j $build_procs $make_params"

outp myconfig build_procs

# change into build dir
pushd $builddir

# BUILD

if [ "$myconfig" = "default" ]; then
    echo "Using default myconfig."
    if [ -e $builddir/myconfig.hpp ]; then
        echo "Deleting $builddir/myconfig.hpp..."
        rm $builddir/myconfig.hpp
    fi
else
    myconfig_file=$srcdir/maintainer/configs/$myconfig.hpp
    if [ ! -e "$myconfig_file" ]; then
        echo "$myconfig_file does not exist!"
        exit 1
    fi
    echo "Copying $myconfig.hpp to $builddir/myconfig.hpp..."
    cp $myconfig_file $builddir/myconfig.hpp
fi
cmd "make $make_params" || exit $?

popd
end "BUILD"

