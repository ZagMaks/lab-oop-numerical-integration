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
        """Знаходить інтеграл із заданою точністю eps за правилом Рунге."""
        pass

    def __str__(self):
        """Повертає рядкове представлення об'єкта інтегратора."""
        pass


class RectangleIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою середніх прямокутників."""

    order = 2
    method_name = "Формула прямокутників"

    def __init__(self, func, a, b):
        super().__init__(func,a,b)

    def integrate(self, n):
        h = (self.b - self.a) / n
        total = sum(self.func(self.a + (i + 0.5) * h) for i in range(n))
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
