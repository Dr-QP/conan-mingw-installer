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
    possible_options = {"threads": ["posix", "win32"],
                "exception": ["dwarf2", "sjlj", "seh"],
                "arch": ["x86", "x86_64"],
                "version": ["4.8", "4.9", "5.4", "6.2"]}

    bad_options = [{
        "arch": "x86",
        "exception": "seh"
    }, {
        "arch": "x86_64",
        "exception": "dwarf2"
    }]

    build_options = [{}]
    for name, values in possible_options.iteritems():
        new_build_options = []
        for value in values:
            for options in build_options:
                new_options = copy.copy(options)
                new_options[name] = value
                new_build_options.append(new_options)
        build_options = new_build_options

    print("Options list:")
    for p in build_options:
        print p
    # builder.add({})

    builder.run()
