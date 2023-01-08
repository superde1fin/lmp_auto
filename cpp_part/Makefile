.DEFAULT_GOAL := all

TARGET = shrt_lib
CFLAGS = --std=c++11 -Wall

all: $(TARGET)

$(TARGET): shortener.cpp $(TARGET).cpp
	g++ $^ -o $@

