import os

from collections import namedtuple

from conans import ConanFile, tools, __version__ as conan_version
from conans.model.version import Version


class MingwInstallerConan(ConanFile):
    name = "mingw_installer"
    version = "1.0"
    license = "http://www.mingw.org/license"
    url = "http://github.com/lasote/conan-mingw-installer"

    if conan_version < Version("0.99"):
        os_name = "os"
        arch_name = "arch"
    else:
        os_name = "os_build"
        arch_name = "arch_build"

    settings = {os_name: ["Windows"],
                arch_name: ["x86", "x86_64"],
                "compiler": {"gcc": {"version": None,
                                     "libcxx": ["libstdc++", "libstdc++11"],
                                     "threads": ["posix", "win32"],
                                     "exception": ["dwarf2", "dwarf", "sjlj", "seh"]}}}

    description = 'MinGW, a contraction of "Minimalist GNU for Windows", ' \
                  'is a minimalist development environment for native Microsoft' \
                  ' Windows applications.'
    build_requires = "7z_installer/1.0@conan/stable"
    build_policy = "missing"

    @property
    def arch(self):
        return self.settings.get_safe("arch_build") or self.settings.get_safe("arch")

    def build(self):
        self.output.info("Updating MinGW List ... please wait.")

        installer = get_best_installer(str(self.arch),
                                       str(self.settings.compiler.threads),
                                       str(self.settings.compiler.exception),
                                       str(self.settings.compiler.version))

        self.output.info("Downloading: %s" % installer.url)
        tools.download(installer.url, "file.7z")
        self.run("7z x file.7z")

    def package(self):
        self.copy("*", dst="", src="mingw32")
        self.copy("*", dst="", src="mingw64")

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
        self.env_info.MINGW_HOME = str(self.package_folder)
        self.env_info.CONAN_CMAKE_GENERATOR = "MinGW Makefiles"
        self.env_info.CXX = os.path.join(self.package_folder, "bin", "g++.exe")
        self.env_info.CC = os.path.join(self.package_folder, "bin", "gcc.exe")


class Installer(namedtuple("Installer", "version arch threads exception revision url")):

    def __new__(cls, raw_data):
        version, arch, threads, exception, revision, url = [x.strip() for x in raw_data.split('|')]
        version = Version(version)
        revision = int(revision[3:])
        return cls.__bases__[0].__new__(cls, version, arch, threads, exception, revision, url)


repository_file = 'https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win32/' \
                      'Personal%20Builds/mingw-builds/installer/repository.txt/download'


def get_best_installer(arch, threads, exception, version):

    if arch == "x86":
        arch = "i686"
        
    if exception == "dwarf2":
        exception = "dwarf"

    tools.download(repository_file, "repository.txt", overwrite=True)

    installers = []
    with open("repository.txt") as f:
        for line in f.readlines():
            installers.append(Installer(line))

    version = Version(version)
    def params_match(i):
        return arch == i.arch and threads == i.threads and exception == i.exception

    def better_choice(i):
        return not best_match or i.version > best_match.version or (i.version == best_match.version and i.revision > best_match.revision)

    best_match = None
    for i in installers:
        if len(version.as_list) == 1:
            if i.version.major() == version.major() and params_match(i) and better_choice(i):
                best_match = i
        elif len(version.as_list) == 2:
            if i.version.major() == version.major() and i.version.minor() == version.minor() and params_match(i) and better_choice(i):
                best_match = i
        elif len(version.as_list) == 3:
            if i.version == version and params_match(i) and better_choice(i):
                best_match = i

    if not best_match:
        raise Exception("There is no suitable MinGW release for the requested features.")
    else:
        return best_match

if __name__ == "__main__":

    installer = get_best_installer("x86", "posix", "sjlj", "4")
    assert(installer.version == "4.9.4")

    installer = get_best_installer("x86", "posix", "sjlj", "4.9")
    assert (installer.version == "4.9.4")

    installer = get_best_installer("x86", "posix", "sjlj", "4.9.3")
    assert (installer.version == "4.9.3")

    installer = get_best_installer("x86", "posix", "sjlj", "5")
    assert (installer.version == "5.4.0")

    installer = get_best_installer("x86", "posix", "sjlj", "5.4")
    assert (installer.version == "5.4.0")

    installer = get_best_installer("x86", "posix", "sjlj", "5.4.0")
    assert (installer.version == "5.4.0")

    installer = get_best_installer("x86", "posix", "sjlj", "5.2.0")
    assert (installer.version == "5.2.0")
    assert (installer.revision == 1)
