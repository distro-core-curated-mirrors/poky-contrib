SUMMARY = "An implementation of JSON Schema validation for Python"
HOMEPAGE = "https://github.com/Julian/jsonschema"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING;md5=7a60a81c146ec25599a3e1dabb8610a8 \
                    file://json/LICENSE;md5=9d4de43111d33570c8fe49b4cb0e01af"

SRC_URI[sha256sum] = "636694eb41b3535ed608fe04129f26542b59ed99808b4f688aa32dcf55317a83"

inherit pypi python3-dir

DEPENDS += "${PYTHON_PN}-vcversioner-native ${PYTHON_PN}-setuptools-scm-native"
DEPENDS += "python3-build-native python3-installer-native python3-pep517-native python3-setuptools-native python3-setuptools-scm-native python3-wheel-native"

PACKAGECONFIG ??= "format"
PACKAGECONFIG[format] = ",,,\
    ${PYTHON_PN}-idna \
    ${PYTHON_PN}-jsonpointer \
    ${PYTHON_PN}-webcolors \
    ${PYTHON_PN}-rfc3987 \
    ${PYTHON_PN}-strict-rfc3339 \
"
PACKAGECONFIG[nongpl] = ",,,\
    ${PYTHON_PN}-idna \
    ${PYTHON_PN}-jsonpointer \
    ${PYTHON_PN}-webcolors \
    ${PYTHON_PN}-rfc3986-validator \
    ${PYTHON_PN}-rfc3339-validator \
"

RDEPENDS:${PN} += " \
    ${PYTHON_PN}-attrs \
    ${PYTHON_PN}-core \
    ${PYTHON_PN}-datetime \
    ${PYTHON_PN}-importlib-metadata \
    ${PYTHON_PN}-io \
    ${PYTHON_PN}-json \
    ${PYTHON_PN}-netclient \
    ${PYTHON_PN}-numbers \
    ${PYTHON_PN}-pkgutil \
    ${PYTHON_PN}-pprint \
    ${PYTHON_PN}-pyrsistent \
    ${PYTHON_PN}-shell \
    ${PYTHON_PN}-six \
    ${PYTHON_PN}-unittest \
    ${PYTHON_PN}-setuptools-scm \
    ${PYTHON_PN}-zipp \
"

do_compile() {
    nativepython3 -m build --wheel --no-isolation
}

do_install:prepend() {                                                                                                                            
    cat > ${S}/install-it.py << EOF                                                                                                               
from installer import install                                                                                                                     
from installer.destinations import SchemeDictionaryDestination                                                                                    
from installer.sources import WheelFile                                                                                                           
                                                                                                                                                  
sysconfig_paths={'stdlib': '${D}${libdir}/${PYTHON_DIR}', 'platstdlib': '${D}${libdir}/${PYTHON_DIR}', 'purelib': '${D}${PYTHON_SITEPACKAGES_DIR}'
, 'platlib': '${D}${PYTHON_SITEPACKAGES_DIR}', 'include': '${D}${incdir}/${PYTHON_DIR}', 'platinclude': '${D}${incdir}/${PYTHON_DIR}', 'scripts': 
'${D}${bindir}', 'data': '${D}${exec_prefix}'}                                                                                                    
                                                                                                                                                  
destination = SchemeDictionaryDestination(                                                                                                        
    sysconfig_paths,                                                                                                                              
    interpreter="${STAGING_BINDIR_NATIVE}/python3-native/python3",                                                                                
    script_kind="posix",                                                                                                                          
)                                                                                                                                                 
                                                                                                                                                  
with WheelFile.open("dist/${PYPI_PACKAGE}-${PV}-py3-none-any.whl") as source:                                                                 
    install(                                                                                                                                      
        source=source,                                                                                                                            
        destination=destination,                                                                                                                  
        additional_metadata={                                                                                                                     
            "INSTALLER": b"python3-installer-0.4.0",                                                                                              
        },                                                                                                                                        
    )                                                                                                                                             
EOF                                                                                                                                               
}

do_install() {
    ${STAGING_BINDIR_NATIVE}/python3-native/python3 ${S}/install-it.py
}

FILES:${PN} += "\
    ${PYTHON_SITEPACKAGES_DIR}/${PYPI_PACKAGE}-${PV}.dist-info* \
    ${PYTHON_SITEPACKAGES_DIR}/${PYPI_PACKAGE}/* \
"

BBCLASSEXTEND = "native nativesdk"
