import pandas as pd
import numpy as np

# Настройки
np.random.seed(42)
n_users = 8000 # Общий размер выборки

# Генерируем ID и распределяем по группам (A - скидка 10%, B - бесплатная доставка)
data = pd.DataFrame({
    'user_id': np.arange(n_users),
    'group': np.random.choice(['A', 'B'], size=n_users)
})

# Задаем вероятности конверсии (пусть B будет чуть лучше)
p_a = 0.10  # 10%
p_b = 0.12  # 12%

# Генерируем факт покупки (1 - купил, 0 - нет)
data['converted'] = data.apply(
    lambda x: np.random.binomial(1, p_a if x['group'] == 'A' else p_b),
    axis=1
)

# Добавим сумму чека для тех, кто совершил покупку
data['revenue'] = data.apply(
    lambda x: np.random.normal(2000, 500) if x['converted'] == 1 else 0,
    axis=1
).clip(lower=0) # Чек не может быть отрицательным

print(data.head())
data.to_csv('ab_test_results.csv', index=False)
