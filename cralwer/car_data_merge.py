import os
import pandas as pd

# 원래의 model.csv 파일 로드
model_df = pd.read_csv('data/model.csv')

# 폴더에서 추출된 데이터 파일 리스트 가져오기
extracted_data_folder = 'extracted_data'
extracted_files = os.listdir(extracted_data_folder)

# 관심 브랜드 목록
brands = ["현대", "기아", "제네시스", "KGM"]

# 추출된 데이터를 담을 데이터프레임 리스트
extracted_data_list = []

# 추출된 데이터 파일 로드 및 합치기
for file_name in extracted_files:
    if file_name.endswith('.csv'):
        # 파일명에서 정보를 추출
        file_info = file_name.replace('.csv', '').split('_')
        category, subcategory, date, brand, model = file_info

        # 관심 브랜드만 필터링
        if brand in brands:
            file_path = os.path.join(extracted_data_folder, file_name)
            extracted_df = pd.read_csv(file_path)
            
            # 데이터프레임에 정보를 추가
            extracted_df['year'], extracted_df['month'] = date.split('.')
            extracted_df['brand'] = brand
            extracted_df['model'] = model
            
            # 데이터를 리스트에 추가
            extracted_data_list.append(extracted_df)

# 모든 추출된 데이터 합치기
if extracted_data_list:
    all_extracted_data = pd.concat(extracted_data_list, ignore_index=True)
else:
    all_extracted_data = pd.DataFrame()

# 'JUSO_SIDO'를 'region'으로 변경
all_extracted_data.rename(columns={'JUSO_SIDO': 'region'}, inplace=True)

# 모델, 연도, 월, 브랜드로 그룹화하여 지역별 합계 구하기
region_sums = all_extracted_data.groupby(['model', 'year', 'month', 'region'])['CNT'].sum().reset_index()

# 데이터가 없는 모델을 제거하고 데이터가 있는 경우 region별로 확장
merged_data = []
for _, row in model_df.iterrows():
    model_name = row['model_name']
    year = str(row['year'])
    month = str(row['month']).zfill(2)
    brand_id = row['brand_id']
    
    relevant_data = region_sums[(region_sums['model'] == model_name) &
                                (region_sums['year'] == year) &
                                (region_sums['month'] == month)]
    
    if not relevant_data.empty:
        for _, data_row in relevant_data.iterrows():
            merged_data.append({
                'model_name': model_name,
                'year': year,
                'month': month,
                'region': data_row['region'],
                'car_cnt': data_row['CNT'],
                'brand_id': brand_id
            })

# 최종 데이터프레임 생성
final_df = pd.DataFrame(merged_data)

# 최종 데이터 저장 - 후에 data/ 폴더로 이동
final_df.to_csv('merged_data.csv', index=False)