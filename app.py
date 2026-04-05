from flask import Flask, render_template, request, jsonify
import sympy as sp
import numpy as np
import plotly.graph_objects as go
import plotly.utils
import json

app = Flask(__name__)

def parse_function(func_str):
    """
    Parses a string like 'y = x^2' or 'x^2' into a SymPy expression.
    Handles 'y=' prefix and common replacements.
    """
    func_str = func_str.lower().strip()
    if '=' in func_str:
        # Get everything after the '=' sign
        func_str = func_str.split('=')[-1].strip()
    
    # Replace '^' with '**' for SymPy parsing if needed (SymPy handles x^2 but good to be safe)
    func_str = func_str.replace('^', '**')
    
    try:
        # Use sympify to convert string to SymPy expression
        x = sp.Symbol('x')
        expr = sp.sympify(func_str)
        return expr, x
    except Exception as e:
        return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    data = request.json
    f1_str = data.get('f1', '')
    f2_str = data.get('f2', '')

    expr1, x = parse_function(f1_str)
    expr2, _ = parse_function(f2_str)

    if expr1 is None or expr2 is None:
        return jsonify({'error': 'Invalid function format. Try something like y = x^2 or 2*x + 1'})

    # 1. Find Intersection Points
    # Solve expr1 = expr2  => expr1 - expr2 = 0
    intersections = []
    try:
        # Optimization: Use sp.solve with manual check for real roots
        # This is generally faster for simple polynomials
        roots = sp.solve(expr1 - expr2, x, dict=False)
        for r in roots:
            # Check if r is specifically a real number
            if r.is_real:
                y_val = expr1.subs(x, r)
                intersections.append({
                    'x': float(r),
                    'y': float(y_val)
                })
        
        # Numerical fallback if no points found symbolically but there might be some
        if not intersections:
            # Try a quick numerical search if functions are not polynomials
            from sympy import nsolve
            # Sample a few starting points
            for start in [-5, 0, 5]:
                try:
                    sol = nsolve(expr1 - expr2, x, start)
                    intersections.append({'x': float(sol), 'y': float(expr1.subs(x, sol))})
                except:
                    continue
            # Remove duplicates from numerical points
            intersections = [dict(t) for t in {tuple(d.items()) for d in intersections}]
    except Exception as e:
        print(f"Solving error: {e}")

    # 2. Generate Plot Data
    # Determine plot range based on intersections or default to [-10, 10]
    if intersections:
        min_x = min(p['x'] for p in intersections) - 5
        max_x = max(p['x'] for p in intersections) + 5
    else:
        min_x, max_x = -10, 10

    x_values = np.linspace(min_x, max_x, 400)
    
    # Lambda-ize expressions for fast numerical evaluation
    f1_lambda = sp.lambdify(x, expr1, 'numpy')
    f2_lambda = sp.lambdify(x, expr2, 'numpy')

    y1_values = f1_lambda(x_values)
    y2_values = f2_lambda(x_values)

    # Create Plotly figure
    fig = go.Figure()

    # Trace for Function 1
    fig.add_trace(go.Scatter(
        x=x_values, y=y1_values,
        mode='lines',
        name=f"y = {sp.printing.latex(expr1)}",
        line=dict(color='#636EFA', width=3)
    ))

    # Trace for Function 2
    fig.add_trace(go.Scatter(
        x=x_values, y=y2_values,
        mode='lines',
        name=f"y = {sp.printing.latex(expr2)}",
        line=dict(color='#EF553B', width=3)
    ))

    # Trace for Intersection Points
    if intersections:
        fig.add_trace(go.Scatter(
            x=[p['x'] for p in intersections],
            y=[p['y'] for p in intersections],
            mode='markers',
            name='Intersections',
            marker=dict(color='#00CC96', size=12, symbol='circle', 
                        line=dict(width=2, color='white')),
            text=[f"({p['x']:.2f}, {p['y']:.2f})" for p in intersections],
            hoverinfo='text'
        ))

    # Shading between curves (Optional but requested)
    fig.add_trace(go.Scatter(
        x=np.concatenate([x_values, x_values[::-1]]),
        y=np.concatenate([y1_values, y2_values[::-1]]),
        fill='toself',
        fillcolor='rgba(100, 100, 100, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False,
        name='Area between curves'
    ))

    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=dict(text='Function Intersection Plot', font=dict(size=24)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor='#333', zerolinecolor='#666'),
        yaxis=dict(gridcolor='#333', zerolinecolor='#666'),
        margin=dict(l=20, r=20, t=60, b=20)
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return jsonify({
        'graph': graphJSON,
        'intersections': intersections
    })

if __name__ == '__main__':
    app.run(debug=True)
