from pytools import shift

def ctt(z:complex): # complex to tuple
    return (z.real, z.imag)

def dot(a, b):
    return a.real*b.real + a.imag*b.imag

def normalize(z):
    return z/abs(z) if abs(z) > 0 else 0j

def transform_f(figure, transform, position = 0j, fnc = lambda x:x):
    return [fnc(transform*f + position) for f in figure]

def inside(figure:list[complex], point:complex):
    center = sum(figure)/len(figure)
    return all(map(lambda c: dot(d := 1j*normalize(c[0] - c[1]), point - center) < dot(d, c[0] - center), zip(figure, shift(figure, -1))))

def stretch(z:complex, coofs:complex):
    return complex(z.real * coofs.real, z.imag * coofs.imag)

def get_box(figure:list[complex]):
    return min(v.real for v in figure) + min(v.imag for v in figure)*1j, max(v.real for v in figure) + max(v.imag for v in figure)*1j

class shapes:
    triangle_v = tuple(1j**(1/2)*normalize(1j**(i+1) + 0.5) for i in range(0, 3))
    square = tuple(1j**0.5*normalize(1j**i) for i in range(0, 4))
    star = tuple((0.5 + 0.5*(i%2))*1j**0.5*normalize(1j**(4*i/10)) for i in range(0, 10))

    
    __circle_hash = dict()
    @classmethod
    def circle(self, N):
        if not (N in shapes.__circle_hash):
            self.__circle_hash[N] = tuple(normalize(1j**(4*i/N)) for i in range(0, N))
        return self.__circle_hash[N]