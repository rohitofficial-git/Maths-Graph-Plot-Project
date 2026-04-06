import numpy as np

def evaluate_function(expr, x_values, use_degrees=False):
    """
    Evaluates a math expression given as a string for a range of x values.
    Uses numpy for performance and ease of explanation.
    """
    # Replace common math symbols to match Python's syntax
    expr = expr.replace('^', '**')
    
    # Wrap trig functions if we are in degrees mode
    def dsin(x): return np.sin(np.radians(x))
    def dcos(x): return np.cos(np.radians(x))
    def dtan(x): return np.tan(np.radians(x))

    # Use a controlled namespace for evaluation
    allowed_names = {
        'x': x_values,
        'sin': dsin if use_degrees else np.sin,
        'cos': dcos if use_degrees else np.cos,
        'tan': dtan if use_degrees else np.tan,
        'exp': np.exp,
        'log': np.log,
        'sqrt': np.sqrt,
        'pi': np.pi,
        'e': np.e,
        'abs': np.abs
    }
    result = eval(expr, {"__builtins__": {}}, allowed_names)
    # Ensure constants (like sin(54)) match the input shape (array or scalar)
    if hasattr(x_values, 'shape'):
        return np.broadcast_to(result, x_values.shape)
    return result

def find_intersection(f1_expr, f2_expr, x_range=(-12, 12), steps=200, use_degrees=False):
    """
    Finds intersection points between two functions using a numerical search.
    This is the core 'calculative' logic requested.
    """
    x_scan = np.linspace(x_range[0], x_range[1], steps)
    
    # We define a difference function: f1(x) - f2(x) = 0
    def diff(x):
        return evaluate_function(f1_expr, x, use_degrees) - evaluate_function(f2_expr, x, use_degrees)
    
    y_diff = diff(x_scan)
    intersections = []
    
    # Scan for sign changes (Bolzano's Theorem)
    for i in range(len(x_scan) - 1):
        if y_diff[i] * y_diff[i+1] < 0:
            # Bisection method for refined root finding
            a, b = x_scan[i], x_scan[i+1]
            for _ in range(20):
                mid = (a + b) / 2
                if diff(a) * diff(mid) < 0:
                    b = mid
                else:
                    a = mid
            
            root_x = float(mid)
            root_y = float(evaluate_function(f1_expr, root_x, use_degrees))
            
            # Add if not a duplicate
            if not any(abs(p['x'] - root_x) < 0.1 for p in intersections):
                intersections.append({'x': root_x, 'y': root_y})
                
    return intersections

def get_plot_data(f1_expr, f2_expr, x_range=(-12, 12), use_degrees=False):
    """
    Generates all data needed for the front-end to plot.
    """
    x_values = np.linspace(x_range[0], x_range[1], 400)
    
    y1_values = evaluate_function(f1_expr, x_values, use_degrees)
    y2_values = evaluate_function(f2_expr, x_values, use_degrees)
    
    intersections = find_intersection(f1_expr, f2_expr, x_range, use_degrees=use_degrees)
    
    return {
        "x": x_values.tolist(),
        "y1": y1_values.tolist(),
        "y2": y2_values.tolist(),
        "intersections": intersections
    }
