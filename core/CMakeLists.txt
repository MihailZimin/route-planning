project(core VERSION 0.1 LANGUAGES CXX)

set(PROJECT_SOURCES
        data.cpp
        data.h
)

add_library(core SHARED ${PROJECT_SOURCES})
set_target_properties(core PROPERTIES PUBLIC_HEADER data.h)
target_include_directories(core PUBLIC .)
