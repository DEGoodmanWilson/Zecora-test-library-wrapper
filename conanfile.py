#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibtestzecoraConan(ConanFile):
    name = "libtestzecora"
    version = "0.1.0"
    description = "Keep it short"
    url = "https://github.com/DEGoodmanWilson/Zecora-test-library-wrapper"
    homepage = "https://github.com/DEGoodmanWilson/Zecora-test-target-library"
    author = "Bincrafters <bincrafters@gmail.com>"
    # Indicates License type of the packaged library
    license = "MIT"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/DEGoodmanWilson/Zecora-test-target-library"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version), sha256="557536a329dbebc381d0875ba2c7830ae49edd19e7a18d88a275aa01b1b4d7b5")
        extracted_dir = "Zecora-test-target-library" + "-" + self.version

        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE*", dst="licenses", src=self._source_subfolder)

        # cmake installs all the files
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
