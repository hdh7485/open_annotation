cmake_minimum_required(VERSION 3.5)
project(open_annotation )
find_package( OpenCV REQUIRED )
add_executable( open_annotation main.cpp )
target_link_libraries( open_annotation ${OpenCV_LIBS} )
