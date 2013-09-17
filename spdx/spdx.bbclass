# This class integrates real-time license scanning, generation of SPDX standard 
# output and verifiying license info during the building process. 
# It is a combination of efforts from the OE-Core, SPDX and Fossology projects.
#
# For more information on FOSSology:
#   http://www.fossology.org
#
# For more information on FOSSologySPDX commandline:
#   https://github.com/spdx-tools/fossology-spdx/wiki/Fossology-SPDX-Web-API
#
# For more information on SPDX:
#   http://www.spdx.org
#

# SPDX file will be output to the path which is defined as[SPDX_MANIFEST_DIR] 
# in ./meta/conf/licenses.conf.

SPDXSSTATEDIR = "${SSTATE_DIR}/spdx"

python do_spdx () {
    import os, sys
    import json

    info = {} 
    info['workdir'] = (d.getVar('WORKDIR', True) or "")
    info['sourcedir'] = (d.getVar('S', True) or "")
    info['pn'] = (d.getVar( 'PN', True ) or "")
    info['pv'] = (d.getVar( 'PV', True ) or "")
    info['src_uri'] = (d.getVar( 'SRC_URI', True ) or "")
    info['spdx_version'] = (d.getVar('SPDX_VERSION', True) or '')
    info['data_license'] = (d.getVar('DATA_LICENSE', True) or '')

    spdx_sstate_dir = (d.getVar('SPDXSSTATEDIR', True) or "")
    manifest_dir = (d.getVar('SPDX_MANIFEST_DIR', True) or "")
    info['outfile'] = os.path.join(manifest_dir, info['pn'] + ".spdx" )
    sstatefile = os.path.join(spdx_sstate_dir, 
        info['pn'] + info['pv'] + ".spdx" )
    info['spdx_temp_dir'] = (d.getVar('SPDX_TEMP_DIR', True) or "")
    info['tar_file'] = os.path.join( info['workdir'], info['pn'] + ".tar.gz" )

    official_lics = d.getVarFlags('SPDXLICENSEMAP')

    ## get everything from cache.  use it to decide if 
    ## something needs to be rerun 
    cur_ver_code = get_ver_code( info['sourcedir'] ) 
    cache_cur = False
    if not os.path.exists( spdx_sstate_dir ):
        bb.mkdirhier( spdx_sstate_dir )
    if not os.path.exists( info['spdx_temp_dir'] ):
        bb.mkdirhier( info['spdx_temp_dir'] )
    if os.path.exists( sstatefile ):
        ## cache for this package exists. read it in
        cached_spdx = get_cached_spdx( sstatefile )

        if cached_spdx['PackageVerificationCode'] == cur_ver_code:
            #bb.warn(info['pn'] + "'s ver code same as cache's. do nothing")
            cache_cur = True
        else:
            local_files = setup_foss_scan( info, 
                cache=True, cached_files=cached_spdx['Files'] )
            cache_lics = cached_spdx['Extracted_licenses']
    else:
        local_files = setup_foss_scan( info )
        cache_lics = {}

    if cache_cur:
        spdx_files = cached_spdx['Files']
        spdx_lics = cached_spdx['Extracted_licenses']
    else:
        ## setup fossology command
        foss_server = (d.getVar('FOSS_SERVER', True) or "")
        foss_flags = (d.getVar('FOSS_WGET_FLAGS', True) or "")
        foss_command = "wget %s --post-file=%s %s"\
            % (foss_flags,info['tar_file'],foss_server)
        
        foss_files, foss_lics = run_fossology( foss_command )
        if not foss_files:
            bb.warn("Fossology scan failed for %s. No manifest created."
                % info['pn'])
            spdx_files = None
        else:
            ## get spdx file information 
            spdx_files, spdx_lics = create_spdx_doc(local_files, 
                foss_files, cache_lics, foss_lics, official_lics)
            
            write_cached_spdx(sstatefile,cur_ver_code
                ,spdx_files, spdx_lics)
    
    if spdx_files:
        ## Get document and package level information
        spdx_header = get_spdx_header(info, cur_ver_code, spdx_files)
    
        ## CREATE MANIFEST
        create_manifest(info,spdx_header,spdx_files,spdx_lics)

        ## clean up the temp stuff
        remove_dir_tree( info['spdx_temp_dir'] )
        if os.path.exists(info['tar_file']):
            remove_file( info['tar_file'] )
}
addtask spdx after do_patch before do_configure

def create_manifest(info,header,files,ex_lics):
    with open(info['outfile'], 'w') as f:
        f.write(header + '\n')

        f.write('## File Information')
        f.write('\n')
        for chksum, block in files.iteritems():
            for key, value in block.iteritems():
                f.write(key + ": " + value)
                f.write('\n')
            f.write('\n')

        f.write('## License Information')
        f.write('\n')
        for ex_lic in ex_lics:
            for key, value in ex_lic.iteritems():
                f.write(key + ": " + value.encode('ascii','ignore'))
                f.write('\n')
            f.write('\n')

def get_cached_spdx( sstatefile ):
    import json
    cached_spdx_info = {}
    with open( sstatefile, 'r' ) as f:
        try:
            cached_spdx_info = json.load(f)
        except ValueError as e:
            cached_spdx_info = None
    return cached_spdx_info

def write_cached_spdx( sstatefile, ver_code, files, ex_lics ):
    import json
    spdx_doc = {}
    spdx_doc['PackageVerificationCode'] = ver_code
    spdx_doc['Files'] = {}
    spdx_doc['Files'] = files
    spdx_doc['Extracted_licenses'] = {}
    spdx_doc['Extracted_licenses'] = (ex_lics or {})
    with open( sstatefile, 'w' ) as f:
        f.write(json.dumps(spdx_doc))

def setup_foss_scan( info, cache=False, cached_files=None ):
    import errno, shutil
    import tarfile
    file_info = {}
    cache_dict = {}

    for f_dir, f in list_files( info['sourcedir'] ):
        full_path =  os.path.join( f_dir, f )
        abs_path = os.path.join(info['sourcedir'], full_path)
        dest_dir = os.path.join( info['spdx_temp_dir'], f_dir )
        dest_path = os.path.join( info['spdx_temp_dir'], full_path )
        try:
            stats = os.stat(abs_path)
        except OSError as e:
            bb.warn( "Stat failed" + str(e) + "\n")
            continue

        checksum = hash_file( abs_path )
        mtime = time.asctime(time.localtime(stats.st_mtime))
        
        ## retain cache information if it exists
        file_info[checksum] = {}
        if cache and checksum in cached_files:
            file_info[checksum] = cached_files[checksum]
        else:
            file_info[checksum]['FileName'] = full_path

        try:
            os.makedirs( dest_dir )
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(dest_dir):
                pass
            else: 
                bb.warn( "mkdir failed " + str(e) + "\n" )
                continue

        if(cache and checksum not in cached_files) or not cache:
            try:
                shutil.copyfile( abs_path, dest_path )
            except shutil.Error as e:
                bb.warn( str(e) + "\n" )
            except IOError as e:
                bb.warn( str(e) + "\n" )
    
    with tarfile.open( info['tar_file'], "w:gz" ) as tar:
        tar.add( info['spdx_temp_dir'], arcname=os.path.basename(info['spdx_temp_dir']) )
    tar.close()
    
    return file_info


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

def list_files( dir ):
    for root, subFolders, files in os.walk( dir ):
        for f in files:
            rel_root = os.path.relpath( root, dir )
            yield rel_root, f
    return

def hash_file( file_name ):
    try: 
        f = open( file_name, 'rb' )
        data_string = f.read()
    except:
       return None
    finally:
        f.close()
    sha1 = hash_string( data_string )
    return sha1

def hash_string( data ):
    import hashlib
    sha1 = hashlib.sha1()
    sha1.update( data )
    return sha1.hexdigest()

def run_fossology( foss_command ):
    import string, re
    import subprocess
    import json
    
    file_info = {}
    extracted_licenses= {}

    p = subprocess.Popen(foss_command.split(), 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    foss_output, foss_error = p.communicate()
    ## try and make sure it looks like spdx output
    json_output = ''
    try: 
        json_output = json.loads(foss_output)
    except ValueError as e:
        bb.warn("Error parsing FOSSology output\n"
            + "command: %s\nOutput: %s" % (foss_command,foss_output))
        return None, None

    ## Make sure there is actually spdx here
    if 'file_level_info' in json_output and\
            json_output['file_level_info'] != None:
        for f in json_output['file_level_info']:
            file_info[f['FileChecksum']] = f
    else:
        bb.warn("Error while trying to run fossology scan\n"
            + "command: %s\nOutput: %s" % (foss_command,foss_output))
        return None, None

    if 'extracted_license_info' in json_output and\
            json_output['extracted_license_info'] != None:
        for e in json_output['extracted_license_info']:
            extracted_licenses[e['LicenseName']] = e

    return file_info, extracted_licenses

def create_spdx_doc(file_info,foss_files,cache_lics,foss_lics,off_lics):
    import json
    ## push foss changes back into cache
    for chksum, lic_info in foss_files.iteritems():
        if chksum in file_info:
            file_info[chksum]['FileName'] = file_info[chksum]['FileName']
            file_info[chksum]['FileType'] = lic_info['FileType']
            file_info[chksum]['FileChecksum: ' 
                + lic_info['FileChecksumAlgorithm']] = chksum
            file_info[chksum]['LicenseInfoInFile'] =\
                lic_info['LicenseInfoInFile']
            file_info[chksum]['LicenseConcluded'] =\
                lic_info['LicenseConcluded']
            file_info[chksum]['FileCopyrightText'] =\
                lic_info['FileCopyrightText']
        else:
            bb.warn(lic_info['FileName'] + " : " + chksum 
                + " : is not in the local file info: " 
                + json.dumps(lic_info,indent=1))
            pass

    file_info, spdx_lics = create_extracted_licenses(
        file_info, foss_lics, cache_lics, off_lics)

    return file_info, spdx_lics

def create_extracted_licenses(files,foss_lics,cache_lics,off_lics):
    """
        Take files with license name fields and change to an
        extracted license format. Return extracted license
        information as well
    """
    import json, re

    spdx_lics = []
    sel = {}
    lic_counter = 0
    refs = {}
    ref = ""

    ## keep cached license references. Don't
    ## overwrite LicenseRef-##
    for ex_lic in cache_lics:
        refs[ex_lic['LicenseID']] = ex_lic
        c = re.search('(\d+)$',ex_lic['LicenseID']).group(1)
        if int(c) > lic_counter:
            lic_counter = int(c) + 1

    for chksum, f in files.iteritems():
        if f['LicenseInfoInFile'] == 'No_license_found':
            continue
        file_lics = []
        for l in f['LicenseInfoInFile'].split(','):
            ## if it is already referencing a license number or
            ## if it is part of the recognized spdx licenses then skip
            if re.match('LicenseRef-\d+', l):
                file_lics.append(l)
                continue
            elif l in off_lics:
                l = off_lics[l]
                file_lics.append(l)
                continue
            elif l in off_lics.values():
                file_lics.append(l)
                continue
    
            if l in refs:
                ref = refs[l]
            else:
                ref = 'LicenseRef-%d' % lic_counter
                refs[l] = ref
                lic_counter += 1

            if not ref in sel:
                sel[ref] = {}
                if l in foss_lics:
                    sel[ref] = foss_lics[l]
                else:
                    sel[ref]['LicenseName'] = l
                    sel[ref]['ExtractedText'] = "<text>NOASSERTION</text>"
                    sel[ref]['LicenseCrossReference'] = ""
                
                sel[ref]['LicenseID'] = ref
                spdx_lics.append(sel[ref])

            file_lics.append(ref)
        
        f['LicenseInfoInFile'] = ','.join(file_lics)

    return files, spdx_lics

def get_ver_code( dirname ):
    chksums = []
    for f_dir, f in list_files( dirname ):
        try:
            stats = os.stat(os.path.join(dirname,f_dir,f))
        except OSError as e:
            bb.warn( "Stat failed" + str(e) + "\n")
            continue
        chksums.append(hash_file(os.path.join(dirname,f_dir,f)))
    chksums.sort()
    ver_code_string = ''.join(chksums).lower()
    ver_code = hash_string( ver_code_string )
    return ver_code

def get_spdx_header( info, spdx_verification_code, spdx_files ):
    """
        Put together the header SPDX information. 
        Eventually this needs to become a lot less 
        of a hardcoded thing. 
    """
    from datetime import datetime
    import os
    head = []
    DEFAULT = "NOASSERTION"

    lic_info = get_license_info_from_files(spdx_files.values())

    package_checksum = ''
    if os.path.exists(info['tar_file']):
        package_checksum = hash_file( info['tar_file'] )
    else:
        package_checksum = DEFAULT

    ## document level information
    head.append("SPDXVersion: " + info['spdx_version'])
    head.append("DataLicense: " + info['data_license'])
    head.append("DocumentComment: <text>SPDX for "
        + info['pn'] + " version " + info['pv'] + "</text>")
    head.append("")

    ## Creator information
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    head.append("## Creation Information")
    head.append("Creator: fossology-spdx")
    head.append("Created: " + now)
    head.append("CreatorComment: <text>UNO</text>")
    head.append("")

    ## package level information
    head.append("## Package Information")
    head.append("PackageName: %s" % info['pn'])
    head.append("PackageVersion: %s" % info['pv'])
    head.append("PackageDownloadLocation: %s" 
        % (info['src_uri'].split()[0] or DEFAULT))
    head.append("PackageSummary: <text>%s</text>" % DEFAULT)
    head.append("PackageFileName: %s" % os.path.basename(info['tar_file']))
    head.append("PackageSupplier: Person:%s" % DEFAULT)
    head.append("PackageOriginator: Person:%s" % DEFAULT)
    head.append("PackageChecksum: SHA1: %s" % package_checksum)
    head.append("PackageVerificationCode: %s" % spdx_verification_code)
    head.append("PackageDescription: <text>%s version %s</text>" 
        % (info['pn'], info['pv']))
    head.append("")
    head.append("PackageCopyrightText: <text>%s</text>" % DEFAULT)
    head.append("")
    head.append("PackageLicenseDeclared: (%s)" % ' AND '.join(lic_info))
    head.append("PackageLicenseConcluded: %s" % DEFAULT)
    for l in lic_info:
        head.append("PackageLicenseInfoFromFiles: %s" % l)
    head.append("")
    
    return '\n'.join(head)

def get_license_info_from_files( files ):
    """
        Get a non-duplicate list of licenses from 
        a list of files
    """
    import json
    ## don't need no license type stuff in the list
    exclude = ['No_license_found','NOASSERTION']
    licenses = []
    for f in files:
        if 'LicenseInfoInFile' in f:
            for l in f['LicenseInfoInFile'].split(','):
                if l in exclude:
                    continue
                if not l in licenses:
                    licenses.append(l)
        else:
            #bb.warn( json.dumps(f) )
            pass

    licenses.sort()
    return licenses
