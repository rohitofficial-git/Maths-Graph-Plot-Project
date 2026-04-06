import numpy as np

def evaluate_function(expr, x_values):
    """
    Evaluates a math expression given as a string for a range of x values.
    Uses numpy for performance and ease of explanation.
    """
    # Replace common math symbols to match Python's syntax
    expr = expr.replace('^', '**')
    # Use a controlled namespace for evaluation
    allowed_names = {
        'x': x_values,
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'exp': np.exp,
        'log': np.log,
        'sqrt': np.sqrt,
        'pi': np.pi,
        'e': np.e,
        'abs': np.abs
    }
    return eval(expr, {"__builtins__": {}}, allowed_names)

def find_intersection(f1_expr, f2_expr, x_range=(-12, 12), steps=200):
    """
    Finds intersection points between two functions using a numerical search.
    This is the core 'calculative' logic requested.
    """
    x_scan = np.linspace(x_range[0], x_range[1], steps)
    
    # We define a difference function: f1(x) - f2(x) = 0
    def diff(x):
        return evaluate_function(f1_expr, x) - evaluate_function(f2_expr, x)
    
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
            root_y = float(evaluate_function(f1_expr, root_x))
            
            # Add if not a duplicate
            if not any(abs(p['x'] - root_x) < 0.1 for p in intersections):
                intersections.append({'x': root_x, 'y': root_y})
                
    return intersections

def get_plot_data(f1_expr, f2_expr, x_range=(-12, 12)):
    """
    Generates all data needed for the front-end to plot.
    """
    x_values = np.linspace(x_range[0], x_range[1], 400)
    
    y1_values = evaluate_function(f1_expr, x_values)
    y2_values = evaluate_function(f2_expr, x_values)
    
    intersections = find_intersection(f1_expr, f2_expr, x_range)
    
    return {
        "x": x_values.tolist(),
        "y1": y1_values.tolist(),
        "y2": y2_values.tolist(),
        "intersections": intersections
    }
