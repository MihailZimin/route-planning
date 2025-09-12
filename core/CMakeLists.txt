project(core VERSION 0.1 LANGUAGES CXX)

set(PROJECT_SOURCES
        data.cpp
        data.h
)

add_library(core SHARED ${PROJECT_SOURCES})
