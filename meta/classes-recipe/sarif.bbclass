TARGET_CFLAGS:append = " -fdiagnostics-format=sarif-file"

# writes <source>.sarif files into source tree
# can use https://github.com/microsoft/sarif-tools to generate reports
# but does not include the source fragment that gcc writes?
