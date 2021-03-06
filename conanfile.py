from conans import ConanFile, tools
from conans.tools import os_info
import os
import sys


class MinGWInstallerConan(ConanFile):
    name = "mingw-installer"
    version = "1.0.0"
    license = "MIT"
    url = "https://github.com/Dr-QP/conan-mingw-installer"
    description = "MinGW installer as a conan package"
    settings = {"os": ["Windows", "Arduino"]}
    options = {"threads": ["posix", "win32"],
               "exception": ["dwarf2", "sjlj", "seh"],
               "arch": ["x86", "x86_64"],
               "version": ["4.8", "4.9", "5.4", "6.2", "6.3", "7.1"]}
    default_options = "exception=seh", "threads=posix", "arch=x86_64", "version=6.3"
    build_policy = "missing"
    build_requires = "7z-installer/16.02@anton-matosov/testing"

    def configure(self):
        if (not os_info.is_windows):
            raise Exception(
                "MinGW toolchain can be used only on Windows directly")

        if (self.options.arch == "x86" and self.options.exception == "seh") or \
           (self.options.arch == "x86_64" and self.options.exception == "dwarf2"):
            raise Exception("Not valid %s and %s combination!" % (self.options.arch,
                                                                  self.options.exception))

    def package_id(self):
        # Toolchain doesn't really depend on OS settings, so package id should be platform agnostic
        self.info.settings.os = ""

    def build(self):
        keychain = "%s_%s_%s_%s" % (str(self.options.version).replace(".", ""),
                                    self.options.arch,
                                    self.options.exception,
                                    self.options.threads)
        files = {
            ############################################################################################################
            ###  4.8
            ############################################################################################################
            "48_x86_dwarf2_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.8.2/threads-posix/dwarf/i686-4.8.2-release-posix-dwarf-rt_v3-rev0.7z",
            "48_x86_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.8.2/threads-posix/sjlj/i686-4.8.2-release-posix-sjlj-rt_v3-rev0.7z",
            "48_x86_dwarf2_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.8.2/threads-win32/dwarf/i686-4.8.2-release-win32-dwarf-rt_v3-rev0.7z",
            "48_x86_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.8.2/threads-win32/sjlj/i686-4.8.2-release-win32-sjlj-rt_v3-rev0.7z",

            "48_x86_64_seh_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.8.2/threads-posix/seh/x86_64-4.8.2-release-posix-seh-rt_v3-rev0.7z",
            "48_x86_64_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.8.2/threads-posix/sjlj/x86_64-4.8.2-release-posix-sjlj-rt_v3-rev0.7z",
            "48_x86_64_seh_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.8.2/threads-win32/seh/x86_64-4.8.2-release-win32-seh-rt_v3-rev0.7z",
            "48_x86_64_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.8.2/threads-win32/sjlj/x86_64-4.8.2-release-win32-sjlj-rt_v3-rev0.7z",

            ############################################################################################################
            # 4.9
            ############################################################################################################
            "49_x86_dwarf2_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.9.2/threads-posix/dwarf/i686-4.9.2-release-posix-dwarf-rt_v3-rev1.7z",
            "49_x86_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.9.2/threads-posix/sjlj/i686-4.9.2-release-posix-sjlj-rt_v3-rev1.7z",
            "49_x86_dwarf2_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.9.2/threads-win32/dwarf/i686-4.9.2-release-win32-dwarf-rt_v3-rev1.7z",
            "49_x86_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/4.9.2/threads-win32/sjlj/i686-4.9.2-release-win32-sjlj-rt_v3-rev1.7z",

            "49_x86_64_seh_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.9.2/threads-posix/seh/x86_64-4.9.2-release-posix-seh-rt_v3-rev1.7z",
            "49_x86_64_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.9.2/threads-posix/sjlj/x86_64-4.9.2-release-posix-sjlj-rt_v3-rev1.7z",
            "49_x86_64_seh_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.9.2/threads-win32/seh/x86_64-4.9.2-release-win32-seh-rt_v3-rev1.7z",
            "49_x86_64_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/4.9.2/threads-win32/sjlj/x86_64-4.9.2-release-win32-sjlj-rt_v3-rev1.7z",


            ############################################################################################################
            ###  5.4
            ############################################################################################################
            "54_x86_dwarf2_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/5.4.0/threads-posix/dwarf/i686-5.4.0-release-posix-dwarf-rt_v5-rev0.7z",
            "54_x86_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/5.4.0/threads-posix/sjlj/i686-5.4.0-release-posix-sjlj-rt_v5-rev0.7z",
            "54_x86_dwarf2_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/5.4.0/threads-win32/dwarf/i686-5.4.0-release-win32-dwarf-rt_v5-rev0.7z",
            "54_x86_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/5.4.0/threads-win32/sjlj/i686-5.4.0-release-win32-sjlj-rt_v5-rev0.7z",

            "54_x86_64_seh_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/5.4.0/threads-posix/seh/x86_64-5.4.0-release-posix-seh-rt_v5-rev0.7z",
            "54_x86_64_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/5.4.0/threads-posix/sjlj/x86_64-5.4.0-release-posix-sjlj-rt_v5-rev0.7z",
            "54_x86_64_seh_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/5.4.0/threads-win32/seh/x86_64-5.4.0-release-win32-seh-rt_v5-rev0.7z",
            "54_x86_64_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/5.4.0/threads-win32/sjlj/x86_64-5.4.0-release-win32-sjlj-rt_v5-rev0.7z",


            ############################################################################################################
            ###  6.2
            ############################################################################################################
            "62_x86_dwarf2_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/6.2.0/threads-posix/dwarf/i686-6.2.0-release-posix-dwarf-rt_v5-rev1.7z",
            "62_x86_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/6.2.0/threads-posix/sjlj/i686-6.2.0-release-posix-sjlj-rt_v5-rev1.7z",
            "62_x86_dwarf2_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/6.2.0/threads-win32/dwarf/i686-6.2.0-release-win32-dwarf-rt_v5-rev1.7z",
            "62_x86_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/6.2.0/threads-win32/sjlj/i686-6.2.0-release-win32-sjlj-rt_v5-rev1.7z",

            "62_x86_64_seh_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.2.0/threads-posix/seh/x86_64-6.2.0-release-posix-seh-rt_v5-rev1.7z",
            "62_x86_64_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.2.0/threads-posix/sjlj/x86_64-6.2.0-release-posix-sjlj-rt_v5-rev1.7z",
            "62_x86_64_seh_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.2.0/threads-win32/seh/x86_64-6.2.0-release-win32-seh-rt_v5-rev1.7z",
            "62_x86_64_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.2.0/threads-win32/sjlj/x86_64-6.2.0-release-win32-sjlj-rt_v5-rev1.7z",


            ############################################################################################################
            ###  6.3
            ############################################################################################################
            "63_x86_dwarf2_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/6.3.0/threads-posix/dwarf/i686-6.3.0-release-posix-dwarf-rt_v5-rev1.7z",
            "63_x86_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/6.3.0/threads-posix/sjlj/i686-6.3.0-release-posix-sjlj-rt_v5-rev1.7z",
            "63_x86_dwarf2_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/6.3.0/threads-win32/dwarf/i686-6.3.0-release-win32-dwarf-rt_v5-rev1.7z",
            "63_x86_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/6.3.0/threads-win32/sjlj/i686-6.3.0-release-win32-sjlj-rt_v5-rev1.7z",

            "63_x86_64_seh_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.3.0/threads-posix/seh/x86_64-6.3.0-release-posix-seh-rt_v5-rev1.7z",
            "63_x86_64_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.3.0/threads-posix/sjlj/x86_64-6.3.0-release-posix-sjlj-rt_v5-rev1.7z",
            "63_x86_64_seh_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.3.0/threads-win32/seh/x86_64-6.3.0-release-win32-seh-rt_v5-rev1.7z",
            "63_x86_64_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/6.3.0/threads-win32/sjlj/x86_64-6.3.0-release-win32-sjlj-rt_v5-rev1.7z",


            ############################################################################################################
            ###  7.1
            ############################################################################################################
            "71_x86_dwarf2_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/7.1.0/threads-posix/dwarf/i686-7.1.0-release-posix-dwarf-rt_v5-rev1.7z",
            "71_x86_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/7.1.0/threads-posix/sjlj/i686-7.1.0-release-posix-sjlj-rt_v5-rev1.7z",
            "71_x86_dwarf2_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/7.1.0/threads-win32/dwarf/i686-7.1.0-release-win32-dwarf-rt_v5-rev1.7z",
            "71_x86_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/7.1.0/threads-win32/sjlj/i686-7.1.0-release-win32-sjlj-rt_v5-rev1.7z",

            "71_x86_64_seh_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/7.1.0/threads-posix/seh/x86_64-7.1.0-release-posix-seh-rt_v5-rev1.7z",
            "71_x86_64_sjlj_posix": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/7.1.0/threads-posix/sjlj/x86_64-7.1.0-release-posix-sjlj-rt_v5-rev1.7z",
            "71_x86_64_seh_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/7.1.0/threads-win32/seh/x86_64-7.1.0-release-win32-seh-rt_v5-rev1.7z",
            "71_x86_64_sjlj_win32": "http://downloads.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/7.1.0/threads-win32/sjlj/x86_64-7.1.0-release-win32-sjlj-rt_v5-rev1.7z",
        }

        tools.download(files[keychain], "file.7z")
        self.run("7z x file.7z")

    def package(self):
        self.copy("*", dst="", src="mingw32")
        self.copy("*", dst="", src="mingw64")

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.env_info.MINGW_HOME = str(self.package_folder)
        self.env_info.CONAN_CMAKE_GENERATOR = "MinGW Makefiles"
        self.env_info.CXX = os.path.join(self.package_folder, "bin", "g++.exe")
        self.env_info.CC = os.path.join(self.package_folder, "bin", "gcc.exe")
