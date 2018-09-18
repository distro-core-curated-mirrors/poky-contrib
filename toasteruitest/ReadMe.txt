Before running toaster test case, we need to have following pre-requisite:

Pre-requisite: -
a) To run toaster follow below step:
1.Fetch the source code for yocto
git clone http://git.yoctoproject.org/git/poky

2. run below command to initiate build environment
source oe-init-build-env

3. Install the basic requirement for Toaster with the below given command-
sudo pip3 install -r <Location-of-toaster-file(toaster-requirements.txt)>
Example- sudo pip3 install -r /home/…. /poky/bitbake/toaster-requirements.txt

4. Start the toaster
source toaster start

b) To install selenium
$ sudo apt-get install scrot python-pip
$ sudo pip install selenium

c) To test with Chrome browser and chromedriver
Download/install chrome on host
Download chromedriver from https://code.google.com/p/chromedriver/downloads/list  according to your host type
put chromedriver in PATH, (e.g. /usr/bin/, provide permission to chromedriver)
set path for chromedriver
export path=$PATH:/usr/bin/chromedriver

d) Necessary images to be built
1) core-image-minimal
2) core-image-sato
while  building if it gives error please install other dependencies like gawk,chrpath,texinfo etc.

e) Please copy contrib file as attached  on path "poky/bitbake/lib/toaster"

f)  Please copy toasteruitest directory into  poky/bitbake/lib/toaster
then goto 
"poky/bitbake/lib/toaster/toasteruitest" and run  "./run_toastertests.py" from that location.


NOTE:  
1) Make sure your system  should not be in locked/sleep mode at least for 1 hour.
2) Test case Number  900:  Its not included as all are manual steps and its time consuming for now, It will be included in future release.
3) Test case Number 955,951: Since Ctrl+C is not working (bug id:12813)so that portion is not implemented as of now.
