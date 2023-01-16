.DEFAULT_GOAL := all

# location of the Python header files
PYTHON_VERSION = 3.10
#PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)
PYTHON_INC= /usr/include
PYTHON_LIB = /usr/lib
PY_USE_DEF="true"
ifeq ($(PY_USE_DEF), "ture")
PYTHON_LIB_INSIDE_PATH=/python$(PYTHON_VERSION)/config
else
PYTHON_LIB_INSIDE_PATH=
endif

# location of the Boost Python include files and library
BOOST_INC = /usr/local/include
BOOST_LIB = /usr/local/lib

TARGET = shrt_lib

CFLAGS = --std=c++11

$(TARGET).so: $(TARGET).o
	g++ -shared -Wl,--export-dynamic -Wl,--no-undefined $(TARGET).o -L$(BOOST_LIB) -l:libboost_python$(subst m,,$(subst .,,$(PYTHON_VERSION))).so -L$(PYTHON_LIB)$(PYTHON_LIB_INSIDE_PATH) -lpython$(PYTHON_VERSION) -o $(TARGET).so $(CFLAGS) -lgmp -lssl -lcrypto

$(TARGET).o: $(TARGET).cpp shortener.hpp shortener.cpp Makefile
	g++ -I$(PYTHON_INC)/python$(PYTHON_VERSION) -I$(BOOST_INC) -fPIC -c $(TARGET).cpp $(CFLAGS)

all: $(TARGET).so
