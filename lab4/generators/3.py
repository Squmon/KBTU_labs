def function_with_a_genrator(N:int):
  return (i for i in range(N) if i%3 == 0 and i%4 == 0)