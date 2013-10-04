# Add SOC_FAMILY to machine overrides so we get access to e.g. 'omap3' and 'ti335x'
<<<<<<< HEAD
MACHINEOVERRIDES =. "${@['', '${SOC_FAMILY}:']['${SOC_FAMILY}' != '']}"
=======
MACHINEOVERRIDES .= "${@['', ':${SOC_FAMILY}']['${SOC_FAMILY}' != '']}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
