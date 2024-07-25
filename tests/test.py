import pandas as pd
import os
# 폴더 경로 및 파일 경로 지정
folder_path = '/Users/seungminoh/SKN03-1st-1Team/data'
file_path = os.path.join(folder_path, 'model.csv')
cleaned_file_path = os.path.join(folder_path, 'cleaned_model.csv')

# CSV 파일 읽기
df = pd.read_csv(file_path, on_bad_lines='skip')

# NaN이 있는 행 제거
df_cleaned = df.dropna()

# model_id 행 제거
df_cleaned = df_cleaned.drop(columns=['model_id'])

# year, month, car_cnt, brand_id를 정수형으로 변환
df_cleaned['year'] = df_cleaned['year'].astype(int)
df_cleaned['month'] = df_cleaned['month'].astype(int)
df_cleaned['car_cnt'] = df_cleaned['car_cnt'].astype(int)
df_cleaned['brand_id'] = df_cleaned['brand_id'].astype(int)

# 정제된 데이터 저장
df_cleaned.to_csv(cleaned_file_path, index=False)

print(f"Cleaned CSV file has been saved to {cleaned_file_path}")