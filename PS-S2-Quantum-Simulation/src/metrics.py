
import math

def absolute_error(observed, exact):
    return abs(float(observed) - float(exact))

def normalized_error(observed, exact):
    return absolute_error(observed, exact) / max(abs(float(exact)), 1e-12)

def safe_float(value):
    try:
        result = float(value)
        return result if math.isfinite(result) else float("nan")
    except (TypeError, ValueError):
        return float("nan")
