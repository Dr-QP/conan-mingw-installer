from conan.packager import ConanMultiPackager
from conans.tools import os_info
import copy


class WindowsPackager(ConanMultiPackager):

    def add(self, options):
        super(self.__class__, self).add(settings={
            "os": "Windows",
        }, options=options)


if __name__ == "__main__":
    builder = WindowsPackager(args="--build missing")
    builder.add({})

    builder.run()
