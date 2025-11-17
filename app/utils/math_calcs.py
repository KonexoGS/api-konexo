from math import pow, sqrt
from fastapi import HTTPException
from datetime import datetime

all_years_counted_default = datetime.now().year - 1975


class MathCalcs:

    @staticmethod
    def average_calc(all_values):
        count_years = len(all_values)
        if count_years < 2:
            raise HTTPException(status_code=400, detail="Não há dados suficientes para calcular a variância.")
        
        average = sum(all_values) / count_years
        sum_pow = 0
        for val in all_values: # type: ignore
            sum_pow += pow((val - average), 2)
            
        return {"result": sum_pow / (count_years - 1), "countYears": count_years if count_years <= 100 else all_years_counted_default }

    @staticmethod
    def weighted_average_calc(default_data, weight_data):
        above = 0.0
        below = 0.0
        count_years = 0

        for i in range(len(default_data)):
            main_values = default_data[i].main_values
            weight_values = weight_data[i].main_values

            for j in range(min(len(main_values), len(weight_values))):
                d = main_values[j].value
                w = weight_values[j].value

                if d is None or w is None:
                    continue
                above += d * w
                below += w
                count_years += 1

        if below == 0:
            raise HTTPException(status_code=400, detail="Não há pesos válidos para calcular a média ponderada.")

        return {"result": above / below, "countYears": count_years if count_years <= 100 else all_years_counted_default}

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

        return {"result": above / (sqrt(below_x) * sqrt(below_y)), "countYears": length if length <= 100 else all_years_counted_default }