project(PackageTest CXX)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(example example.cpp)
target_link_libraries(example ${CONAN_LIBS})

find_package(X11 REQUIRED)
message("${X11_INCLUDE_DIR}")
include_directories(${X11_INCLUDE_DIR})
