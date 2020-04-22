from sklearn.model_selection import train_test_split
import pandas as pd

df_data = pd.DataFrame(test.data)
df_labels = pd.DataFrame(test.target)

def min_max_normalize(lst):
    normalized = []
    
    for value in lst:
        normalized_num = (value - min(lst)) / (max(lst) - min(lst))
        normalized.append(normalized_num)
    
    return normalized

    for x in range(len(df_data.columns)):
        df_data[x] = min_max_normalize(df_data[x])
    df_data.describe()