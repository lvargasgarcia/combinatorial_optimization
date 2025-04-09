#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "efficient_operators.hpp"

namespace py = pybind11;

PYBIND11_MODULE(drils, m) {
    m.doc() = "Python bindings for the DRILS function";

    m.def("DRILS", &DRILS, 
          py::arg("file"), 
          py::arg("neighborhood_size"), 
          py::arg("time_interval_drils"),
          py::arg("steepest_descent"),
          "Run the DRILS algorithm and return the best permutation and its value");
}