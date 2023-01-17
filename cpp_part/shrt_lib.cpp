#include <boost/python.hpp>
#include "shortener.cpp"

using namespace boost::python;

BOOST_PYTHON_MODULE(shrt_lib){
    class_<Shortener, boost::noncopyable>("Shortener", init<std::string>())
    .def("shorten_file", static_cast<int(Shortener::*)(int, int, int, int)>(&Shortener::shorten_file))
    .def("shorten_file", static_cast<int(Shortener::*)(int, int, int, std::string)>(&Shortener::shorten_file))
    ;
    }
