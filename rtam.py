import random
import math
import re
import numpy as np
from rtamt import StlDiscreteTimeSpecification, RTAMTException
import spot


def normalize_ltl(formula: str) -> str:
    f = formula

    replacements = {
        r'\bglobally\b': 'G',
        r'\bfinally\b': 'F',
        r'\buntil\b': 'U',
        r'\bimply\b': '->',
        r'\bequal\b': '<->',
        r'\band\b': '&',
        r'\bor\b': '|',
    }

    for pat, rep in replacements.items():
        f = re.sub(pat, rep, f)

    # Clean spacing
    f = " ".join(f.split())
    return f


def ltl_equivalent(f1: str, f2: str) -> bool:
    try:
        a1 = spot.translate(f1, 'det')
        a2 = spot.translate(f2, 'det')
        return spot.are_equivalent(a1, a2)
    except Exception as e:
        print("LTL parse error:", e)
        return False



