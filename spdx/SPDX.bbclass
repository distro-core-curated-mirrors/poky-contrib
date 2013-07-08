python do_SPDX () {
    import os
    import tarfile
    import subprocess

    info = {} 
    info['workdir'] = (d.getVar('WORKDIR', True) or "")
    info['sourcedir'] = (d.getVar('S', True) or "")
    info['pn'] = (d.getVar( 'PN', True ) or "")
    info['pv'] = (d.getVar( 'PV', True ) or "")

    outfile = "/home/yocto/fossology_scans/" + info['pn'] + ".spdx.out"
    info['spdxdir'] = info['workdir'] + "/spdx_temp"

    ## remove old log file, create tmp dir
    remove_file( outfile )
    if not os.path.exists( info['spdxdir'] ):
        os.makedirs( info['spdxdir'] )

    file = open( outfile, 'w+' )
    write_metadata( info, file )
    cp_changed_files( info, file )

    tar_file = os.path.join( info['workdir'], info['pn'] + ".tar.gz" )
    with tarfile.open( tar_file, "w:gz" ) as tar:
        tar.add( info['spdxdir'], arcname=os.path.basename(info['spdxdir']) )
    tar.close()

    foss_server = "https://foss-spdx-dev.ist.unomaha.edu"\
        + "/?mod=spdx_license_once"
    foss_flags = ["wget", "-qO", "-", "--no-check-certificate", 
        "--timeout=0", "--post-file=" + tar_file, foss_server]
    p = subprocess.Popen(foss_flags, stdout=subprocess.PIPE)
    foss_output, foss_error = p.communicate()

    file.write( foss_output + "\n" )
    file.close()

    ## clean up the temp stuff
    remove_dir_tree( info['spdxdir'] )
    remove_file( tar_file )
}
addtask SPDX after do_patch before do_configure

def cp_changed_files( info, file ):
    import errno, shutil
    for f_dir, f in listFiles( info['sourcedir'] ):
        full_path =  os.path.join( f_dir, f )
        dest_dir = os.path.join( info['spdxdir'], f_dir )
        dest_path = os.path.join( info['spdxdir'], full_path )
        try:
            stats = os.stat( full_path )
        except OSError as e:
            file.write( "Stat failed" + str(e) + "\n")
            continue

        checksum = hash_file( full_path )
        file.write( "Name: %s\nSize: %s\nmtime: %s\nsha1: %s\n\n" % 
            ( full_path, stats.st_size, 
            time.asctime(time.localtime(stats.st_mtime)), checksum) )

        try:
            os.makedirs( dest_dir )
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(dest_dir):
                pass
            else: 
                file.write( "mkdir failed " + str(e) + "\n" )
                continue

        try:
            shutil.copyfile( full_path, dest_path )
        except shutil.Error as e:
            file.write( str(e) + "\n" )
        except IOError as e:
            file.write( str(e) + "\n" )


def remove_dir_tree( dir_name ):
    import shutil
    try: 
        shutil.rmtree( dir_name )
    except:
        pass

def remove_file( file_name ):
    try:
        os.remove( file_name )
    except OSError as e:
        pass

def listFiles( dir ):
    for root, subFolders, files in os.walk( dir ):
        for f in files:
            rel_root = os.path.relpath( root, dir )
            yield rel_root, f
            #yield os.path.join( root, f )
    return

def hash_file( file_name ):
    import hashlib
    sha1 = hashlib.sha1()
    f = open( file_name, 'rb' )
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()

def write_metadata( info, file ):
    file.write( "----------------\n" )
    for key, value in info.iteritems():
        file.write( key + " = " + value + "\n" )
    file.write( "----------------\n\n" )
