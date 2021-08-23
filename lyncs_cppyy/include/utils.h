// A set of useful functions that are included by lyncs_cppyy
// and made available at Python level

// Turns a class pointer to shared_ptr
template<typename T>
std::shared_ptr<T> lyncs_cppyy_make_shared(T* ptr) {
  return std::shared_ptr<T>(ptr);
}
