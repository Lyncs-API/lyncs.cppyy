#include "to_pointers.h"

template <typename T> class base_type{
public:
    typedef T type;
};

template <typename T> class base_type<T*>{
public:
    typedef typename base_type<T>::type type;
};

template<typename T>
auto product(T l0) {
  return l0;
}

template<typename T, class ... Ts>
auto product(T l0, Ts ... ls) {
  return l0*product(ls...);
}

template<typename T1, typename T2>
auto flatten(std::vector<T1> &vec, T1* arr, T2 l0) {
  for(int i=0; i<l0; i++) {
    vec.push_back(arr[i]);
  }
  return vec;
}

template<typename T, typename T0, class ... Ts>
auto flatten(std::vector<T1> &vec, typename add_pointers<T, Ts...>::type arr, T0 l0, Ts ... ls) {
  for(T3 i=0; i<l0; i++) {
    flatten(vec, arr[i], ls...);
  }
  return vec;
}

template<typename T, class ... Ts>
auto flatten(typename add_pointers<T, Ts...>::type arr, Ts ... shape) {
  std::vector<T> v;
  v.reserve(product(shape...));
  return flatten(v, arr, shape ...);
}
