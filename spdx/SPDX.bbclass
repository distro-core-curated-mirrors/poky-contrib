do_SPDX () {
    ## set up 
    outfile=/home/yocto/fossology_scans/${PN}.spdx.out
    foss_server=https://foss-spdx-dev.ist.unomaha.edu
    foss_flags="-qO - --no-check-certificate --timeout=0"

    ## create tmp dir and remove old log file
    rm -f ${outfile}
    mkdir -p ${WORKDIR}/spdx_temp
    echo "Made temp spdx directory in WORKDIR" >> ${outfile}
    ls -ld ${WORKDIR}/spdx_temp >> ${outfile}
    echo >> ${outfile}

	## Eventually we will just assume that if no cache, run against
    ## all files, but for now leave out this check
    # if [ there is no cached SPDX ]; then
    ##   copy the entire contents of the source directory
    #    cp -fpR ${S}/ ${WORKDIR}/spdx_temp
    # else 
        for file in `find ${S}/ -type f`; do
            ## take only the files in ${S} that have a different
            ## checksum than is in the cached SPDX
            # if [ file checksum different than what's in cache ]; then
                file_chksum=`sha1sum ${file} | awk '{print $1}'`
                printf "${file} checksum = ${file_chksum}\n" >> ${outfile}
                printf "Copying to ${WORKDIR}/spdx_temp\n\n" >> ${outfile}
                cp -fp ${file} ${WORKDIR}/spdx_temp
            #else
                ## file is the same as before, doubt I need to do anything
                # code if I do
            #fi
        done
    # fi
    
    ## tar all files that have changed and were copied here, 
    ## send them to fossology to be scanned. 
    tar -pzcvf ${WORKDIR}/${BPN}.tar.gz ${WORKDIR}/spdx_temp/
    spdx_checksum=`sha1sum ${WORKDIR}/${BPN}.tar.gz | awk '{print $1}'`
    foss_output=`wget ${foss_flags} --post-file=${WORKDIR}/${BPN}.tar.gz ${foss_server}/?mod=spdx_license_once`
    
    ## write out the output and checksum of tar file for now
    echo "\nFOSSOLOGY output:" >> ${outfile}
    echo ${foss_output} >> ${outfile}
    printf "Checksum:  %s\n\n" ${spdx_checksum} >> ${outfile}
        
    ## remove the tar file that was made and spdx_temp directory
    rm -f ${WORKDIR}/${BPN}.tar.gz
    rm -rf ${WORKDIR}/spdx_temp/
    echo "Removed spdx temp directory" >> ${outfile}
    ls -ld ${WORKDIR}/spdx_temp || echo "${WORKDIR}/spdx_temp removed properly" >> ${outfile}

    ## compare ${foss_output} against the SPDX file that is in cache
    # to come
    ## write possibly updated SPDX back to cache
    # to come
}
addtask SPDX after do_patch before do_configure
