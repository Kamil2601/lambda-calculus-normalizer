from language import *
from parser import *
# from converter import *

def eval_krivine(term: Term):
    stack = []
    env = []
    while True:
        if term.is_app():
            stack.append((term.t2, env))
            term = term.t1

        elif term.is_lambda():
            if len(stack) == 0:
                return term, env

            stack_top = stack.pop()
            env = [stack_top] + env
            term = term.t

        elif term.is_var():
            index = term.var
            if index >= len(env):
                if len(stack) == 0:
                    return term, env
                else:
                    raise Exception("Not implemented")
            else:
                index = term.var
                term, env = env[index]


def shift(t, d, c = 0):
    if t.is_var():
        if t.var < c:
            return t
        else:
            return Var(t.var + d)

    elif t.is_lambda():
        return Lambda(t.var, shift(t.t, d, c+1))

    elif t.is_app():
        return App(shift(t.t1, d, c), shift(t.t2, d, c))



# [n -> s]t
def substitution(t,n,s):
    if t.is_var():
        if t.var == n:
            return s
        else:
            return t
    elif t.is_app():
        return App(substitution(t.t1, n, s), substitution(t.t2, n, s))
    elif t.is_lambda():
        return Lambda(t.var, substitution(t.t, n + 1, shift(s, 1, 0)))



def normalize_subst_cbn(t):
    if t.is_app():
        t1_norm = normalize_subst_cbn(t.t1)
        if t1_norm.is_lambda():
            beta_reduced = substitution(t1_norm.t, 0, shift(t.t2, 1))
            beta_reduced = shift(beta_reduced, -1)
            return normalize_subst_cbn(beta_reduced)
            # return shift(normalize_subst_cbn(beta_reduced), -1, 0)
        return App(t1_norm, t.t2)

    return t


def normalize_subst_no(t):
    t_normalized_cbn = normalize_subst_cbn(t)

    if t_normalized_cbn.is_lambda():
        return Lambda(t_normalized_cbn.var, normalize_subst_no(t_normalized_cbn.t))
    elif t_normalized_cbn.is_app():
        return App(
            normalize_subst_no(t_normalized_cbn.t1),
            normalize_subst_no(t_normalized_cbn.t2),
        )

    return t_normalized_cbn


def alpha_equal(t1, t2):
    if t1.is_var() and t2.is_var():
        return t1.var == t2.var
    elif t1.is_lambda() and t2.is_lambda():
        return alpha_equal(t1.t, t2.t)
    elif t1.is_app() and t2.is_app():
        lefts_equal = alpha_equal(t1.t1, t2.t1)
        if lefts_equal:
            return alpha_equal(t1.t2, t2.t2)

    return False

def beta_equal(clo1, clo2):
    t1, free1 = clo1
    t2, free2 = clo2
    normalized_t1 = normalize_subst_no(t1)
    normalized_t2 = normalize_subst_no(t2)

    normalized_t1_free_vars = restore_free_vars(normalized_t1, free1)
    normalized_t2_free_vars = restore_free_vars(normalized_t2, free2)

    return alpha_equal(normalized_t1_free_vars, normalized_t2_free_vars)
