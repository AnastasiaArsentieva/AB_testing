import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Загружаем данные
df = pd.read_csv('ab_test_results.csv')

# Настройка стиля
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

# Строим график конверсии с 95% доверительными интервалами (ci=95)
ax = sns.barplot(x='group', y='converted', data=df, capsize=.1, palette='viridis')

# Добавляем подписи
plt.title('Конверсия по группам с 95% доверительным интервалом', fontsize=15)
plt.ylabel('Conversion Rate (среднее)', fontsize=12)
plt.xlabel('Группа (A - Скидка, B - Доставка)', fontsize=12)

# Добавим проценты на столбцы для наглядности
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2%}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center', va = 'center',
                xytext = (0, 9),
                textcoords = 'offset points')

plt.show()

# Задаем бизнес-параметры
COGS_RATIO = 0.6  # Себестоимость 60%
SHIPPING_COST = 300  # Стоимость доставки для компании в группе B


# Считаем метрики для каждого пользователя
def calculate_metrics(row):
    revenue = row['revenue']
    if row['converted'] == 0:
        return pd.Series([0, 0], index=['aov', 'profit'])

    # Расчет маржи (Profit)
    if row['group'] == 'A':
        # Группа А: выручка уже со скидкой (мы так генерировали), затрат на доставку нет
        profit = revenue - (revenue * COGS_RATIO)
    else:
        # Группа B: выручка полная, но вычитаем себестоимость и стоимость доставки
        profit = revenue - (revenue * COGS_RATIO) - SHIPPING_COST

    return pd.Series([revenue, profit], index=['aov', 'profit'])


# Применяем расчеты
df[['aov_val', 'profit_val']] = df.apply(calculate_metrics, axis=1)

# Агрегируем результаты
business_results = df.groupby('group').agg({
    'converted': 'mean',
    'revenue': ['mean', 'sum'],  # Mean revenue здесь — это ARPU (выручка на одного вошедшего в тест)
    'profit_val': ['mean', 'sum']  # Mean profit — это AMPU (прибыль на пользователя)
}).round(2)

print(business_results)
