import pandas as pd

def calculate_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    distance_matrix = pd.pivot_table(df, values='distance', index='id_start', columns='id_end', fill_value=0)
    distance_matrix += distance_matrix.T
    return distance_matrix

def unroll_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    unrolled_df = df.unstack().reset_index(name='distance')
    unrolled_df.columns = ['id_start', 'id_end', 'distance']
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]
    return unrolled_df

def find_ids_within_ten_percentage_threshold(df: pd.DataFrame, reference_id: int) -> pd.Series:
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    within_threshold_ids = df.groupby('id_start')['distance'].mean().between(
        reference_avg_distance * 0.9, reference_avg_distance * 1.1
    ).index
    return within_threshold_ids.sort_values()

def calculate_toll_rate(df: pd.DataFrame) -> pd.DataFrame:
    df['moto'] = df['distance'] * 0.8
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6
    return df

import pandas as pd

import pandas as pd

import pandas as pd

def calculate_time_based_toll_rates(df):
    df['start_day'] = df['id_start'].astype(str).str[:2].apply(lambda x: pd.to_datetime(x, format='%d').day_name())
    df['end_day'] = df['id_end'].astype(str).str[:2].apply(lambda x: pd.to_datetime(x, format='%d').day_name())
    
    df['start_time'] = pd.to_datetime('2023-01-01 ' + df['id_start'].astype(str).str[2:], format='%Y-%m-%d %H%M%S').dt.time
    df['end_time'] = pd.to_datetime('2023-01-01 ' + df['id_end'].astype(str).str[2:], format='%Y-%m-%d %H%M%S').dt.time
    
    df['discount_factor'] = 1.0

    weekday_discount = {
        (0, pd.to_datetime('00:00:00').time(), pd.to_datetime('10:00:00').time()): 0.8,
        (0, pd.to_datetime('10:00:00').time(), pd.to_datetime('18:00:00').time()): 1.2,
        (0, pd.to_datetime('18:00:00').time(), pd.to_datetime('23:59:59').time()): 0.8,
        (1, pd.to_datetime('00:00:00').time(), pd.to_datetime('23:59:59').time()): 0.7,
        (2, pd.to_datetime('00:00:00').time(), pd.to_datetime('23:59:59').time()): 0.7,
        (3, pd.to_datetime('00:00:00').time(), pd.to_datetime('23:59:59').time()): 0.7,
        (4, pd.to_datetime('00:00:00').time(), pd.to_datetime('23:59:59').time()): 0.7,
        (5, pd.to_datetime('00:00:00').time(), pd.to_datetime('23:59:59').time()): 0.7,
        (6, pd.to_datetime('00:00:00').time(), pd.to_datetime('23:59:59').time()): 0.7
    }

    for (weekday, start_time, end_time), discount_factor in weekday_discount.items():
        mask = (
            (df['start_day'] == weekday) &
            (df['start_time'] >= start_time) &
            (df['end_time'] <= end_time)
        )
        df.loc[mask, 'discount_factor'] = discount_factor

    vehicle_types = ['moto', 'car', 'rv', 'bus', 'truck']
    for vehicle_type in vehicle_types:
        df[vehicle_type] = df[vehicle_type] * df['discount_factor']

    df.drop(columns=['discount_factor'], inplace=True)
    return df



df = pd.read_csv('datasets/dataset-3.csv')

distance_matrix = calculate_distance_matrix(df)
print("Question 1 - Distance Matrix:")
print(distance_matrix)
print("\n")

unrolled_df = unroll_distance_matrix(distance_matrix)
print("Question 2 - Unrolled Distance Matrix:")
print(unrolled_df)
print("\n")

reference_id = 1001402 
within_threshold_ids = find_ids_within_ten_percentage_threshold(unrolled_df, reference_id)
print(f"Question 3 - IDs within 10% of the average distance for reference ID {reference_id}:")
print(within_threshold_ids)
print("\n")

toll_rate_df = calculate_toll_rate(unrolled_df)
print("Question 4 - Toll Rate:")
print(toll_rate_df)
print("\n")

time_based_toll_df = calculate_time_based_toll_rates(unrolled_df)
print("Question 5 - Time-Based Toll Rates:")
print(time_based_toll_df)