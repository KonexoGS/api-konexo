from math import pow, sqrt
from fastapi import HTTPException

class MathCalcs:

    @staticmethod
    def correlation_calc(first_data, second_data):
        x_values = []
        y_values = []

        for i in range(len(first_data)):
            x_vals = first_data[i].main_values
            y_vals = second_data[i].main_values
            for j in range(min(len(x_vals), len(y_vals))):
                x = x_vals[j].value
                y = y_vals[j].value
                if x is None or y is None:
                    continue
                x_values.append(x)
                y_values.append(y)

        length = len(x_values)
        if length < 2:
            raise HTTPException(status_code=400, detail="Não há dados suficientes para calcular a correlação.")

        average_x = sum(x_values) / length
        average_y = sum(y_values) / length

        above = sum((x - average_x) * (y - average_y) for x, y in zip(x_values, y_values))
        below_x = sum((x - average_x) ** 2 for x in x_values)
        below_y = sum((y - average_y) ** 2 for y in y_values)

        if below_x == 0 or below_y == 0:
            raise HTTPException(status_code=400, detail="Ocorreu uma variância zero. Correlação indefinida.")

        return above / (sqrt(below_x) * sqrt(below_y))