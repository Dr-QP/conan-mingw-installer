from conan.packager import ConanMultiPackager
from conans.tools import os_info
import copy


class WindowsPackager(ConanMultiPackager):

    def add(self, options):
        if not self.is_bad_options(options):
            super(self.__class__, self).add(settings={
                "os": "Windows",
            }, options=self.mingw_options(options))

    def mingw_options(self, options):
        result = {}
        for name, value in options.iteritems():
            result["mingw-installer:" + name] = value
        return result

    def is_bad_options(self, options):
        return (options.get("arch") == "x86" and options.get("exception") == "seh") or \
            (options.get("arch") == "x86_64" and options.get("exception") == "dwarf2")


if __name__ == "__main__":
    # self.password = password or os.getenv("CONAN_PASSWORD", None)
    builder = WindowsPackager(args="--build missing")

    default_options = {
        "exception": "seh",
        "threads": "posix",
        "arch": "x86_64",
        "version": "6.3"
    }
    builder.add(default_options)

    # Build only default, because packages are pretty big (160MB per package)
    builder.run()
    builder.password = None # Clear password to prevent binaries upload

    possible_options = {"threads": ["posix", "win32"],
                        "exception": ["dwarf2", "sjlj", "seh"],
                        "arch": ["x86", "x86_64"],
                        "version": ["4.8", "4.9", "5.4", "6.2"]}

    build_options = [{}]
    for name, values in possible_options.iteritems():
        new_build_options = []
        for value in values:
            for options in build_options:
                new_options = copy.copy(options)
                new_options[name] = value
                new_build_options.append(new_options)
        build_options = new_build_options

    for p in build_options:
        builder.add(p)

    builder.run()
