from conan.packager import ConanMultiPackager
import copy


if __name__ == "__main__":
    builder = ConanMultiPackager()
    base = {"os": "Windows", "compiler": "gcc", "compiler.version": "7.1",
            "compiler.exception": "seh", "compiler.libcxx": "libstdc++",
            "compiler.threads": "posix"}
    versionsToUpload = ["4.9", "5.4", "6.3", "7.1"]
    versionsToBuildOnly = ["4.8", "6.2"]
    for version in versionsToUpload + versionsToBuildOnly:
        tmp = copy.copy(base)
        tmp["compiler.version"] = version
        for th in ["posix", "win32"]:
            tmp2 = copy.copy(tmp)
            tmp2["compiler.threads"] = th
            for ex in ["seh", "sjlj"]:
                tmp3 = copy.copy(tmp2)
                tmp3["compiler.exception"] = ex
                builder.add(tmp3, {}, {}, {}, upload=(version in versionsToUpload))
    
    builder.run()
