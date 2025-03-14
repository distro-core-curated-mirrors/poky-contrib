# auto detection instead of build time configured via SERIAL_CONSOLES
# to support multiple devices
PACKAGECONFIG:append:genericarm64 = " serial-getty-generator"
