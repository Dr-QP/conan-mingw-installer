from conans import ConanFile, CMake
import os


channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "anton-matosov")


class ConanarduinosdkTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "mingw-installer/0.1@%s/%s" % (username, channel)

    def test(self):
        self.output.success("Done")
