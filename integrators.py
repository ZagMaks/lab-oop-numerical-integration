"""Модуль реалізації класів чисельного інтегрування."""


class BaseIntegrator:
    """Базовий клас для чисельного обчислення визначених інтегралів."""

    order = 1
    method_name = "Базовий метод"

    def __init__(self, func, a, b):
        self.func = func
        self.a = float(a)
        self.b = float(b)

    @classmethod
    def from_dict(cls, func, params):
        return cls(func,params["a"],params["b"])

    @staticmethod
    def validate_bounds(a, b):
        return b>=a
    
    def integrate(self, n):
        """Обчислює наближене значення інтеграла для n розбиттів."""
        raise NotImplementedError

    def adaptive_integrate(self, eps=1e-4, initial_n=2):
        n = initial_n
        koef = 2**self.order-1
        I_h = self.integrate(n)
        I_h2 = self.integrate(2*n)
        delta = abs(I_h-I_h2)/koef
        print(f"n = {n} -> I = {I_h}")
        counter = 1
        while delta>=eps:
            n*=2
            I_h = I_h2
            I_h2 = self.integrate(2*n)
            delta = abs(I_h2-I_h)/koef
            print(f"n = {n} -> I = {I_h}")
            counter += 1
        print(f"n = {2*n} -> I = {I_h2}")
        value = I_h2 + (I_h2 - I_h)/koef
        counter += 1
        return value,2*n,delta,counter
    
    def amount_of_iterations(self, eps=1e-4, initial_n=2):
        counter = self.adaptive_integrate(eps=1e-4,initial_n=2)[3]
        return counter
    def __str__(self):
        return (f"{self.method_name} (порядок точності O(h^{self.order})) на відрізку [{self.a}; {self.b}]")


class RectangleIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою середніх прямокутників."""

    order = 2
    method_name = "Формула прямокутників"

    def __init__(self, func, a, b):
        super().__init__(func,a,b)

    def integrate(self, n):
        h = (self.b - self.a) / n
        total = sum(self.func(self.a + (i + 0.5) * h) for i in range (n))
        return total*h


class TrapezoidIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою трапецій."""

    order = 2
    method_name = "Формула трапецій"

    def __init__(self, func, a, b):
        super().__init__(func,a,b)

    def integrate(self, n):
        h = (self.b - self.a)/n
        Sum = sum(self.func(self.a + i*h) for i in range(1,n))
        return h*(((self.func(self.a)+self.func(self.b))/2) + Sum)


class SimpsonIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою Сімпсона."""

    order = 4
    method_name = "Формула Сімпсона"

    def __init__(self, func, a, b):
        super().__init__(func,a,b)

    def integrate(self, n):
        h = (self.b - self.a)/n
        Sum1 = sum(self.func(self.a + i*h)for i in range(1,n,2))
        Sum2 = sum(self.func(self.a + i*h)for i in range(2,n-1,2))
        return (h/3)*(self.func(self.a)+self.func(self.b)+4*Sum1+2*Sum2)
