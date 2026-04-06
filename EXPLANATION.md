# Explaining the Mathematical Logic (Python)

This project handles all calculations in Python for better readability and performance. Here's a breakdown of the core logic:

## 1. Function Evaluation (`evaluate_function`)
We use `numpy` to handle math expressions.
- **Dynamic Calculation**: We take the string from the user (e.g., `x^2`), replace `^` with `**` (Python's power operator), and use Python's `eval` function. 
- **Safety**: We limit `eval` to only a specific set of safe math functions (`sin`, `cos`, `tan`, etc.) to prevent malicious code execution.
- **Efficiency**: `numpy` allows us to evaluate the function for hundreds of points at once!

## 2. Finding Intersections (`find_intersection`)
How do we find where two lines cross? 
We define a new function: `diff(x) = f1(x) - f2(x)`.
When these two functions are equal, `diff(x)` must be **zero**.

### The Strategy:
- **Phase 1: Scanning**: We scan the X-axis (from -12 to 12) looking for a "sign change". If `diff(x)` is positive at one point and negative at the next, a crossing **must** exist between them (Bolzano's Theorem).
- **Phase 2: Bisection Method**: Once we find a sign change between point `a` and `b`, we zoom in:
  1. Find the `mid` point.
  2. If the sign change happens between `a` and `mid`, move `b` to `mid`.
  3. Otherwise, move `a` to `mid`.
  4. Repeat this 20 times to get a very precise answer.

## 3. Data Flow
1. **Frontend (JS)**: Sends the functions (e.g., `x^2`, `2x+8`) to the Python Backend.
2. **Backend (Python)**:
   - Calculates 400 points for the graph.
   - Finds intersection points using the Bisection method.
   - Returns everything as JSON.
3. **Frontend (JS)**: Simply renders the points using `Plotly.js`.
