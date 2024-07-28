from car_data_extractor import CarDataExtractor
import time

car_extractor = CarDataExtractor()
car_extractor.driver.get('https://carcharts-free.carisyou.net/')
time.sleep(7)

brand_model_map = car_extractor.get_brand_and_model_lists()

# 특정 브랜드 필터링 (예: 현대, 기아, 제네시스, KGM)
target_brands = ["현대", "기아", "제네시스", "KGM"]
filtered_brand_model_map = {brand: models for brand, models in brand_model_map.items() if brand in target_brands}

filters = {
    "모델": [
        [("지역별", "model_cate4")],
        "기간",
        list(filtered_brand_model_map.items())
    ]
}

periods = ["2023.10", "2023.11", "2023.12",
"2024.01", "2024.02", "2024.03", "2024.04", "2024.05", "2024.06"]

# 필터 조합 생성
filter_combinations = CarDataExtractor.generate_combinations(filters, periods)
filter_combinations.sort()

start_index = 24  # 필요한 경우 시작 인덱스를 변경 제네시스 g80

processed_combinations = set()
for combination in filter_combinations[start_index:]:
    combination_tuple = tuple(combination)
    if combination_tuple not in processed_combinations:
        car_extractor.select_filter_and_extract_data(combination)
        processed_combinations.add(combination_tuple)