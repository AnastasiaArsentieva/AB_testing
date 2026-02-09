import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Загружаем данные (убедись, что файл ab_test_results.csv в той же папке)
df = pd.read_csv('ab_test_results.csv')

# 2. Бизнес-параметры (константы)
COGS_RATIO = 0.6    # Себестоимость 60%
SHIPPING_COST = 300 # Стоимость доставки для Группы B

# 3. Создаем колонку profit_val (её-то и не хватало!)
def calculate_profit(row):
    if row['converted'] == 0:
        return 0
    revenue = row['revenue']
    if row['group'] == 'A':
        # Скидка уже в revenue, дополнительных затрат нет
        return revenue - (revenue * COGS_RATIO)
    else:
        # Доставка бесплатная для клиента, но платная для нас
        return revenue - (revenue * COGS_RATIO) - SHIPPING_COST

df['profit_val'] = df.apply(calculate_profit, axis=1)

# 4. Сегментация (Точка безубыточности = 3000)
def get_segment(revenue):
    if revenue == 0: return 'No purchase'
    return 'VIP (>3000)' if revenue > 3000 else 'Standard (<3000)'

df['segment'] = df['revenue'].apply(get_segment)

# 5. Анализ прибыли по сегментам (только для тех, кто купил)
purchases_only = df[df['converted'] == 1]
segment_analysis = purchases_only.groupby(['segment', 'group'])['profit_val'].mean().unstack()

print("--- Средняя прибыль с ОДНОГО ЗАКАЗА по сегментам ---")
print(segment_analysis)

# 6. Визуализация
plt.figure(figsize=(10, 6))
sns.barplot(x='segment', y='profit_val', hue='group', data=purchases_only, palette='magma')
plt.axhline(0, color='black', linewidth=1)
plt.title('Экономика сегментов: Скидка (A) vs Доставка (B)', fontsize=14)
plt.ylabel('Чистая прибыль с заказа (руб.)')
plt.show()

