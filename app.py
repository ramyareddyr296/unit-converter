import math

from flask import Flask, render_template, request

app = Flask(__name__)

LENGTH_UNITS = {
    "Meters": 1,
    "Kilometers": 1000,
    "Centimeters": 0.01,
    "Feet": 0.3048,
    "Inches": 0.0254,
}

WEIGHT_UNITS = {
    "Kilograms": 1,
    "Grams": 0.001,
    "Pounds": 0.45359237,
    "Ounces": 0.028349523125,
}

TEMPERATURE_UNITS = ["Celsius", "Fahrenheit", "Kelvin"]


def convert_measurement(units, template):
    result = None
    error = None

    if request.method == "POST":
        try:
            value = float(request.form["value"])
            from_unit = request.form["from_unit"]
            to_unit = request.form["to_unit"]

            if not math.isfinite(value):
                error = "Please enter a finite number."
            elif value < 0:
                error = "Please enter a positive value or zero."
            else:
                converted = value * units[from_unit] / units[to_unit]

                if not math.isfinite(converted):
                    error = "The value is too large to convert."
                else:
                    result = (
                        f"{value:g} {from_unit} = "
                        f"{converted:.6g} {to_unit}"
                    )

        except (ValueError, KeyError, OverflowError):
            error = "Please enter a valid number and select valid units."

    return render_template(
        template,
        units=units,
        result=result,
        error=error,
    )


@app.route("/", methods=["GET", "POST"])
@app.route("/length", methods=["GET", "POST"])
def length():
    return convert_measurement(LENGTH_UNITS, "length.html")


@app.route("/weight", methods=["GET", "POST"])
def weight():
    return convert_measurement(WEIGHT_UNITS, "weight.html")


@app.route("/temperature", methods=["GET", "POST"])
def temperature():
    result = None
    error = None

    if request.method == "POST":
        try:
            value = float(request.form["value"])
            from_unit = request.form["from_unit"]
            to_unit = request.form["to_unit"]

            if not math.isfinite(value):
                raise ValueError

            if (
                from_unit not in TEMPERATURE_UNITS
                or to_unit not in TEMPERATURE_UNITS
            ):
                raise ValueError

            # Convert the input temperature to Celsius.
            if from_unit == "Celsius":
                celsius = value
            elif from_unit == "Fahrenheit":
                celsius = (value - 32) * 5 / 9
            else:
                celsius = value - 273.15

            if celsius < -273.15:
                error = "Temperature cannot be below absolute zero."
            else:
                # Convert Celsius to the selected output unit.
                if to_unit == "Celsius":
                    converted = celsius
                elif to_unit == "Fahrenheit":
                    converted = celsius * 9 / 5 + 32
                else:
                    converted = celsius + 273.15

                if not math.isfinite(converted):
                    error = "The value is too large to convert."
                else:
                    result = (
                        f"{value:g} {from_unit} = "
                        f"{converted:.6g} {to_unit}"
                    )

        except (ValueError, KeyError, OverflowError):
            error = "Please enter a valid number and select valid units."

    return render_template(
        "temperature.html",
        units=TEMPERATURE_UNITS,
        result=result,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)