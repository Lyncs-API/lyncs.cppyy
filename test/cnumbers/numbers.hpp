namespace numbers {

  long gbl;
  
  template<typename T>
  T zero() {
    return (T) 0;
  }
  
  template<typename T>
  T one() {
    return (T) 1;
  }

  template<typename T>
  T global() {
    return (T) gbl;
  }  

  namespace another {
    template<typename T>
    T two() {
      return (T) 2;
    }
  }
}
