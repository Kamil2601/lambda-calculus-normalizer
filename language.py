class Term:
    def __str__(self):
        pass

    def debug_str(self):
        pass

    def is_var(self):
        return False

    def is_lambda(self):
        return False

    def is_app(self):
        return False

class Var(Term):
    def __init__(self, var):
        self.info = None
        self.var = var

    def __str__(self):
        return str(self.var)

    def is_var(self):
        return True

    def debug_str(self):
        return f"Var {self.var}"


class Lambda(Term):
    def __init__(self, var: str, t: Term):
        self.info = None
        self.var = var
        self.t = t

    def __str__(self):
        return f"λ{self.var}. {self.t}"

    def debug_str(self):
        return f"Lambda {self.var}. ({self.t.debug_str()})"

    def is_lambda(self):
        return True


class App(Term):
    def __init__(self, t1: Term, t2: Term):
        self.info = None
        self.t1 = t1
        self.t2 = t2

    def __str__(self):
        res = ""
        if self.t1.is_var():
            res += f"{self.t1}"
        else:
            res += f"({self.t1})"

        if self.t2.is_var():
            res += f" {self.t2}"
        else:
            res += f" ({self.t2})"

        return res

    def debug_str(self):
        return f"App ({self.t1.debug_str()}), ({self.t2.debug_str()})"

    def is_app(self):
        return True

class Nat(Term):
    def __init__(self, n):
        self.n = int(n)

    def __str__(self):
        return str(self.n)

class Add(Term):
    def __init__(self, n, m):
        self.n = n
        self.m = m

    def __str__(self):
        return f"add ({str(self.n)}) ({str(self.m)})"

class Mul(Term):
    def __init__(self, n, m):
        self.n = n
        self.m = m

    def __str__(self):
        return f"mul ({str(self.n)}) ({str(self.m)})"

class Sub(Term):
    def __init__(self, n, m):
        self.n = n
        self.m = m

    def __str__(self):
        return f"sub ({str(self.n)}) ({str(self.m)})"

class Eq(Term):
    def __init__(self, n, m):
        self.n = n
        self.m = m

    def __str__(self):
        return f"eq ({str(self.n)}) ({str(self.m)})"

class Tru(Term):
    def __str__(self):
        return "true"

class Fls(Term):
    def __str__(self):
        return "false"

class If(Term):
    def __init__(self, cond, if_true, if_false):
        self.cond = cond
        self.if_true = if_true
        self.if_false = if_false

    def __str__(self):
        return f"if ({str(self.cond)}) then ({str(self.if_true)}) else ({str(self.if_false)})"
    

class Fix(Term):
    def __init__(self, f):
        self.f = f

    def __str__(self):
        return f"fix ({self.f})"

class Pair(Term):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return f"pair ({self.first}) ({self.second})"

class Fst(Term):
    def __init__(self, pair):
        self.pair = pair

    def __str__(self):
        return f"fst ({self.pair})"

class Snd(Term):
    def __init__(self, pair):
        self.pair = pair

    def __str__(self):
        return f"snd ({self.pair})"

class Nil(Term):
    def __str__(self):
        return f"nil"

class Cons(Term):
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def __str__(self):
        return f"cons ({self.head}) ({self.tail})"

class Head(Term):
    def __init__(self, t):
        self.list = t

    def __str__(self):
        return f"head ({self.list})"

class Tail(Term):
    def __init__(self, t):
        self.list = t

    def __str__(self):
        return f"tail ({self.list})"

class IsNil(Term):
    def __init__(self, t):
        self.list = t

    def __str__(self):
        return f"isnil ({self.list})"

