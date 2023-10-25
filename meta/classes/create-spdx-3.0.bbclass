#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: GPL-2.0-only
#

DEPLOY_DIR_SPDX ??= "${DEPLOY_DIR}/spdx"

# The product name that the CVE database uses.  Defaults to BPN, but may need to
# be overriden per recipe (for example tiff.bb sets CVE_PRODUCT=libtiff).
CVE_PRODUCT ??= "${BPN}"
CVE_VERSION ??= "${PV}"

SPDXDIR ??= "${WORKDIR}/spdx-3.0"
SPDXDEPLOY = "${SPDXDIR}/deploy"
SPDXWORK = "${SPDXDIR}/work"
SPDXIMAGEWORK = "${SPDXDIR}/image-work"
SPDXSDKWORK = "${SPDXDIR}/sdk-work"
SPDXDEPS = "${SPDXDIR}/deps.json"

SPDX_TOOL_NAME ??= "oe-spdx-creator"
SPDX_TOOL_VERSION ??= "1.0"

SPDXRUNTIMEDEPLOY = "${SPDXDIR}/runtime-deploy"

SPDX_INCLUDE_SOURCES ??= "0"
SPDX_ARCHIVE_SOURCES ??= "0"
SPDX_ARCHIVE_PACKAGED ??= "0"

SPDX_UUID_NAMESPACE ??= "sbom.openembedded.org"
SPDX_NAMESPACE_PREFIX ??= "http://spdx.org/spdxdoc"
SPDX_PRETTY ??= "0"

SPDX_LICENSES ??= "${COREBASE}/meta/files/spdx-licenses.json"

SPDX_CUSTOM_ANNOTATION_VARS ??= ""

SPDX_ORG ??= "OpenEmbedded ()"
SPDX_SUPPLIER ??= "Organization: ${SPDX_ORG}"
SPDX_SUPPLIER[doc] = "The SPDX PackageSupplier field for SPDX packages created from \
    this recipe. For SPDX documents create using this class during the build, this \
    is the contact information for the person or organization who is doing the \
    build."

def new_spdxid(d, doc, *suffix):
    pn = d.getVar("PN")
    return "/".join([get_doc_namespace(d, doc), pn] + list(suffix))

def extract_licenses(filename):
    import re

    lic_regex = re.compile(rb'^\W*SPDX-License-Identifier:\s*([ \w\d.()+-]+?)(?:\s+\W*)?$', re.MULTILINE)

    try:
        with open(filename, 'rb') as f:
            size = min(15000, os.stat(filename).st_size)
            txt = f.read(size)
            licenses = re.findall(lic_regex, txt)
            if licenses:
                ascii_licenses = [lic.decode('ascii') for lic in licenses]
                return ascii_licenses
    except Exception as e:
        bb.warn(f"Exception reading {filename}: {e}")
    return None

def get_doc_namespace(d, doc):
    import uuid
    namespace_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, d.getVar("SPDX_UUID_NAMESPACE"))
    return "%s/%s-%s" % (d.getVar("SPDX_NAMESPACE_PREFIX"), doc.name, str(uuid.uuid5(namespace_uuid, doc.name)))

def generate_creationInfo(d, document, comment=None):
    """
    Generate the creationInfo and its elements for a document
    """
    from datetime import datetime, timezone
    import oe.spdx3

    creation_time = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    document.creationInfo = oe.spdx3.SPDX3CreationInfo()
    document.creationInfo.specVersion = "3.0.0"
    document.creationInfo.created = creation_time
    document.creationInfo.dataLicense = "https://spdx.org/licenses/CC0-1.0"

    if comment is not None:
        document.creationInfo.comment = comment

    tool = oe.spdx3.SPDX3Tool()
    tool.name = "OpenEmbedded Core create-spdx.bbclass"
    tool.spdxId = new_spdxid(d, document, "Actor", tool.name.replace(" ", ""))
    tool.creationInfo = document.creationInfo
    document.element.append(tool)
    document.creationInfo.createdUsing.append(tool)

    organization = oe.spdx3.SPDX3Organization()
    organization.name = d.getVar("SPDX_ORG")
    organization.spdxId = new_spdxid(d, document, "Actor", organization.name.replace(" ", ""))
    organization.creationInfo = document.creationInfo
    document.element.append(organization)
    document.creationInfo.createdBy.append(organization)

    person = oe.spdx3.SPDX3Person()
    person.name = "Person: N/A ()"
    person.spdxId = new_spdxid(d, document, "Actor", person.name.replace(" ", ""))
    document.creationInfo.createdBy.append(person)
    document.element.append(person)

def get_supplier(d, doc=None):
    """
    Get the supplier of a document or create it.
    """
    import oe.spdx3

    supplier = d.getVar("SPDX_SUPPLIER")
    agentName = supplier.split(": ")[1]
    agentType = supplier.split(": ")[0]

    if doc:
        for element in doc.element:
            if(isinstance(element, oe.spdx3.SPDX3Agent) and element.name == agentName):
                return element

    if(agentType == "Organization"):
        agent = oe.spdx3.SPDX3Organization()
    elif(agentType == "Person"):
        agent = oe.spdx3.SPDX3Person()
    else:
        raise KeyError("%r is not a valid SPDX agent type" % agentType)

    agent.name = agentName
    agent.spdxId = new_spdxid(d, doc, "Actor", agent.name)
    agent.creationInfo = doc.creationInfo

    return agent

def create_annotation(d, doc, recipe, comment):
    import oe.spdx3

    c = oe.spdx3.SPDX3Annotation()
    c.annotationType = "other"
    c.subject = recipe.spdxId
    c.statement = comment
    c.spdxId = new_spdxid(d, doc, "annotation", comment)

    doc.element.append(c)

def create_relationship(d, doc, _from, relationshipType, to):
    import oe.spdx3

    if isinstance(_from, oe.spdx3.SPDX3Element):
        _from = _from.spdxId
    
    if isinstance(to, oe.spdx3.SPDX3Element):
        to = to.spdxId

    for el in doc.element:
        if isinstance(el, oe.spdx3.SPDX3Relationship) and \
        el._from == _from and \
        el.relationshipType == relationshipType:
            el.to.append(to)
            return el.spdxId
    
    r = oe.spdx3.SPDX3Relationship()
    r.spdxId = new_spdxid(d, doc, "Relationship", relationshipType)
    r._from = _from
    r.to.append(to)
    r.relationshipType = relationshipType

    doc.element.append(r)
    return r.spdxId

def recipe_spdx_is_native(doc, recipe):
    import oe.spdx3

    for element in doc.element:
        if isinstance(element, oe.spdx3.SPDX3Annotation) \
        and element.subject == recipe.spdxId \
        and element.statement == "isNative":
            return True

    return False

def is_work_shared_spdx(d):
    return bb.data.inherits_class('kernel', d) or ('work-shared' in d.getVar('WORKDIR'))

def get_json_indent(d):
    if d.getVar("SPDX_PRETTY") == "1":
        return 2
    return None

python() {
    import json
    if d.getVar("SPDX_LICENSE_DATA"):
        return

    with open(d.getVar("SPDX_LICENSES"), "r") as f:
        data = json.load(f)
        # Transform the license array to a dictionary
        data["licenses"] = {l["licenseId"]: l for l in data["licenses"]}
        d.setVar("SPDX_LICENSE_DATA", data)
}

def add_extracted_license(d, document, ident, name):
    from pathlib import Path
    import oe.spdx3

    extracted_info = oe.spdx3.SPDX3SimpleLicensingText()
    extracted_info.name = name
    extracted_info.licenseText = None

    if name == "PD":
        # Special-case this.
        extracted_info.licenseText = "Software released to the public domain"
    else:
        # Seach for the license in COMMON_LICENSE_DIR and LICENSE_PATH
        for directory in [d.getVar('COMMON_LICENSE_DIR')] + (d.getVar('LICENSE_PATH') or '').split():
            try:
                with (Path(directory) / name).open(errors="replace") as f:
                    extracted_info.licenseText = f.read()
                    break
            except FileNotFoundError:
                pass
        if extracted_info.licenseText is None:
            # If it's not SPDX or PD, then NO_GENERIC_LICENSE must be set
            filename = d.getVarFlag('NO_GENERIC_LICENSE', name)
            if filename:
                filename = d.expand("${S}/" + filename)
                with open(filename, errors="replace") as f:
                    extracted_info.licenseText = f.read()
            else:
                bb.fatal("Cannot find any text for license %s" % name)

    return extracted_info

def convert(d, l, document):
    import oe.spdx3

    license_data = d.getVar("SPDX_LICENSE_DATA")

    if l == "(" or l == ")":
        return l

    if l == "&":
        return "AND"

    if l == "|":
        return "OR"

    if l == "CLOSED":
        return "NONE"

    spdx_license = d.getVarFlag("SPDXLICENSEMAP", l) or l

    if spdx_license in license_data["licenses"]:
        lic = oe.spdx3.SPDX3LicenseExpression()
        lic.licenseExpression = spdx_license
        lic.licenseListVersion = d.getVar("SPDX_LICENSE_DATA")["licenseListVersion"]
        return lic
    else:
        spdx_license = "LicenseText-" + l
        return add_extracted_license(d, document, spdx_license, l)


def convert_license_to_spdx(lic, document, d, existing={}):
    import oe.spdx3

    licenses_found = []
    licenses_id = []
    
    lic_split = lic.replace("(", " ( ").replace(")", " ) ").replace("|", " | ").replace("&", " & ").split()
    for l in lic_split:
        licenses_found.append(convert(d, l, document))
    
    for element in licenses_found:

        existing_licenses = document.get_licenses()

        if isinstance(element, oe.spdx3.SPDX3LicenseExpression):
            lic_type = "LicenseExpression"
        else:
            lic_type = "SimpleLicenseText"

        if isinstance(element, oe.spdx3.SPDX3AnyLicenseInfo) and not existing_licenses:
            element.spdxId = new_spdxid(d, document, lic_type, "1")
            licenses_id.append(element.spdxId)
            document.element.append(element)
        elif isinstance(element, oe.spdx3.SPDX3AnyLicenseInfo):
            for existinglic in existing_licenses:
                if ("licenseExpression" in element.properties() and "licenseExpression" in existinglic.properties() and element.licenseExpression == existinglic.licenseExpression) or \
                ("licenseText" in element.properties() and "licenseText" in existinglic.properties() and element.licenseText == existinglic.licenseText):
                    licenses_id.append(existinglic.spdxId)
                    break

            element.spdxId = new_spdxid(d, document, lic_type, str(len(existing_licenses) + 1))
            licenses_id.append(element.spdxId)
            document.element.append(element)

    return licenses_id

def process_sources(d):
    pn = d.getVar('PN')
    assume_provided = (d.getVar("ASSUME_PROVIDED") or "").split()
    if pn in assume_provided:
        for p in d.getVar("PROVIDES").split():
            if p != pn:
                pn = p
                break

    # glibc-locale: do_fetch, do_unpack and do_patch tasks have been deleted,
    # so avoid archiving source here.
    if pn.startswith('glibc-locale'):
        return False
    if d.getVar('PN') == "libtool-cross":
        return False
    if d.getVar('PN') == "libgcc-initial":
        return False
    if d.getVar('PN') == "shadow-sysroot":
        return False

    # We just archive gcc-source for all the gcc related recipes
    if d.getVar('BPN') in ['gcc', 'libgcc']:
        bb.debug(1, 'spdx: There is bug in scan of %s is, do nothing' % pn)
        return False

    return True


def add_package_files(d, doc, spdx_pkg, topdir, get_spdxid, get_types, *, archive=None, ignore_dirs=[], ignore_top_level_dirs=[]):
    from pathlib import Path
    import oe.spdx3

    source_date_epoch = d.getVar("SOURCE_DATE_EPOCH")
    if source_date_epoch:
        source_date_epoch = int(source_date_epoch)

    sha1s = []
    spdx_files = []

    file_counter = 1
    for subdir, dirs, files in os.walk(topdir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        if subdir == str(topdir):
            dirs[:] = [d for d in dirs if d not in ignore_top_level_dirs]

        for file in files:
            filepath = Path(subdir) / file
            filename = str(filepath.relative_to(topdir))

            if not filepath.is_symlink() and filepath.is_file():
                spdx_file = oe.spdx3.SPDX3File()
                spdx_file.name = filename
                spdx_file.spdxId = get_spdxid(file_counter)
                spdx_file.primaryPurpose = None
                spdx_file.additionalPurpose = []
                types = get_types(filepath)
                for t in types:
                    if t in oe.spdx3.SPDX3SoftwarePurpose:
                        if spdx_file.primaryPurpose == None:
                            spdx_file.primaryPurpose = t
                        else:
                            spdx_file.additionalPurpose.append(t)

                if archive is not None:
                    with filepath.open("rb") as f:
                        info = archive.gettarinfo(fileobj=f)
                        info.name = filename
                        info.uid = 0
                        info.gid = 0
                        info.uname = "root"
                        info.gname = "root"

                        if source_date_epoch is not None and info.mtime > source_date_epoch:
                            info.mtime = source_date_epoch

                        archive.addfile(info, f)

                sha1 = bb.utils.sha1_file(filepath)
                sha1s.append(sha1)

                hashSha1 = oe.spdx3.SPDX3Hash()
                hashSha1.algorithm = "sha1"
                hashSha1.hashValue = sha1
                spdx_file.verifiedUsing.append(hashSha1)

                hashSha256 = oe.spdx3.SPDX3Hash()
                hashSha256.algorithm = "sha256"
                hashSha256.hashValue = bb.utils.sha256_file(filepath)
                spdx_file.verifiedUsing.append(hashSha256)

                if d.getVar("SPDX_ENABLE_LICENSING") == "1" and \
                "source" in get_types(filepath):
                    extracted_lics = extract_licenses(filepath)
                    if extracted_lics:
                        for lic in extracted_lics:
                            current_licenses = doc.get_licenses_exp()
                            if current_licenses:
                                for c_lic in current_licenses:
                                    if lic == c_lic.licenseExpression:
                                        create_relationship(d, doc, spdx_file, "declaredLicense", c_lic)
                                        break

                                l = oe.spdx3.SPDX3LicenseExpression()
                                l.licenseExpression = lic
                                l.licenseListVersion = d.getVar("SPDX_LICENSE_DATA")["licenseListVersion"]
                                l.spdxId = new_spdxid(d, doc, "LicenseExpression", str(len(current_licenses) +1))
                                doc.element.append(l)
                                create_relationship(d, doc, spdx_file, "declaredLicense", l)
                            else:
                                l = oe.spdx3.SPDX3LicenseExpression()
                                l.licenseExpression = lic
                                l.spdxId = new_spdxid(d, doc, "LicenseExpression", "1")
                                l.licenseListVersion = d.getVar("SPDX_LICENSE_DATA")["licenseListVersion"]
                                doc.element.append(l)
                                create_relationship(d, doc, spdx_file, "declaredLicense", l)

                doc.element.append(spdx_file)

                create_relationship(d, doc, spdx_pkg, "contains", spdx_file)

                spdx_files.append(spdx_file)
                file_counter += 1

    return spdx_files


def add_package_sources_from_debug(d, package_doc, spdx_package, package, package_files, sources):
    return

add_package_sources_from_debug[vardepsexclude] += "STAGING_KERNEL_DIR"

def collect_dep_recipes(d, doc, spdx_recipe):
    import json
    from pathlib import Path
    import oe.sbom
    import oe.spdx3

    deploy_dir_spdx = Path(d.getVar("DEPLOY_DIR_SPDX"))
    spdx_deps_file = Path(d.getVar("SPDXDEPS"))
    package_archs = d.getVar("SSTATE_ARCHS").split()
    package_archs.reverse()

    dep_recipes = []

    with spdx_deps_file.open("r") as f:
        deps = json.load(f)

    for dep_pn, dep_hashfn in deps:
        dep_recipe_path = oe.sbom.doc_find_by_hashfn(deploy_dir_spdx, package_archs, "recipe-" + dep_pn, dep_hashfn)
        if not dep_recipe_path:
            bb.fatal("Cannot find any SPDX file for recipe %s, %s" % (dep_pn, dep_hashfn))

        spdx_dep_doc, spdx_dep_pkg, spdx_dep_sha1 = oe.sbom.search_doc(dep_recipe_path, ["Package"])

        for pkg in spdx_dep_pkg['Package']:
            if pkg["name"] == dep_pn:
                spdx_dep_recipe = pkg
                break
        else:
            continue

        dep_recipes.append(oe.sbom.DepRecipe(spdx_dep_doc, spdx_dep_sha1, spdx_dep_recipe))

        dep_recipe_ref = oe.spdx3.SPDX3ExternalMap()
        dep_recipe_ref.externalId = spdx_dep_doc["spdxId"]
        hashSha1 = oe.spdx3.SPDX3Hash()
        hashSha1.algorithm = "sha1"
        hashSha1.hashValue = spdx_dep_sha1
        dep_recipe_ref.verifiedUsing.append(hashSha1)

        doc.imports.append(dep_recipe_ref)
        create_relationship(d, doc, dep_recipe_ref.externalId, "buildDependency", spdx_recipe)

    # return dep_recipes

collect_dep_recipes[vardepsexclude] = "SSTATE_ARCHS"

def collect_dep_sources(d, dep_recipes):
    return {}

def add_download_packages(d, doc, recipe):
    import os.path
    from bb.fetch2 import decodeurl, CHECKSUM_LIST
    import bb.process
    import oe.spdx3
    import oe.sbom

    for download_idx, src_uri in enumerate(d.getVar('SRC_URI').split()):
        f = bb.fetch2.FetchData(src_uri, d)

        for name in f.names:
            package = oe.spdx3.SPDX3Package()
            package.name = "%s-source-%d" % (d.getVar("PN"), download_idx + 1)
            package.spdxId = new_spdxid(d, doc, "source", str(download_idx + 1))

            if f.type == "file":
                continue

            uri = f.type
            proto = getattr(f, "proto", None)
            if proto is not None:
                uri = uri + "+" + proto
            uri = uri + "://" + f.host + f.path

            if f.method.supports_srcrev():
                uri = uri + "@" + f.revisions[name]

            if f.method.supports_checksum(f):
                for checksum_id in CHECKSUM_LIST:
                    if checksum_id not in oe.spdx3.SPDX3HashAlgorithm:
                        continue

                    expected_checksum = getattr(f, "%s_expected" % checksum_id)
                    if expected_checksum is None:
                        continue

                    c = oe.spdx3.SPDX3Hash()
                    c.algorithm = checksum_id.upper()
                    c.hashValue = expected_checksum
                    package.verifiedUsing.append(c)

            package.downloadLocation = uri
            doc.element.append(package)

            create_relationship(d, doc, doc, "describes", package)
            create_relationship(d, doc, package, "buildDependency", recipe)

def collect_direct_deps(d, dep_task):
    current_task = "do_" + d.getVar("BB_CURRENTTASK")
    pn = d.getVar("PN")

    taskdepdata = d.getVar("BB_TASKDEPDATA", False)

    for this_dep in taskdepdata.values():
        if this_dep[0] == pn and this_dep[1] == current_task:
            break
    else:
        bb.fatal(f"Unable to find this {pn}:{current_task} in taskdepdata")

    deps = set()
    for dep_name in this_dep[3]:
        dep_data = taskdepdata[dep_name]
        if dep_data[1] == dep_task and dep_data[0] != pn:
            deps.add((dep_data[0], dep_data[7]))

    return sorted(deps)

collect_direct_deps[vardepsexclude] += "BB_TASKDEPDATA"
collect_direct_deps[vardeps] += "DEPENDS"

python do_collect_spdx_deps() {
    # This task calculates the build time dependencies of the recipe, and is
    # required because while a task can deptask on itself, those dependencies
    # do not show up in BB_TASKDEPDATA. To work around that, this task does the
    # deptask on do_create_spdx and writes out the dependencies it finds, then
    # do_create_spdx reads in the found dependencies when writing the actual
    # SPDX document
    import json
    from pathlib import Path

    spdx_deps_file = Path(d.getVar("SPDXDEPS"))

    deps = collect_direct_deps(d, "do_create_spdx")

    with spdx_deps_file.open("w") as f:
        json.dump(deps, f)
}
# NOTE: depending on do_unpack is a hack that is necessary to get it's dependencies for archive the source
addtask do_collect_spdx_deps after do_unpack
do_collect_spdx_deps[depends] += "${PATCHDEPENDENCY}"
do_collect_spdx_deps[deptask] = "do_create_spdx"
do_collect_spdx_deps[dirs] = "${SPDXDIR}"

python do_create_spdx() {
    import oe.sbom
    import oe.spdx3
    import uuid
    from pathlib import Path
    from contextlib import contextmanager
    import oe.cve_check

    @contextmanager
    def optional_tarfile(name, guard, mode="w"):
        import tarfile
        import bb.compress.zstd

        num_threads = int(d.getVar("BB_NUMBER_THREADS"))

        if guard:
            name.parent.mkdir(parents=True, exist_ok=True)
            with bb.compress.zstd.open(name, mode=mode + "b", num_threads=num_threads) as f:
                with tarfile.open(fileobj=f, mode=mode + "|") as tf:
                    yield tf
        else:
            yield None


    deploy_dir_spdx = Path(d.getVar("DEPLOY_DIR_SPDX"))
    spdx_workdir = Path(d.getVar("SPDXWORK"))
    include_sources = d.getVar("SPDX_INCLUDE_SOURCES") == "1"
    archive_sources = d.getVar("SPDX_ARCHIVE_SOURCES") == "1"
    archive_packaged = d.getVar("SPDX_ARCHIVE_PACKAGED") == "1"

    doc = oe.spdx3.SPDX3SpdxDocument()

    doc.name = "recipe-" + d.getVar("PN")
    doc.documentNamespace = get_doc_namespace(d, doc)
    doc.spdxId = new_spdxid(d, doc, "Document")
    generate_creationInfo(d, doc)

    recipe = oe.spdx3.SPDX3Package()
    recipe.spdxId = new_spdxid(d, doc, "Recipe")
    recipe.name = d.getVar("PN")
    recipe.packageVersion = d.getVar("PV")
    recipe.suppliedBy.append(get_supplier(d, doc))

    if bb.data.inherits_class("native", d) or bb.data.inherits_class("cross", d):
        create_annotation(d, doc, recipe, "isNative")

    homepage = d.getVar("HOMEPAGE")
    if homepage:
        recipe.homePage = homepage

    if d.getVar("SPDX_ENABLE_LICENSING") == "1":
        _license = d.getVar("LICENSE")
        if _license:
            licenseDeclared = convert_license_to_spdx(_license, doc, d)
            for l in licenseDeclared:
                create_relationship(d, doc, recipe, "declaredLicense", l)

    summary = d.getVar("SUMMARY")
    if summary:
        recipe.summary = summary

    description = d.getVar("DESCRIPTION")
    if description:
        recipe.description = description

    if d.getVar("SPDX_CUSTOM_ANNOTATION_VARS"):
        for var in d.getVar('SPDX_CUSTOM_ANNOTATION_VARS').split():
            recipe.annotations.append(create_annotation(d, doc, recipe, var + "=" + d.getVar(var)))

    # TODO: CVE handling

    doc.element.append(recipe)

    create_relationship(d, doc, doc, "describes", recipe)

    add_download_packages(d, doc, recipe)

    if process_sources(d) and include_sources:
        recipe_archive = deploy_dir_spdx / "recipes" / (doc.name + ".tar.zst")
        with optional_tarfile(recipe_archive, archive_sources) as archive:
            spdx_get_src(d)

            add_package_files(
                d,
                doc,
                recipe,
                spdx_workdir,
                lambda file_counter: new_spdxid(d, doc, "sourcefile", str(file_counter)),
                lambda filepath: ["source"],
                ignore_dirs=[".git"],
                ignore_top_level_dirs=["temp"],
                archive=archive,
            )

            if archive is not None:
                recipe.packageFileName = str(recipe_archive.name)

    collect_dep_recipes(d, doc, recipe)

    doc_sha1 = oe.sbom.write_doc(d, doc, doc, d.getVar("SSTATE_PKGARCH"), "recipes", indent=get_json_indent(d))

    # TODO: Recipe_ref not working with image_spdx_archive
    #recipe_ref = oe.spdx3.SPDX3ExternalMap()
    #recipe_ref.externalId = recipe.spdxId
    #recipe_hash = oe.spdx3.SPDX3Hash()
    #recipe_hash.algorithm = "sha1"
    #recipe_hash.hashValue = doc_sha1
    #recipe_ref.verifiedUsing.append(recipe_hash)
    #recipe_ref.definingDocument = get_doc_namespace(d, doc)

    if not recipe_spdx_is_native(doc, recipe):
        bb.build.exec_func("read_subpackage_metadata", d)

        pkgdest = Path(d.getVar("PKGDEST"))
        for package in d.getVar("PACKAGES").split():
            if not oe.packagedata.packaged(package, d):
                continue

            doc = oe.spdx3.SPDX3SpdxDocument()
            pkg_name = d.getVar("PKG:%s" % package) or package
            doc.name = pkg_name
            doc.documentNamespace = get_doc_namespace(d, doc)
            doc.spdxId = new_spdxid(d, doc, "Document")
            generate_creationInfo(d, doc)

            # TODO: Rework when License Profile implemented
            #doc.imports.append(recipe_ref)

            package_license = d.getVar("LICENSE:%s" % package) or d.getVar("LICENSE")

            spdx_package = oe.spdx3.SPDX3Package()

            spdx_package.spdxId = new_spdxid(d, doc, "package", pkg_name)
            spdx_package.name = pkg_name
            spdx_package.packageVersion = d.getVar("PV")
            spdx_package.suppliedBy.append(get_supplier(d, doc))

            if d.getVar("SPDX_ENABLE_LICENSING") == "1":
                licenseDeclared = convert_license_to_spdx(package_license, doc, d)
                for l in licenseDeclared:
                    create_relationship(d, doc, spdx_package, "declaredLicense", l)

            doc.element.append(spdx_package)

            create_relationship(d, doc, recipe, "generates", spdx_package)
            create_relationship(d, doc, doc, "describes", spdx_package)

            package_archive = deploy_dir_spdx / "packages" / (doc.name + ".tar.zst")
            with optional_tarfile(package_archive, archive_packaged) as archive:
                package_files = add_package_files(
                    d,
                    doc,
                    spdx_package,
                    pkgdest / package,
                    lambda file_counter: new_spdxid(d, doc, "package", pkg_name, "file", str(file_counter)),
                    lambda filepath: ["executable"],
                    ignore_top_level_dirs=['CONTROL', 'DEBIAN'],
                    archive=archive,
                )

                if archive is not None:
                    spdx_package.packageFileName = str(package_archive.name)

            # TODO: is that required ?
            # add_package_sources_from_debug(d, doc, spdx_package, package, package_files, sources)

            oe.sbom.write_doc(d, doc, doc, d.getVar("SSTATE_PKGARCH"), "packages", indent=get_json_indent(d))
}
do_create_spdx[vardepsexclude] += "BB_NUMBER_THREADS"
# NOTE: depending on do_unpack is a hack that is necessary to get it's dependencies for archive the source
addtask do_create_spdx after do_package do_packagedata do_unpack do_collect_spdx_deps before do_populate_sdk do_build do_rm_work

SSTATETASKS += "do_create_spdx"
do_create_spdx[sstate-inputdirs] = "${SPDXDEPLOY}"
do_create_spdx[sstate-outputdirs] = "${DEPLOY_DIR_SPDX}"

python do_create_spdx_setscene () {
    sstate_setscene(d)
}
addtask do_create_spdx_setscene

do_create_spdx[dirs] = "${SPDXWORK}"
do_create_spdx[cleandirs] = "${SPDXDEPLOY} ${SPDXWORK}"
do_create_spdx[depends] += "${PATCHDEPENDENCY}"

def collect_package_providers(d):
    from pathlib import Path
    import oe.sbom
    import oe.spdx
    import json

    deploy_dir_spdx = Path(d.getVar("DEPLOY_DIR_SPDX"))

    providers = {}

    deps = collect_direct_deps(d, "do_create_spdx")
    deps.append((d.getVar("PN"), d.getVar("BB_HASHFILENAME")))

    for dep_pn, dep_hashfn in deps:
        localdata = d
        recipe_data = oe.packagedata.read_pkgdata(dep_pn, localdata)
        if not recipe_data:
            localdata = bb.data.createCopy(d)
            localdata.setVar("PKGDATA_DIR", "${PKGDATA_DIR_SDK}")
            recipe_data = oe.packagedata.read_pkgdata(dep_pn, localdata)

        for pkg in recipe_data.get("PACKAGES", "").split():

            pkg_data = oe.packagedata.read_subpkgdata_dict(pkg, localdata)
            rprovides = set(n for n, _ in bb.utils.explode_dep_versions2(pkg_data.get("RPROVIDES", "")).items())
            rprovides.add(pkg)

            if "PKG" in pkg_data:
                pkg = pkg_data["PKG"]
                rprovides.add(pkg)

            for r in rprovides:
                providers[r] = (pkg, dep_hashfn)

    return providers

collect_package_providers[vardepsexclude] += "BB_TASKDEPDATA"

python do_create_runtime_spdx() {
    from datetime import datetime, timezone
    import oe.sbom
    import oe.spdx3
    import oe.packagedata
    from pathlib import Path

    deploy_dir_spdx = Path(d.getVar("DEPLOY_DIR_SPDX"))
    spdx_deploy = Path(d.getVar("SPDXRUNTIMEDEPLOY"))
    is_native = bb.data.inherits_class("native", d) or bb.data.inherits_class("cross", d)

    creation_time = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    providers = collect_package_providers(d)
    pkg_arch = d.getVar("SSTATE_PKGARCH")
    package_archs = d.getVar("SSTATE_ARCHS").split()
    package_archs.reverse()

    if not is_native:
        bb.build.exec_func("read_subpackage_metadata", d)

        dep_package_cache = {}

        pkgdest = Path(d.getVar("PKGDEST"))
        for package in d.getVar("PACKAGES").split():
            localdata = bb.data.createCopy(d)
            pkg_name = d.getVar("PKG:%s" % package) or package
            localdata.setVar("PKG", pkg_name)
            localdata.setVar('OVERRIDES', d.getVar("OVERRIDES", False) + ":" + package)

            if not oe.packagedata.packaged(package, localdata):
                continue

            pkg_spdx_path = oe.sbom.doc_path(deploy_dir_spdx, pkg_name, pkg_arch, "packages")

            j_package_doc, j_packages, package_doc_sha1 = oe.sbom.search_doc(pkg_spdx_path, ["Package"])

            for p in j_packages["Package"]:
                if p['name'] == pkg_name:
                    j_spdx_package = p
                    break
            else:
                bb.fatal("Package '%s' not found in %s" % (pkg_name, pkg_spdx_path))

            runtime_doc = oe.spdx3.SPDX3SpdxDocument()
            runtime_doc.name = "runtime-" + pkg_name
            runtime_doc.documentNamespace = get_doc_namespace(localdata, runtime_doc)
            runtime_doc.creationInfo.created = creation_time
            generate_creationInfo(d, runtime_doc,
                                  "This document was created by analyzing package runtime dependencies.")

            package_ref = oe.spdx3.SPDX3ExternalMap()
            package_ref.externalId = "DocumentRef-package-" + package
            package_ref.definingDocument = j_package_doc['documentNamespace']
            hashSha1 = oe.spdx3.SPDX3Hash()
            hashSha1.algorithm = "sha1"
            hashSha1.hashValue = package_doc_sha1
            package_ref.verifiedUsing.append(hashSha1)

            runtime_doc.imports.append(package_ref)

            create_relationship(
                d, runtime_doc,
                runtime_doc,
                "amends",
                "%s:%s" % (package_ref.externalId, j_package_doc['spdxId'])
            )

            deps = bb.utils.explode_dep_versions2(localdata.getVar("RDEPENDS") or "")
            seen_deps = set()
            for dep, _ in deps.items():
                if dep in seen_deps:
                    continue

                if dep not in providers:
                    continue

                (dep, dep_hashfn) = providers[dep]

                if not oe.packagedata.packaged(dep, localdata):
                    continue

                dep_pkg_data = oe.packagedata.read_subpkgdata_dict(dep, d)
                dep_pkg = dep_pkg_data["PKG"]

                if dep in dep_package_cache:
                    (j_dep_spdx_package, dep_package_ref) = dep_package_cache[dep]
                else:
                    dep_path = oe.sbom.doc_find_by_hashfn(deploy_dir_spdx, package_archs, dep_pkg, dep_hashfn)
                    if not dep_path:
                        bb.fatal("No SPDX file found for package %s, %s" % (dep_pkg, dep_hashfn))

                    j_spdx_dep_doc, j_spdx_dep_packages, spdx_dep_sha1 = oe.sbom.search_doc(dep_path, ["Package"])

                    for pkg in j_spdx_dep_packages["Package"]:
                        if pkg['name'] == dep_pkg:
                            j_dep_spdx_package = pkg
                            break
                    else:
                        bb.fatal("Package '%s' not found in %s" % (dep_pkg, dep_path))


                    dep_package_ref = oe.spdx3.SPDX3ExternalMap()
                    dep_package_ref.externalId = "DocumentRef-runtime-dependency-" + j_spdx_dep_doc['name']
                    dep_package_ref.definingDocument = j_spdx_dep_doc['documentNamespace']
                    hashSha1 = oe.spdx3.SPDX3Hash()
                    hashSha1.algorithm = "sha1"
                    hashSha1.hashValue = spdx_dep_sha1
                    dep_package_ref.verifiedUsing.append(hashSha1)

                    dep_package_cache[dep] = (j_dep_spdx_package, dep_package_ref)

                runtime_doc.imports.append(dep_package_ref)

                create_relationship(
                    d, runtime_doc,
                    "%s:%s" % (dep_package_ref.externalId, j_dep_spdx_package['spdxId']),
                    "runtimeDependency",
                    "%s:%s" % (package_ref.externalId, j_spdx_package['spdxId'])
                )
                seen_deps.add(dep)

            oe.sbom.write_doc(d, runtime_doc, runtime_doc, pkg_arch, "runtime", spdx_deploy, indent=get_json_indent(d))
}

do_create_runtime_spdx[vardepsexclude] += "OVERRIDES SSTATE_ARCHS"

addtask do_create_runtime_spdx after do_create_spdx before do_build do_rm_work
SSTATETASKS += "do_create_runtime_spdx"
do_create_runtime_spdx[sstate-inputdirs] = "${SPDXRUNTIMEDEPLOY}"
do_create_runtime_spdx[sstate-outputdirs] = "${DEPLOY_DIR_SPDX}"

python do_create_runtime_spdx_setscene () {
    sstate_setscene(d)
}
addtask do_create_runtime_spdx_setscene

do_create_runtime_spdx[dirs] = "${SPDXRUNTIMEDEPLOY}"
do_create_runtime_spdx[cleandirs] = "${SPDXRUNTIMEDEPLOY}"
do_create_runtime_spdx[rdeptask] = "do_create_spdx"

def spdx_get_src(d):
    """
    save patched source of the recipe in SPDX_WORKDIR.
    """
    import shutil
    spdx_workdir = d.getVar('SPDXWORK')
    spdx_sysroot_native = d.getVar('STAGING_DIR_NATIVE')
    pn = d.getVar('PN')

    workdir = d.getVar("WORKDIR")

    try:
        # The kernel class functions require it to be on work-shared, so we dont change WORKDIR
        if not is_work_shared_spdx(d):
            # Change the WORKDIR to make do_unpack do_patch run in another dir.
            d.setVar('WORKDIR', spdx_workdir)
            # Restore the original path to recipe's native sysroot (it's relative to WORKDIR).
            d.setVar('STAGING_DIR_NATIVE', spdx_sysroot_native)

            # The changed 'WORKDIR' also caused 'B' changed, create dir 'B' for the
            # possibly requiring of the following tasks (such as some recipes's
            # do_patch required 'B' existed).
            bb.utils.mkdirhier(d.getVar('B'))

            bb.build.exec_func('do_unpack', d)
        # Copy source of kernel to spdx_workdir
        if is_work_shared_spdx(d):
            share_src = d.getVar('WORKDIR')
            d.setVar('WORKDIR', spdx_workdir)
            d.setVar('STAGING_DIR_NATIVE', spdx_sysroot_native)
            src_dir = spdx_workdir + "/" + d.getVar('PN')+ "-" + d.getVar('PV') + "-" + d.getVar('PR')
            bb.utils.mkdirhier(src_dir)
            if bb.data.inherits_class('kernel',d):
                share_src = d.getVar('STAGING_KERNEL_DIR')
            cmd_copy_share = "cp -rf " + share_src + "/* " + src_dir + "/"
            cmd_copy_shared_res = os.popen(cmd_copy_share).read()
            bb.note("cmd_copy_shared_result = " + cmd_copy_shared_res)

            git_path = src_dir + "/.git"
            if os.path.exists(git_path):
                shutils.rmtree(git_path)

        # Make sure gcc and kernel sources are patched only once
        if not (d.getVar('SRC_URI') == "" or is_work_shared_spdx(d)):
            bb.build.exec_func('do_patch', d)

        # Some userland has no source.
        if not os.path.exists( spdx_workdir ):
            bb.utils.mkdirhier(spdx_workdir)
    finally:
        d.setVar("WORKDIR", workdir)

spdx_get_src[vardepsexclude] += "STAGING_KERNEL_DIR"

do_rootfs[recrdeptask] += "do_create_spdx do_create_runtime_spdx"
do_rootfs[cleandirs] += "${SPDXIMAGEWORK}"

ROOTFS_POSTUNINSTALL_COMMAND =+ "image_combine_spdx"

do_populate_sdk[recrdeptask] += "do_create_spdx do_create_runtime_spdx"
do_populate_sdk[cleandirs] += "${SPDXSDKWORK}"
POPULATE_SDK_POST_HOST_COMMAND:append:task-populate-sdk = " sdk_host_combine_spdx"
POPULATE_SDK_POST_TARGET_COMMAND:append:task-populate-sdk = " sdk_target_combine_spdx"

python image_combine_spdx() {
    import os
    import oe.sbom
    from pathlib import Path
    from oe.rootfs import image_list_installed_packages

    image_name = d.getVar("IMAGE_NAME")
    image_link_name = d.getVar("IMAGE_LINK_NAME")
    imgdeploydir = Path(d.getVar("IMGDEPLOYDIR"))
    img_spdxid = oe.sbom.get_image_spdxid(image_name)
    packages = image_list_installed_packages(d)

    combine_spdx(d, image_name, imgdeploydir, img_spdxid, packages,
                 Path(d.getVar("SPDXIMAGEWORK")), Path(d.getVar("DEPLOY_DIR_SPDX")))
    image_spdx_archive(d, image_name, imgdeploydir,
                       Path(d.getVar("SPDXIMAGEWORK")), Path(d.getVar("DEPLOY_DIR_SPDX")))

    def make_image_link(target_path, suffix):
        if image_link_name:
            link = imgdeploydir / (image_link_name + suffix)
            if link != target_path:
                link.symlink_to(os.path.relpath(target_path, link.parent))

    spdx_tar_path = imgdeploydir / (image_name + ".spdx.tar.zst")
    make_image_link(spdx_tar_path, ".spdx.tar.zst")
}

def combine_spdx(d, rootfs_name, rootfs_deploydir, rootfs_spdxid, packages, spdx_workdir, spdx_deploydir):
    """
    Combine the SPDX for the deployed image.

    Create a document with the main image as package, add relations for each
    packages and their runtime dependencies.
    """
    import os
    import oe.spdx3
    import oe.sbom
    from datetime import timezone, datetime
    from pathlib import Path
    import bb.compress.zstd

    providers = collect_package_providers(d)
    package_archs = d.getVar("SSTATE_ARCHS").split()
    package_archs.reverse()

    creation_time = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    doc = oe.spdx3.SPDX3SpdxDocument()
    doc.name = rootfs_name
    doc.documentNamespace = get_doc_namespace(d, doc)
    doc.spdxId = new_spdxid(d, doc, "Document")
    generate_creationInfo(d, doc)

    image = oe.spdx3.SPDX3Package()
    image.name = d.getVar("PN")
    image.packageVersion = d.getVar("PV")
    image.spdxId = new_spdxid(d, doc, "image", rootfs_spdxid)
    image.suppliedBy.append(get_supplier(d, doc))

    doc.element.append(image)

    # TODO: this is done later, do we require this ?
    # image_spdx_path = spdx_workdir / (rootfs_name + ".spdx.json")
    # with image_spdx_path.open("wb") as f:
    #     doc.to_json(f, sort_keys=True, indent=get_json_indent(d))

    num_threads = int(d.getVar("BB_NUMBER_THREADS"))

    visited_docs = set()

    index = {"documents": []}

    for name in sorted(packages.keys()):
        if name not in providers:
            bb.fatal("Unable to find SPDX provider for '%s'" % name)

        pkg_name, pkg_hashfn = providers[name]

        pkg_spdx_path = oe.sbom.doc_find_by_hashfn(spdx_deploydir, package_archs, pkg_name, pkg_hashfn)
        if not pkg_spdx_path:
            bb.fatal("No SPDX file found for package %s, %s" % (pkg_name, pkg_hashfn))

        j_pkg_doc, j_pkg_pkgs, pkg_doc_sha1 = oe.sbom.search_doc(pkg_spdx_path, ['Package'])

        for p in j_pkg_pkgs['Package']:
            if p['name'] == name:
                pkg_ref = oe.spdx3.SPDX3ExternalMap()
                pkg_ref.externalId = j_pkg_doc['spdxId']
                pkg_ref.definingDocument = j_pkg_doc['documentNamespace']
                hashSha1 = oe.spdx3.SPDX3Hash()
                hashSha1.algorithm = "sha1"
                hashSha1.hashValue = pkg_doc_sha1
                pkg_ref.verifiedUsing.append(hashSha1)

                doc.imports.append(pkg_ref)
                create_relationship(d, doc, image, "contains", pkg_ref.externalId)
                break
        else:
            bb.fatal("Unable to find package with name '%s' in SPDX file %s" % (name, pkg_spdx_path))

        runtime_spdx_path = oe.sbom.doc_find_by_hashfn(spdx_deploydir, package_archs, "runtime-" + name, pkg_hashfn)
        if not runtime_spdx_path:
            bb.fatal("No runtime SPDX document found for %s, %s" % (name, pkg_hashfn))

        j_runtime_doc, _, runtime_doc_sha1 = oe.sbom.search_doc(runtime_spdx_path)

        runtime_ref = oe.spdx3.SPDX3ExternalMap()
        runtime_ref.externalId = "DocumentRef-%s" % j_runtime_doc['name']
        runtime_ref.definingDocument = j_runtime_doc['documentNamespace']
        hashSha1 = oe.spdx3.SPDX3Hash()
        hashSha1.algorithm = "sha1"
        hashSha1.hashValue = runtime_doc_sha1
        runtime_ref.verifiedUsing.append(hashSha1)

        doc.imports.append(runtime_ref)
        create_relationship(
            d,
            doc,
            image,
            "runtimeDependency",
            "%s:%s" % (runtime_ref.externalId, j_runtime_doc['spdxId'])
        )

    image_spdx_path = spdx_workdir / (rootfs_name + ".spdx.json")

    with image_spdx_path.open("wb") as f:
        doc.to_json(f, sort_keys=False, indent=get_json_indent(d))


def image_spdx_archive(d, rootfs_name, rootfs_deploydir, spdx_workdir, spdx_deploydir):
    import tarfile
    import io
    import json

    source_date_epoch = d.getVar("SOURCE_DATE_EPOCH")

    image_spdx_path = spdx_workdir / (rootfs_name + ".spdx.json")

    num_threads = int(d.getVar("BB_NUMBER_THREADS"))

    visited_docs = set()

    index = {"documents": []}

    spdx_tar_path = rootfs_deploydir / (rootfs_name + ".spdx.tar.zst")
    with bb.compress.zstd.open(spdx_tar_path, "w", num_threads=num_threads) as f:
        with tarfile.open(fileobj=f, mode="w|") as tar:
            def collect_spdx_document(path):
                nonlocal tar
                nonlocal spdx_deploydir
                nonlocal source_date_epoch
                nonlocal index

                package_archs = d.getVar("SSTATE_ARCHS").split()
                package_archs.reverse()

                if path in visited_docs:
                    return

                visited_docs.add(path)

                with path.open("rb") as f:
                    doc, _, sha1 = oe.sbom.search_doc(f, [])
                    f.seek(0)

                    if doc['documentNamespace'] in visited_docs:
                        return

                    bb.note("Adding SPDX document %s" % path)
                    visited_docs.add(doc['documentNamespace'])
                    info = tar.gettarinfo(fileobj=f)

                    info.name = doc['name'] + ".spdx.json"
                    info.uid = 0
                    info.gid = 0
                    info.uname = "root"
                    info.gname = "root"

                    if source_date_epoch is not None and info.mtime > int(source_date_epoch):
                        info.mtime = int(source_date_epoch)

                    tar.addfile(info, f)

                    index["documents"].append({
                        "filename": info.name,
                        "documentNamespace": doc['documentNamespace'],
                        "sha1": sha1,
                    })
                if 'imports' in doc:
                    for ref in doc['imports']:
                        ref_path = oe.sbom.doc_find_by_namespace(spdx_deploydir, package_archs, ref['definingDocument'])
                        if not ref_path:
                            bb.fatal("Cannot find any SPDX file for document %s" % ref['definingDocument'])
                        collect_spdx_document(ref_path)

            collect_spdx_document(image_spdx_path)

            index["documents"].sort(key=lambda x: x["filename"])

            index_str = io.BytesIO(json.dumps(
                index,
                sort_keys=True,
                indent=get_json_indent(d),
            ).encode("utf-8"))

            info = tarfile.TarInfo()
            info.name = "index.json"
            info.size = len(index_str.getvalue())
            info.uid = 0
            info.gid = 0
            info.uname = "root"
            info.gname = "root"

            tar.addfile(info, fileobj=index_str)


python sdk_host_combine_spdx() {
    return
}

python sdk_target_combine_spdx() {
    return
}
