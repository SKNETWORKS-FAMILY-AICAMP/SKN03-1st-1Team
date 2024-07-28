import os
import pandas as pd

# 폴더 경로 및 파일 경로 지정
folder_path = '/Users/seungminoh/SKN03-1st-1Team/data'
exclude_file_path = os.path.join(folder_path, 'faq_data.csv')
brand_output_path = os.path.join(folder_path, 'brand.csv')
model_output_path = os.path.join(folder_path, 'model.csv')
cleaned_file_path = os.path.join(folder_path, 'cleaned_model.csv')

# 폴더 안의 모든 CSV 파일 읽기
all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 제외할 파일 제거
all_files = [f for f in all_files if os.path.join(folder_path, f) != exclude_file_path]

# 빈 데이터프레임 생성
combined_df = pd.DataFrame()

# 각 파일을 읽어서 병합
for file in all_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path, on_bad_lines='skip')
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# EXTRACT_DE가 비어있는 경우 0으로 대체
combined_df['EXTRACT_DE'] = combined_df['EXTRACT_DE'].astype(str).fillna('0')

# 브랜드와 차종을 CONVAL에서 분리
combined_df[['brand_name', 'model_name']] = combined_df['CONVAL'].str.split(' ', n=1, expand=True)

# year와 month 컬럼 생성
combined_df['year'] = combined_df['EXTRACT_DE'].str[:4]
combined_df['month'] = combined_df['EXTRACT_DE'].str[4:6]

# 컬럼 이름 변경 및 필요한 컬럼 선택
combined_df = combined_df.rename(columns={'CNT': 'car_cnt'})
combined_df = combined_df[['brand_name', 'model_name', 'car_cnt', 'year', 'month']]

# car_cnt를 정수형으로 변환
combined_df['car_cnt'] = combined_df['car_cnt'].astype(int)

# brand 테이블 생성
brand_df = combined_df[['brand_name']].drop_duplicates().reset_index(drop=True)

# 기아와 제네시스에 특정 brand_id 할당
brand_id_map = {
    '기아': 1,
    '제네시스': 2
}
brand_df['brand_id'] = brand_df['brand_name'].map(brand_id_map)

# 나머지 브랜드의 brand_id를 재할당하여 1과 2를 제외한 숫자로 설정
current_id = 3
for idx, row in brand_df.iterrows():
    if pd.isna(row['brand_id']):
        while current_id in brand_id_map.values():
            current_id += 1
        brand_df.at[idx, 'brand_id'] = current_id
        current_id += 1

# model 테이블 생성
model_df = combined_df.merge(brand_df, on='brand_name')
model_df['model_id'] = model_df.index + 1

# 필요한 컬럼 선택
model_df = model_df[['model_id', 'model_name', 'year', 'month', 'car_cnt', 'brand_id']]

# NaN이 있는 행 제거
model_df_cleaned = model_df.dropna()

# model_id 행 제거
model_df_cleaned = model_df_cleaned.drop(columns=['model_id'])

# year, month, car_cnt, brand_id를 정수형으로 변환
model_df_cleaned['year'] = model_df_cleaned['year'].astype(int)
model_df_cleaned['month'] = model_df_cleaned['month'].astype(int)
model_df_cleaned['car_cnt'] = model_df_cleaned['car_cnt'].astype(int)
model_df_cleaned['brand_id'] = model_df_cleaned['brand_id'].astype(int)

# CSV 파일 저장
brand_df.to_csv(brand_output_path, index=False)
model_df.to_csv(model_output_path, index=False)
model_df_cleaned.to_csv(cleaned_file_path, index=False)

print(f"CSV files have been created:\n{brand_output_path}\n{model_output_path}\nCleaned CSV file has been saved to {cleaned_file_path}")