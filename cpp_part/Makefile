.DEFAULT_GOAL := all

# location of the Python header files
PYTHON_VERSION = 3.10
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)

# location of the Boost Python include files and library
BOOST_INC = /usr/include
BOOST_LIB = /usr/local/lib/boost_1_79_0

TARGET = shrt_lib

CFLAGS = --std=c++11

$(TARGET).so: $(TARGET).o
	g++ -shared -Wl,--export-dynamic -Wl,--no-undefined $(TARGET).o -L$(BOOST_LIB) -l:libboost_python$(subst .,,$(PYTHON_VERSION)).so -L/usr/lib/python$(PYTHON_VERSION)/config -lpython$(PYTHON_VERSION) -o $(TARGET).so $(CFLAGS) -lgmp -lssl -lcrypto

$(TARGET).o: $(TARGET).cpp shortener.hpp shortener.cpp Makefile
	g++ -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC -c $(TARGET).cpp $(CFLAGS)
	objcopy --redefine-sym _ZN5boost6python15instance_holder8allocateEP7_objectmmm=_ZN5boost6python15instance_holder8allocateEP7_objectmm $(TARGET).o

all: $(TARGET).so
