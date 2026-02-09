from scipy.stats import ttest_ind
import pandas as pd


# Загружаем данные
df = pd.read_csv('ab_test_results.csv')

# Берем только тех, кто совершил покупку
rev_a = df[(df['group'] == 'A') & (df['converted'] == 1)]['revenue']
rev_b = df[(df['group'] == 'B') & (df['converted'] == 1)]['revenue']

t_stat, p_val_rev = ttest_ind(rev_a, rev_b, equal_var=False)

print(f"\nСравнение среднего чека (AOV):")
print(f"P-value для AOV: {p_val_rev:.4f}")
