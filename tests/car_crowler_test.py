from car_data_extractor import CarDataExtractor
import time

car_extractor = CarDataExtractor()
car_extractor.driver.get('https://carcharts-free.carisyou.net/')
time.sleep(7)

brand_model_map = car_extractor.get_brand_and_model_lists()

#print(brand_model_map)

filters = {
    "모델": [
        [("기간별", "model_cate1"), ("지역별", "model_cate4")],
        "기간",
        list(brand_model_map.items())
    ]
}


periods = ["2023.01", "2023.02", "2023.03", "2023.04", "2023.05", "2023.06", "2023.07", "2023.08", "2023.09", "2023.10", "2023.11", "2023.12",
"2024.01", "2024.02", "2024.03", "2024.04", "2024.05", "2024.06"]

# 필터 조합 생성
filter_combinations = CarDataExtractor.generate_combinations(filters, periods)
filter_combinations.sort()
#print(len(filter_combinations))

start_index = 292

processed_combinations = set()
for combination in filter_combinations[start_index:]:
    combination_tuple = tuple(combination)
    if combination_tuple not in processed_combinations:
        car_extractor.select_filter_and_extract_data(combination)
        processed_combinations.add(combination_tuple)
