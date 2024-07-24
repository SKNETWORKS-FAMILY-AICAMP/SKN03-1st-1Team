from tests.car_data_extractor import CarDataExtractor
import time

car_extractor = CarDataExtractor()
car_extractor.driver.get('https://carcharts-free.carisyou.net/')
time.sleep(7)

brand_model_map = car_extractor.get_brand_and_model_lists()

filters = {
    "모델": [
        [("기간별", "model_cate1"), ("성별/연령별", "model_cate2"), ("연료별", "model_cate3"), ("지역별", "model_cate4")],
        "기간",
        list(brand_model_map.items())
    ],
    "브랜드": [
        [("국산", "brand_cate11"), ("수입", "brand_cate12")],
        ("남성", "brand_cate21"), ("여성", "brand_cate22"), ("법인", "brand_cate23"), "기간"
    ],
    "TOP10": [
        [("국산", "top10_cate1"), ("수입", "top10_cate2")],
        "기간"
    ]
}

periods = ["2023.01", "2023.02", "2023.03", "2023.04", "2023.05", "2023.06", "2023.07", "2023.08", "2023.09", "2023.10", "2023.11", "2023.12",
"2024.01", "2024.02", "2024.03", "2024.04", "2024.05", "2024.06"]

# 필터 조합 생성
filter_combinations = CarDataExtractor.generate_combinations(filters, periods)

processed_combinations = set()
for combination in filter_combinations:
    combination_tuple = tuple(combination)
    if combination_tuple not in processed_combinations:
        car_extractor.select_filter_and_extract_data(combination)
        processed_combinations.add(combination_tuple)
