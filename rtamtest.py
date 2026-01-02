import numpy as np
from rtamt import StlDiscreteTimeSpecification

spec = StlDiscreteTimeSpecification()
spec.declare_var('prop_1', 'float')
spec.spec = 'G prop_1'
spec.parse()

t = np.array([0,1,2])
v = np.array([1.0, -1.0, 0.5])

formats = {
    "numpy per-signal dict": {
        'prop_1': {'time': t, 'value': v}
    },

    "flat dict (time + separate value)": {
        'time': t,
        'prop_1': v
    },

    "flat dict all numpy arrays": {
        'prop_1': v,
        'prop_2': v  # extra noise
    }
}

for name, tr in formats.items():
    print(f"\n=== Testing {name} ===")
    try:
        r = spec.evaluate(tr)
        print("OK:", r)
    except Exception as e:
        print("ERROR:", e)
