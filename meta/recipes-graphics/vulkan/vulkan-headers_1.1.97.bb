SUMMARY = "Vulkan Header files and API registry"
HOMEPAGE = "https://www.khronos.org/vulkan/"
BUGTRACKER = "https://github.com/KhronosGroup/Vulkan-Headers"
SECTION = "libs"

LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=3b83ef96387f14655fc854ddc3c6bd57" 
SRC_URI = "git://github.com/KhronosGroup/Vulkan-Headers.git;nobranch=1"
SRCREV = "c200cb25db0f47364d3318d92c1d8e9dfff2fef1"
UPSTREAM_CHECK_GITTAGREGEX = "sdk-(?P<pver>\d+(\.\d+)+)"

S = "${WORKDIR}/git"

inherit cmake lib_package

FILES_${PN} += " \
  /usr/share \
  /usr/share/vulkan \
  /usr/share/vulkan/registry \
  /usr/share/vulkan/registry/validusage.json \
  /usr/share/vulkan/registry/reg.py \
  /usr/share/vulkan/registry/genvk.py \
  /usr/share/vulkan/registry/vk.xml \
  /usr/share/vulkan/registry/generator.py \
  /usr/share/vulkan/registry/cgenerator.py \
"
