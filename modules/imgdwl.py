import os, urllib, sgmllib, re, sys, fnmatch
from base import basic_functionality, TestParams as TP
from pokyconfig import Config
from IPython import embed

class URLParser(sgmllib.SGMLParser):
    "A simple parser class."

    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."
        sgmllib.SGMLParser.__init__(self, verbose)
        self.hyperlinks = list()

    def start_a(self, attributes):
        "Process a hyperlink and its 'attributes'."
        for name, value in attributes:
            if name == "href":
                self.hyperlinks.append(value)

    def get_hyperlinks(self):
        "Return the list of hyperlinks."
        return self.hyperlinks


class OnlineDwl(basic_functionality):
    def __init__(self):
        """
        """
        super(OnlineDwl, self).__init__()
        self.cfg = Config()
        self.url = self.create_link(self.release)
        self.proxies = [None, dict()][self.test_type != 'generic']


    def create_link(self, release):
        if self.test_type == "generic":
            base_url = self.cfg.get_cfg_param("generic_URL", "GENERAL")
            url = base_url.format(release, self.bsp)
        elif self.test_type == "meta-intel":
            base_url = self.cfg.get_cfg_param("mi_URL","GENERAL")
            url = base_url.format(release, self.bsp)
        elif self.test_type == "wic_local":
            base_url = self.cfg.get_cfg_param("wic_local_URL", "GENERAL")
            url = base_url.format(release, self.bsp)
        elif self.test_type == "wic_AB":
            base_url = self.cfg.get_cfg_param("wic_AB_URL", "GENERAL")
            url = base_url.format(self.bsp, self.core_name)
        else:
            pass # didn't figure it out if i want an err mess here
        return url


    def interogate_page(self):
        fl = urllib.urlopen(self.url, proxies=self.proxies) # skipping proxy if not test-type= generic
        page_content = fl.read()
        fl.close()
        # this is where the magic is
        url_parser = URLParser()
        url_parser.parse(page_content)
        return url_parser.get_hyperlinks()

    def check_for_artifacts(self, artifact):
        """
        will return the artifact(manifest or hddimg or whatever needed) name used to download later on
        """

        url_content = self.interogate_page()
        #print url_content
        if artifact in url_content:
            print "Artifact {} found on {}".format(artifact, self.url)
            return artifact
        else:
            print "Artifact {} NOT found on {}.".format(artifact, self.url)
            return ""


    def dwl_artifacts(self, artifact_type):
        """
        This function will download the image from AB on local BUILD dir and after
        will transfer it to the USB_SW machine to be written on USB stick
        It also takes the .manifest file
        """
        #embed()
        if not os.path.exists(self.dwl_dir):
            os.makedirs(self.dwl_dir)

        dwl_handler = urllib.URLopener(proxies=self.proxies)
        if artifact_type == "manifest":
            manifest_file = "{}-{}.manifest".format(self.core_name, self.bsp)
            manifest_file = self.check_for_artifacts(manifest_file)
            if manifest_file:
                dest_manifest_file = os.path.join(self.dwl_dir, manifest_file)
                dwl_handler.retrieve(self.url + manifest_file, dest_manifest_file)
                return True

        elif artifact_type == "hddimg":
            hddimg_file = "{}-{}.hddimg".format(self.core_name, self.bsp)
            hddimg_file = TP.img_file = self.check_for_artifacts(hddimg_file)
            if not hddimg_file:
                sys.exit("No test can be done without an image to write on a board."
                         "Please check the link from where to download is correct.")
            if hddimg_file:
                dest_image_file = os.path.join(self.dwl_dir, hddimg_file)
                print "Downloading image: {}".format(hddimg_file)
                dwl_handler.retrieve(self.url + hddimg_file, dest_image_file)
                return True

        elif artifact_type == "direct":
            self.check_for_artifacts("directdisk-201603081424-sda.direct")
        return False


class UseImage(basic_functionality):
    def __init__(self):
        super(UseImage, self).__init__()

    def send_img_to_USB_SW(self):
        #img_file, manifest_file = self.check_for_image()
        USB_SW_img_dir = Config.get_cfg_param("remote_img_dir", "USB-SW")
        if self.retest == 'Yes':
            self.img_file = "{}-{}.hddimg".format(self.core_name, self.bsp)
        image_file = os.path.join(self.dwl_dir, self.img_file)
        scp_command = "scp %s root@%s:%s" % (image_file , self.SW_ip, USB_SW_img_dir)
        res = self.run_comamd_locally(scp_command)
        return res


    def write_image_on_stick(self):
        stick = TP.stick = self.rezerve_stick().strip()
        print "Selected stick: {}".format(stick)
        command = "/root/USB_SW/image_on_stick.sh {} {}".format(self.img_file, stick)
        result = self.run_command_remotelly(self.SW_ip,command)
        return result.exit_code
