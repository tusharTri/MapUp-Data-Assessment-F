import pandas as pd
import numpy as np


def generate_car_matrix(df: pd.DataFrame) -> pd.DataFrame:
    df = df.pivot(index='id_1', columns='id_2', values='car')
    df = df.fillna(0)
    for i in range(min(df.shape)):
        df.iloc[i, i] = 0

    # Display the resulting DataFrame
    return df

def get_type_count(df: pd.DataFrame) -> dict:
    bins = [-np.inf, 15, 25, np.inf]
    labels = ['low', 'medium', 'high']
    df['car_type'] = pd.cut(df['car'], bins=bins, labels=labels)
    type_count = df['car_type'].value_counts().to_dict()
    return dict(sorted(type_count.items()))

def get_bus_indexes(df: pd.DataFrame) -> list:
    mean_bus = df['bus'].mean()
    bus_indexes = df.index[df['bus'] > 2 * mean_bus].tolist()
    return sorted(bus_indexes)

def filter_routes(df: pd.DataFrame) -> list:
    avg_truck_by_route = df.groupby('route')['truck'].mean()
    routes_filtered = avg_truck_by_route.index[avg_truck_by_route > 7].tolist()
    return sorted(routes_filtered)


def multiply_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    modified_matrix = matrix.apply(lambda x: np.where(x > 20, x * 0.75, x * 1.25))
    return modified_matrix.round(1)



def time_check(df: pd.DataFrame) -> pd.Series:
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %H:%M:%S')
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %H:%M:%S')
    df['day_of_week'] = df['start_datetime'].dt.day_name()

    completeness_check = df.groupby(['id', 'id_2'])[['start_datetime', 'end_datetime', 'day_of_week']].apply(
        lambda group: (
            (group['start_datetime'].min() == pd.to_datetime('00:00:00')) &
            (group['end_datetime'].max() == pd.to_datetime('23:59:59')) &
            (set(group['day_of_week']) == set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']))
        )
    )

    return completeness_check

df1 = pd.read_csv('datasets/dataset-1.csv')


df2 = pd.read_csv('datasets/dataset-2.csv')
result_question_1 = generate_car_matrix(df1)
result_question_2 = get_type_count(df1)
result_question_3 = get_bus_indexes(df1)
result_question_4 = filter_routes(df1)
result_question_5 = multiply_matrix(result_question_1)
result_question_6 = time_check(df2)
print("Result of Question 1 (generate_car_matrix):")
print(result_question_1)

print("\nResult of Question 2 (get_type_count):")
print(result_question_2)

print("\nResult of Question 3 (get_bus_indexes):")
print(result_question_3)

print("\nResult of Question 4 (filter_routes):")
print(result_question_4)

print("\nResult of Question 5 (multiply_matrix):")
print(result_question_5)

print("\nResult of Question 6 (time_check):")
print(result_question_6)
result_question_6_counts = result_question_6.value_counts()

print("False:", result_question_6_counts.get(False, 0))
print("True:", result_question_6_counts.get(True, 0))

