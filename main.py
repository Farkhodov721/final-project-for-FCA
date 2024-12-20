from flask import Flask, render_template, request

app = Flask(__name__)

app.jinja_env.globals.update(zip=zip)

def binary_to_gray(binary):
    return binary ^ (binary >> 1)

def generate_gray_code(n_bits):
    return [f"{binary_to_gray(i):0{n_bits}b}" for i in range(2 ** n_bits)]


def generate_boolean_expression(cell_values, num_variables):
    variables = ['A', 'B', 'C', 'D'][:num_variables]
    minterms = []

    # Iterate through cell values to identify '1' cells
    for index, value in enumerate(cell_values):
        if value == "1" or value == 1:  # Only include cells with '1'
            binary_index = bin(index)[2:].zfill(num_variables)  # Convert index to binary
            term = ""
            for i, bit in enumerate(binary_index):
                if bit == "1":
                    term += variables[i]  # Add variable for a '1' bit
                else:
                    term += f"{variables[i]}'"  # Add complemented variable for a '0' bit
            minterms.append(term)

    return " + ".join(minterms) if minterms else "0"


def get_kmap_labels(num_variables):
    rows = []
    cols = []
    if num_variables == 2:
        rows = ['0', '1']
        cols = ['0', '1']
    elif num_variables == 3:
        rows = ['0', '1']
        cols = generate_gray_code(2)
    elif num_variables == 4:
        rows = generate_gray_code(2)
        cols = generate_gray_code(2)

    return rows, cols

@app.route("/", methods=["GET", "POST"])

def index():
    num_variables = None
    cell_values = None
    kmap_matrix = []
    rows = []
    cols = []
    boolean_expression = None

    if request.method == "POST":
        num_variables = int(request.form.get("num_variables"))
        cell_values = [request.form.get(f"cell_{i}", "0") for i in range(2 ** num_variables)]

        cell_values = [int(value) if value in ["0", "1"] else 0 for value in cell_values]

        rows, cols = get_kmap_labels(num_variables)

        for row in rows:
            row_data = []
            for col in cols:
                gray_row = int(row, 2)
                gray_col = int(col, 2)
                index = (gray_row << len(col)) + gray_col  # Calculate index from Gray codes
                row_data.append(cell_values[index])  # Fill the matrix cell
            kmap_matrix.append(row_data)

        # Generate the Boolean expression in SOP form
        boolean_expression = generate_boolean_expression(cell_values, num_variables)

    return render_template(
        "index.html",
        num_variables=num_variables,
        rows=rows,
        cols=cols,
        kmap_matrix=kmap_matrix,
        boolean_expression=boolean_expression,
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
