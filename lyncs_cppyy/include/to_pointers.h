template <typename T, typename T0, class ... Ts>
class add_pointers : public add_pointers<T*, Ts...>{
};

template <typename T, typename T0>
class add_pointers<T, T0>{
public:
    typedef T* type;
};


template<typename T>
size_t _pointers_size(T l0) {
  return 1;
}

template<typename T, class ... Ts>
size_t _pointers_size(T l0, Ts ... ls) {
  return (l0+1)*_pointers_size(ls...);
}

template<typename T, class ... Ts>
size_t pointers_size(T l0, Ts ... ls) {
  return l0*_pointers_size(ls...);
}

template<typename T,  class Tn>
void fill_in(T* arr, T** buf, size_t coord, Tn lm1, Tn ln) {
  for(Tn i=0; i<lm1; i++) {
    buf[i] = arr + (coord*lm1 + i)*ln;
  }
}


template<typename T, class T0, class ... Ts>
void fill_in(T* arr, typename add_pointers<T*,Ts...>::type buf, size_t coord, T0 l0, Ts ... shape) {
  for(T0 i=0; i<l0; i++) {
    size_t skip;
    buf[i] = buf+skip;
    fill_in(buf[i], arr, coord*l0+i, shape...);
  }
}


template<typename T, class T0>
auto to_pointers(T* arr, T0 l0) {
  return arr;
}

template<typename T, class ... Ts>
auto to_pointers(T* arr, Ts ... shape) {
  auto buffer = static_cast<typename add_pointers<T, Ts...>::type>(std::malloc(pointers_size(shape...)*sizeof(void*)));
  //auto buffer = std::make_unique<typename add_pointers<T, Ts...>::type []>(pointers_size(shape...));
  fill_in(arr, buffer, 0, shape...);
  return buffer;
}
