import os
from time import sleep
from oeqa.oetest import oeRuntimeTest
from oeqa.utils.decorators import TestNeedsBin

class mytest(oeRuntimeTest):

############### A simple test for the DUT ######################

    @TestNeedsBin(("hello-dut","rm"),
                  ("hello-test","rm"),
                  ("hello-test","rpm","rm"),
                  ("hello-dut","rpm"),
                  ("hello","native")
                  )
    def test_hello_on_DUT_3(self):
         (status, output) = self.target.run("hello")
         self.a=5
         print("For hello: " + str(output) + "\n")
         (status1,output1) = self.target.run("hello-test")
         print("For hello-test: " + str(output1) + "\n")
         self.assertEqual(status, 0, "failed for hello")
         self.assertEqual(status1, 0, "failed for hello-test")

       
