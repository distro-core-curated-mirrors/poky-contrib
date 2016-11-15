#!/usr/bin/env bash
#
# Copyright (c) 2011, Intel Corporation.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

set -o nounset
set -o errexit

OUTDIR="buildstats-plots"
CD=$(dirname $0)

function bsplots() {
    local STAT=$1

    NS_STAT=$(echo $STAT | sed -e 's/ /-/g')
    GPLIMAGE='set terminal png fontscale 1 size 1920,1080'

    # task-recipe plot
    OUTDATA="$OUTDIR/$NS_STAT.ts"
    OUTGPL="set output '$OUTDATA.png'"
    $CD/buildstats-plot.sh -o "$OUTDATA" -s "$STAT" > "$OUTDATA.gpl"
    gnuplot -e "$GPLIMAGE;$OUTGPL" "$OUTDATA.gpl"

    # task plot
    OUTDATA="$OUTDIR/$NS_STAT.t"
    OUTGPL="set output '$OUTDATA.png'"
    $CD/buildstats-plot.sh -o "$OUTDATA" -s "$STAT" -S > "$OUTDATA.gpl"
    gnuplot -e "$GPLIMAGE;$OUTGPL" "$OUTDATA.gpl"
}

if [ ! -d "$OUTDIR" ]; then
    mkdir -p $OUTDIR
fi

bsplots "utime"
bsplots "stime"
bsplots "cutime"
bsplots "cstime"
bsplots "IO wchar"
bsplots "IO write_bytes"
bsplots "IO syscr"
bsplots "IO read_bytes"
bsplots "IO rchar"
bsplots "IO syscw"
bsplots "IO cancelled_write_bytes"
bsplots "rusage ru_utime"
bsplots "rusage ru_stime"
bsplots "rusage ru_maxrss"
bsplots "rusage ru_minflt"
bsplots "rusage ru_majflt"
bsplots "rusage ru_inblock"
bsplots "rusage ru_oublock"
bsplots "rusage ru_nvcsw"
bsplots "rusage ru_nivcsw"
bsplots "Child rusage ru_utime"
bsplots "Child rusage ru_stime"
bsplots "Child rusage ru_maxrss"
bsplots "Child rusage ru_minflt"
bsplots "Child rusage ru_majflt"
bsplots "Child rusage ru_inblock"
bsplots "Child rusage ru_oublock"
bsplots "Child rusage ru_nvcsw"
bsplots "Child rusage ru_nivcsw"
