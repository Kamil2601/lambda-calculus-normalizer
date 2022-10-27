import re
from language import *

def is_var(token):
    return re.match("^[a-z]+$", token)


def is_nat(token):
    return re.match("^\d+$", token)


def is_lambda(token):
    return re.match("^lambda [a-z]+[.]$", token)


def is_term(token):
    return isinstance(token, Term)


def lambda_var(token):
    return token[7:-1]

def tail(xs):
    if len(xs) == 0:
        return []
    return xs[1:]

def parse_brackets(tokens):
    stack = []
    for token in tokens:
        if token == ")":
            error = True
            for i in range(len(stack) - 1, -1, -1):
                if stack[i] == "(":
                    error = False
                    stack = stack[:i] + [stack[i + 1 :]]
                    break
            if error:
                raise Exception("Parse error")
        else:
            stack.append(token)

    if "(" in stack:
        raise Exception("Parse error")

    def remove_brackets(xs):
        while len(xs) == 1 and not isinstance(xs, str):
            xs = xs[0]

        if isinstance(xs, str):
            return xs
        return [remove_brackets(x) for x in xs]

    return remove_brackets(stack)


def parse_term(term_str: str):
    term_str = " ".join(term_str.split())
    
    

    regex = "lambda [a-z]+[.]|[a-z]+|\d+|[(]|[)]"

    tokens = re.findall(regex, term_str)

    tokens = parse_brackets(tokens)

    term, list_tail = parse([tokens])

    return term

def terms_strings(text):
    res = []
    for term_str in text.split(";"):
        t_str = " ".join(term_str.split())
        
        if len(t_str) > 0:
            res.append(t_str)

    return res


def parse(tokens):
    try:
        hd = tokens[0]
    except:
        raise Exception("Parse error")
    if isinstance(hd, list):
        term, l = parse(hd)

        while l != []:
            t, l = parse(l)
            term = App(term, t)

        return term, tail(tokens)

    if is_lambda(hd):
        var = lambda_var(hd)
        term, l = parse(tail(tokens))

        while l != []:
            t, l = parse(l)
            term = App(term, t)

        return Lambda(var, term), l

    elif hd in ['add', 'mul', 'sub', 'eq', 'cons', 'pair']:
        t1, l1 = parse(tail(tokens))
        t2, l2 = parse(l1)

        if hd == 'add':
            return Add(t1, t2), l2
        elif hd == 'mul':
            return Mul(t1,t2), l2
        elif hd == 'sub':
            return Sub(t1,t2), l2
        elif hd == 'eq':
            return Eq(t1,t2), l2
        elif hd == 'cons':
            return Cons(t1,t2), l2
        elif hd == 'pair':
            return Pair(t1,t2), l2
    
    elif hd == "if":
        t1, l1 = parse(tail(tokens))
        t2, l2 = parse(l1)
        t3, l3 = parse(l2)

        return If(t1,t2,t3), l3

    elif hd == "true":
        return Tru(), tail(tokens)
    elif hd == "false":
        return Fls(), tail(tokens)
    elif hd == "nil":
        return Nil(), tail(tokens)

    elif hd in ["fst", "snd", "head", "tail", "isnil", "fix"]:
        t, l = parse(tail(tokens))

        if hd == "fst":
            return Fst(t), l
        elif hd == "snd":
            return Snd(t), l
        elif hd == "head":
            return Head(t), l
        elif hd == "tail":
            return Tail(t), l
        elif hd == "isnil":
            return IsNil(t), l
        elif hd == "fix":
            return Fix(t), l

    elif is_var(hd):
        return Var(hd), tail(tokens)
    elif is_nat(hd):
        return Nat(hd), tail(tokens)


def nat_to_lambda(n):
    app = Var("z")

    for _ in range(n):
        app = App(Var("s"), app)

    return Lambda("s", (Lambda("z", app)))

def desugar(term: Term):
    if isinstance(term, Var):
        return term
    elif isinstance(term, Lambda):
        return Lambda(term.var, desugar(term.t))
    elif isinstance(term, App):
        return App(desugar(term.t1), desugar(term.t2))
    elif isinstance(term, Nat):
        return nat_to_lambda(term.n)
    elif isinstance(term, Add):
        add = parse_term("lambda m. lambda n. lambda s. lambda z. m s (n s z)")
        return App(App(add, desugar(term.n)), desugar(term.m))
    elif isinstance(term, Mul):
        plus = "(lambda m. lambda n. lambda s. lambda z. m s (n s z))"
        times = parse_term(f"lambda m. lambda n. m ({plus} n) (lambda s. lambda n. n)")
        return App(App (times, desugar(term.n)), desugar(term.m))
    elif isinstance(term, Sub):
        zz = Pair(Nat(0), Nat(0))
        ss = Lambda("p", Pair(Snd(Var("p")), Add(Nat(1), Snd(Var("p")))))
        prd = Lambda("m", Fst(App(App(Var("m"), ss), zz)))
        return desugar(Lambda("m", Lambda("n", App(App(Var("n"), prd), Var("m")))))
    elif isinstance(term, Eq):
        isZero = parse_term("lambda n. n (lambda x. false) true")
        leq = Lambda("m", Lambda("n", App(isZero, Sub(Var("m"), Var("n")))))
        lambda_and = parse_term("lambda p. lambda q. p q p")
        m_leq_n = App(App(leq, Var("m")), Var("n"))
        n_leq_m = App(App(leq, Var("n")), Var("m"))
        return Lambda("m", Lambda("n", App(App(lambda_and, m_leq_n), n_leq_m)))
    elif isinstance(term, Tru):
        return Lambda("t", (Lambda("f", Var("t"))))
    elif isinstance(term, Fls):
        return Lambda("t", (Lambda("f", Var("f"))))
    elif isinstance(term, If):
        return App(App(desugar(term.cond), desugar(term.if_true)), desugar(term.if_false))
    elif isinstance(term, Fix):
        fix = parse_term("lambda f. (lambda x. f (lambda y. x x y)) (lambda x. f (lambda y. x x y))")
        return App(fix, desugar(term.f))
    elif isinstance(term, Pair):
        pair =  parse_term("lambda f. lambda s. lambda b. b f s")
        return App(App(pair, desugar(term.first)), desugar(term.second))
    elif isinstance(term, Fst):
        fst = Lambda("p", App(Var("p"), Lambda("t", (Lambda("f", Var("t"))))))
        return App(fst, desugar(term.pair))
    elif isinstance(term, Snd):
        snd = Lambda("p", App(Var("p"), Lambda("t", (Lambda("f", Var("f"))))))
        return App(snd, desugar(term.pair))
    elif isinstance(term, Nil):
        return parse_term("lambda c. lambda n. n")
    elif isinstance(term, Cons):
        cons = parse_term("lambda h. lambda t. lambda c. lambda n. c h (t c n)")
        return App(App(cons, desugar(term.head)), desugar(term.tail))
    elif isinstance(term, Head):
        head = parse_term("lambda l. l (lambda h. lambda t. h) (lambda t. lambda f. f)")
        return desugar(App(head, term.list))
    elif isinstance(term, Tail):
        tru = "(lambda t. lambda f. t)"
        fls = "(lambda t. lambda f. f)"

        pair = "(lambda f. lambda s. lambda b. b f s)"
        fst = f"(lambda p. p {tru})"
        snd = f"(lambda p. p {fls})"

        tail = parse_term(f"lambda l. {fst} (l (lambda x. lambda p. pair ({snd} p) (cons x ({snd} p))) ({pair} nil nil))")

        return desugar(App(tail, term.list))

    elif isinstance(term, IsNil):
        tru = "(lambda t. lambda f. t)"
        fls = "(lambda t. lambda f. f)"

        isnil = parse_term(f"lambda l. l (lambda h. lambda t. {fls}) {tru}")
        return App(isnil, desugar(term.list))


def normal_to_deBruijn(term: Term):
    free_vars = {}

    def convert(t: Term, bound_vars):
        if t.is_var():
            try:
                return Var(bound_vars.index(t.var))
            except:
                if t.var not in free_vars:
                    free_var_index = len(free_vars)
                    free_vars[t.var] = free_var_index
                return Var(free_vars[t.var] + len(bound_vars))
        elif t.is_app():
            return App(convert(t.t1, bound_vars), convert(t.t2, bound_vars))
        elif t.is_lambda():
            return Lambda("", convert(t.t, [t.var] + bound_vars))

    return convert(term, []), list(free_vars.keys())


def deBruijn_to_normal(term, free_vars):
    def convert(t: Term, bound_vars):
        if t.is_var():
            if len(bound_vars) > t.var:
                return Var(bound_vars[t.var])
            else:
                return Var(free_vars[t.var - len(bound_vars)])
        elif t.is_app():
            return App(convert(t.t1, bound_vars), convert(t.t2, bound_vars))
        elif t.is_lambda():
            t.var = f"x{len(bound_vars)}"
            return Lambda(t.var, convert(t.t, [t.var] + bound_vars))

    return convert(term, [])

def restore_free_vars(term, free_vars):
    def convert(t: Term, bound_vars):
        if t.is_var():
            if len(bound_vars) > t.var:
                return t
            else:
                return Var(free_vars[t.var - len(bound_vars)])
        elif t.is_app():
            return App(convert(t.t1, bound_vars), convert(t.t2, bound_vars))
        elif t.is_lambda():
            return Lambda(t.var, convert(t.t, [t.var] + bound_vars))

    return convert(term, [])


def parse_term_to_deBruijn(term_str: str):
    term = parse_term(term_str)
    desugared_term = desugar(term)
    return normal_to_deBruijn(desugared_term)
