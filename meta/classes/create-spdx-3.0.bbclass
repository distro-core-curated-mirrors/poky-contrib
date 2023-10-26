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

def generate_creationInfo(d, document):
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

    tool = oe.spdx3.SPDX3Tool()
    tool.name = "OpenEmbedded Core create-spdx.bbclass"
    tool.spdxId = "spdx-" + d.getVar("PN") + ":SPDXRef-Actor-" + tool.name.replace(" ", "")
    tool.creationInfo = document.creationInfo
    document.element.append(tool)
    document.creationInfo.createdUsing.append(tool)

    organization = oe.spdx3.SPDX3Organization()
    organization.name = d.getVar("SPDX_ORG")
    organization.spdxId = "spdx-" + d.getVar("PN") + ":SPDXRef-Actor-" + organization.name.replace(" ", "")
    organization.creationInfo = document.creationInfo
    document.element.append(organization)
    document.creationInfo.createdBy.append(organization)

    person = oe.spdx3.SPDX3Person()
    person.name = "Person: N/A ()"
    person.spdxId = "spdx-" + d.getVar("PN") + ":SPDXRef-Actor-" + person.name.replace(" ", "")
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
    agent.spdxId = "spdx-" + d.getVar("PN") + ":SPDXRef-Actor-" + agent.name.replace(" ", "")
    agent.creationInfo = doc.creationInfo

    return agent

def recipe_spdx_is_native(d, recipe):
    return False
# TODO: find a better way to mark native recipes
#    return any(a.annotationType == "OTHER" and
#      a.annotator == "Tool: %s - %s" % (d.getVar("SPDX_TOOL_NAME"), d.getVar("SPDX_TOOL_VERSION")) and
#      a.comment == "isNative" for a in recipe.annotations)

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

def convert_license_to_spdx(lic, document, d, existing={}):
    from pathlib import Path
    import oe.spdx

    license_data = d.getVar("SPDX_LICENSE_DATA")
    extracted = {}

    def add_extracted_license(ident, name):
        nonlocal document

        if name in extracted:
            return

        extracted_info = oe.spdx.SPDX3ExtractedLicensingInfo()
        extracted_info.name = name
        extracted_info.licenseId = ident
        extracted_info.extractedText = None

        if name == "PD":
            # Special-case this.
            extracted_info.extractedText = "Software released to the public domain"
        else:
            # Seach for the license in COMMON_LICENSE_DIR and LICENSE_PATH
            for directory in [d.getVar('COMMON_LICENSE_DIR')] + (d.getVar('LICENSE_PATH') or '').split():
                try:
                    with (Path(directory) / name).open(errors="replace") as f:
                        extracted_info.extractedText = f.read()
                        break
                except FileNotFoundError:
                    pass
            if extracted_info.extractedText is None:
                # If it's not SPDX or PD, then NO_GENERIC_LICENSE must be set
                filename = d.getVarFlag('NO_GENERIC_LICENSE', name)
                if filename:
                    filename = d.expand("${S}/" + filename)
                    with open(filename, errors="replace") as f:
                        extracted_info.extractedText = f.read()
                else:
                    bb.fatal("Cannot find any text for license %s" % name)

        extracted[name] = extracted_info
        document.hasExtractedLicensingInfos.append(extracted_info)

    def convert(l):
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
            return spdx_license

        try:
            spdx_license = existing[l]
        except KeyError:
            spdx_license = "LicenseRef-" + l
            add_extracted_license(spdx_license, l)

        return spdx_license

    lic_split = lic.replace("(", " ( ").replace(")", " ) ").replace("|", " | ").replace("&", " & ").split()

    return ' '.join(convert(l) for l in lic_split)

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

                # TODO: Rework when License Profile implemented
                #if "SOURCE" in spdx_file.fileTypes:
                #    extracted_lics = extract_licenses(filepath)
                #    if extracted_lics:
                #        spdx_file.licenseInfoInFiles = extracted_lics

                doc.element.append(spdx_file)

                doc.add_relationship(spdx_pkg, "contains", spdx_file)

                spdx_files.append(spdx_file)
                file_counter += 1

    return spdx_files


def add_package_sources_from_debug(d, package_doc, spdx_package, package, package_files, sources):
    from pathlib import Path
    import oe.packagedata
    import oe.spdx3

    debug_search_paths = [
        Path(d.getVar('PKGD')),
        Path(d.getVar('STAGING_DIR_TARGET')),
        Path(d.getVar('STAGING_DIR_NATIVE')),
        Path(d.getVar('STAGING_KERNEL_DIR')),
    ]

    pkg_data = oe.packagedata.read_subpkgdata_extended(package, d)

    if pkg_data is None:
        return

    for file_path, file_data in pkg_data["files_info"].items():
        if not "debugsrc" in file_data:
            continue

        for pkg_file in package_files:
            if file_path.lstrip("/") == pkg_file.name.lstrip("/"):
                break
        else:
            bb.fatal("No package file found for %s in %s; SPDX found: %s" % (str(file_path), package,
                " ".join(p.name for p in package_files)))
            continue

        for debugsrc in file_data["debugsrc"]:
            ref_id = None
            for search in debug_search_paths:
                if debugsrc.startswith("/usr/src/kernel"):
                    debugsrc_path = search / debugsrc.replace('/usr/src/kernel/', '')
                else:
                    debugsrc_path = search / debugsrc.lstrip("/")
                if not debugsrc_path.exists():
                    continue

                file_sha256 = bb.utils.sha256_file(debugsrc_path)

                if file_sha256 in sources:
                    source_file = sources[file_sha256]
                    doc_ref = package_doc.find_external_map(source_file.doc.documentNamespace)
                    if doc_ref is None:
                        doc_ref = oe.spdx3.SPDX3ExternalMap()
                        doc_ref.externalId = "DocumentRef-dependency-" + source_file.doc.name
                        doc_ref.verifiedUsing = oe.spdx3.SPDX3Hash()
                        doc_ref.verifiedUsing.algorithm = "sha1"
                        doc_ref.verifiedUsing.hashValue = source_file.doc_sha1
                        doc_ref.definingDocument = source_file.doc.documentNamespace

                        package_doc.imports.append(doc_ref)

                    ref_id = "%s:%s" % (doc_ref.externalId, source_file.file.spdxId)
                else:
                    bb.debug(1, "Debug source %s with SHA256 %s not found in any dependency" % (str(debugsrc_path), file_sha256))
                break
            else:
                bb.debug(1, "Debug source %s not found" % debugsrc)

            relation_id = package_doc.add_relationship(ref_id, "generates", pkg_file)
            comment = oe.spdx3.SPDX3Annotation()
            comment.subject = relation_id
            comment.annotationType = "other"
            comment.statement = "debugsrc"
            package_doc.element.append(comment)

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
        dep_recipe_ref.externalId = "DocumentRef-%s" % spdx_dep_doc["name"]
        hashSha1 = oe.spdx3.SPDX3Hash()
        hashSha1.algorithm = "sha1"
        hashSha1.hashValue = spdx_dep_sha1
        dep_recipe_ref.verifiedUsing.append(hashSha1)

        doc.imports.append(dep_recipe_ref)
        doc.add_relationship("%s:%s" % (dep_recipe_ref.externalId, spdx_dep_recipe["spdxId"]), "buildDependency", spdx_recipe)

    return dep_recipes

collect_dep_recipes[vardepsexclude] = "SSTATE_ARCHS"

def collect_dep_sources(d, dep_recipes):
    import oe.sbom
    import oe.spdx3

    sources = {}
    for dep in dep_recipes:
        # Don't collect sources from native recipes as they
        # match non-native sources also.
        if hasattr(dep.doc, "element"):
            for element in dep.doc.element:
                if isinstance(element, oe.spdx3.SPDX3Annotation) \
                and element.subject == dep.recipe.spdxId \
                and element.statement == "isNative":
                    continue

        recipe_files = []

        if hasattr(dep.doc, "element"):
            for element in dep.doc.element:
                if isinstance(element, oe.spdx3.SPDX3Relationship) and element._from == dep.recipe.spdxId and element.relationshipType == "contains":
                    recipe_files = element.to

            for element in dep.doc.element:
                if isinstance(element, oe.spdx3.SPDX3File) \
                and element.spdxId not in recipe_files \
                and (element.primaryPurpose == "source" or "source" in element.additionalPurpose):
                    for checksum in element.verifiedUsing:
                        if algorithm in checksum.properties() \
                        and checksum.algorithm == "sha256":
                            sources[checksum.hashValue] = oe.sbom.DepSource(dep.doc, dep.doc_sha1, dep.recipe, spdx_file)
                            break

    return sources

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
            package.spdxId = oe.sbom.get_download_spdxid(d, download_idx + 1)

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

            doc.add_relationship(doc, "describes", package)
            doc.add_relationship(package, "buildDependency", recipe)


def collect_direct_deps(d, dep_task):

    deps = set()

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
    generate_creationInfo(d, doc)

    recipe = oe.spdx3.SPDX3Package()
    recipe.spdxId = oe.sbom.get_recipe_spdxid(d)
    recipe.name = d.getVar("PN")
    recipe.packageVersion = d.getVar("PV")
    recipe.suppliedBy.append(get_supplier(d, doc))

    if bb.data.inherits_class("native", d) or bb.data.inherits_class("cross", d):
        comment = oe.spdx3.SPDX3Annotation()
        comment.annotationType = "other"
        comment.subject = recipe.spdxId
        comment.statement = "isNative"

        doc.element.append(comment)

    homepage = d.getVar("HOMEPAGE")
    if homepage:
        recipe.homePage = homepage
# TODO: Rework when License Profile implemented
#    license = d.getVar("LICENSE")
#    if license:
#        recipe.licenseDeclared = convert_license_to_spdx(license, doc, d)

    summary = d.getVar("SUMMARY")
    if summary:
        recipe.summary = summary

    description = d.getVar("DESCRIPTION")
    if description:
        recipe.description = description

    if d.getVar("SPDX_CUSTOM_ANNOTATION_VARS"):
        for var in d.getVar('SPDX_CUSTOM_ANNOTATION_VARS').split():
            recipe.annotations.append(create_annotation(d, var + "=" + d.getVar(var)))

    # TODO: CVE handling

    doc.element.append(recipe)

    doc.add_relationship(doc, "describes", recipe)

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
                lambda file_counter: "SPDXRef-SourceFile-%s-%d" % (d.getVar("PN"), file_counter),
                lambda filepath: ["source"],
                ignore_dirs=[".git"],
                ignore_top_level_dirs=["temp"],
                archive=archive,
            )

            if archive is not None:
                recipe.packageFileName = str(recipe_archive.name)

    dep_recipes = collect_dep_recipes(d, doc, recipe)

    doc_sha1 = oe.sbom.write_doc(d, doc, doc, d.getVar("SSTATE_PKGARCH"), "recipes", indent=get_json_indent(d))
    dep_recipes.append(oe.sbom.DepRecipe(doc, doc_sha1, recipe))

    #TODO: references

    sources = collect_dep_sources(d, dep_recipes)
#    found_licenses = {license.name:recipe_ref.externalDocumentId + ":" + license.licenseId for license in doc.hasExtractedLicensingInfos}

    if not recipe_spdx_is_native(d, recipe):
        bb.build.exec_func("read_subpackage_metadata", d)

        pkgdest = Path(d.getVar("PKGDEST"))
        for package in d.getVar("PACKAGES").split():
            if not oe.packagedata.packaged(package, d):
                continue

            doc = oe.spdx3.SPDX3SpdxDocument()
            pkg_name = d.getVar("PKG:%s" % package) or package
            doc.name = pkg_name
            doc.documentNamespace = get_doc_namespace(d, doc)
            generate_creationInfo(d, doc)

            # TODO: Rework when License Profile implemented
            # package_doc.creationInfo.licenseListVersion = d.getVar("SPDX_LICENSE_DATA")["licenseListVersion"]
            # package_doc.externalDocumentRefs.append(recipe_ref)

            package_license = d.getVar("LICENSE:%s" % package) or d.getVar("LICENSE")

            spdx_package = oe.spdx3.SPDX3Package()

            spdx_package.spdxId = oe.sbom.get_package_spdxid(pkg_name)
            spdx_package.name = pkg_name
            spdx_package.packageVersion = d.getVar("PV")
            # TODO: Rework when License Profile implemented
            #spdx_package.licenseDeclared = convert_license_to_spdx(package_license, package_doc, d, found_licenses)
            spdx_package.suppliedBy = [ d.getVar("SPDX_SUPPLIER") ]

            doc.element.append(spdx_package)

            doc.add_relationship(recipe, "generates", spdx_package)
            doc.add_relationship(doc, "describes", spdx_package)

            package_archive = deploy_dir_spdx / "packages" / (doc.name + ".tar.zst")
            with optional_tarfile(package_archive, archive_packaged) as archive:
                package_files = add_package_files(
                    d,
                    doc,
                    spdx_package,
                    pkgdest / package,
                    lambda file_counter: oe.sbom.get_packaged_file_spdxid(pkg_name, file_counter),
                    lambda filepath: ["executable"],
                    ignore_top_level_dirs=['CONTROL', 'DEBIAN'],
                    archive=archive,
                )

                if archive is not None:
                    spdx_package.packageFileName = str(package_archive.name)

            add_package_sources_from_debug(d, doc, spdx_package, package, package_files, sources)

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
    # TODO: implement for SPDX3
    return
}

do_create_runtime_spdx[vardepsexclude] += "OVERRIDES"

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
    return
}

python sdk_host_combine_spdx() {
    return
}

python sdk_target_combine_spdx() {
    return
}
