#
# Whether the platform supports kernel tracing
#
LTTNGMODULES = "lttng-modules"
LTTNGMODULES_arc = ""
LTTNGMODULES:riscv64 = ""

COMPATIBLE_HOST:riscv64:pn-lttng-modules = "null"
COMPATIBLE_HOST_arc:pn-lttng-modules = "null"

# Whether the platform supports userspace tracing
# lttng-ust uses sched_getcpu() which is not there on for some platforms.
LTTNGUST = "lttng-ust"
LTTNGUST_arc = ""

COMPATIBLE_HOST_arc:pn-lttng-ust = "null"

