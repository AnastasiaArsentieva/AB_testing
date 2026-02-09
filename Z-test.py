import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

# Загружаем данные
df = pd.read_csv('ab_test_results.csv')

# Считаем количество успехов и общее число попыток
stats = df.groupby('group')['converted'].agg(['sum', 'count'])

successes = stats['sum'].values  # Массив [Успехи_А, Успехи_B]
nobs = stats['count'].values      # Массив [Всего_А, Всего_B]

# Запускаем Z-тест
z_stat, p_val = proportions_ztest(successes, nobs)

print(f"Статистика Z: {z_stat:.4f}")
print(f"p-value: {p_val:.4f}")

if p_val < 0.05:
    print("Результат статистически значим! Отвергаем нулевую гипотезу.")
else:
    print("Разница случайна. Не удалось отвергнуть нулевую гипотезу.")
