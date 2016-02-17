#!/usr/bin/python

from iniparser import IniParser

inifile = IniParser()
eclipse_version= inifile.getValue("settings-eclipse.ini", "Run", "eclipse_version")

print eclipse_version

#menu
file_menu = 'File'
project_menu = 'Project'
run_menu='Run'
yocto_project_tools_menu = 'YoctoProjectTools'
window_menu = 'Window'
help_menu = 'Help'
new_menu = 'New'
targetprofiles_menu = 'Target Profiles'
externaltools_menu = 'External Tools'
openperspective_menu = 'Open Perspective'

### menu item
preferences_item = 'Preferences'
project_item = 'Project...'
changeYPsettings_item = 'Change Yocto Project Settings'
closeperspective_item = 'Close Perspective'
direct_item = 'Direct'
buildproject_item = 'Build Project'
qemu_item = '1 qemu_i586-poky-linux'
qemu2_item = '2 qemu_i586-poky-linux'
runconfiguration_item = 'Run Configurations...'
debugconfiguration_item = 'Debug Configurations...'
other_item = 'Other...'
bitbakerecipe_item = 'BitBake Recipe'
installnewsoftware_item = 'Install New Software...'
search_item = 'Search'
launchHob_item = 'Launch HOB'
launchToaster_item = 'Launch Toaster'
restart_item = 'Restart'
exit_item = 'Exit'

### button
cancel_button = 'Cancel'
apply_button = 'Apply'
ok_button = 'OK'
saveAs_button = 'Save as ...'
finish_button = 'Finish'
yes_button = 'Yes'
rename_button = 'Rename'
remove_button = 'Remove'
continue_button = 'Continue'
new_button = 'New...'
run_button = 'Run'
debug_button = 'Debug'
populate_button = 'Populate...'
add_button = 'Add...'
selectall_button = 'Select All'
details_button = '<< Details'
new2_button = 'New'
close_button= 'Close'

### radio button


### role name
menu_rolename = 'menu'
menuitem_rolename = 'menu item'
frame_rolename = 'frame'
text_rolename = 'text'
tablecell_rolename = 'table cell'
button_rolename = 'push button'
combobox_rolename = 'combo box'
radiobutton_rolename = 'radio button'
treetable_rolename = 'tree table'
radio_menu_item_rolename = 'radio menu item'
checkbox_rolename = 'check box'
togglebutton_rolename = 'toggle button'
label_rolename='label'




### frame
worspacelauncher_frame = 'Workspace Launcher '
preferences_frame = 'Preferences '
saveAs_frame = 'Save as new cross development profile '
new_project_frame = 'New Project '
open_perspective_frame = 'Open Associated Perspective? '
update_frame = 'Update cross development profile '
rename_frame = 'Rename cross development profile '
remove_frame = 'Remove cross development profile '
delete_frame = 'Delete Resources '
runconfiguration_frame = 'Run Configurations '
newconnection_frame = 'New Connection '
enterpassword_frame = 'Enter Password '
warning_frame = 'Warning '
projectproperties_frame = 'Properties for '
debugconfiguration_frame = 'Debug Configurations '
confirmperspectiveswitch_frame = 'Confirm Perspective Switch '
openp_other_erspective_frame = 'Open Perspective '
yoctoBBcommander_frame = 'Yocto Project BitBake Commander '
problemoccurred_frame = 'Problem Occurred '
install_frame = 'Install '
addrepository_frame = 'Add Repository '
securitywarning_frame = 'Security Warning '
softwareupdates_frame = 'Software Updates '
gdbserverdebugger_frame = 'gdbserver debugger '
launchHob_frame = 'Launch HOB '
launchToaster_frame = 'Launch Toaster'

###table cell
YP_ADT_tablecell = 'Yocto Project ADT'
general_tablecell = 'General'
executable_tablecell = 'Executable'
YPADT_AutotoolsP_tablecell = 'Yocto Project ADT Autotools Project'
reconfigureproject_tablecell = 'Reconfigure Project - Run configuration scripts for project'
console_tablecell = 'Console'
ssh_tablecell = 'SSH Only'
cansi_tablecell = 'Hello World ANSI C Autotools Project'
cgtk_tablecell = 'Hello World GTK C Autotools Project'
cplusansi_tablecell  = 'Hello World C++ Autotools Project'
cremote_tablecell = 'C/C++ Remote Application'

### tree table
projecttype_treetable = 'Project type:'

### description
clear_console_description = 'Clear Console'

###posible errors gdb
error_connection_closed = 'Remote connection closed'

if eclipse_version=="kepler":
    next_button = '&Next  '
    acceptterms_button = "I accept the terms of the license agreement"

elif eclipse_version=="luna":
    next_button = '&Next  '
    acceptterms_button = "I accept the terms of the license agreement"

elif eclipse_version=="mars":
    next_button = 'Next >'
    perspective_menu = "Perspective"
    acceptterms_button = "I accept the terms of the license agreements"
else:
    print "nasol"


### linux tools

perf_item = "perf"
perf_frame ="Perf   "

powertop_item = 'powertop'
powertop_frame = 'Powertop '