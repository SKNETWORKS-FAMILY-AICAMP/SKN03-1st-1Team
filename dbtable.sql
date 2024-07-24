CREATE TABLE `model` (
	  `model_id`		INT				NOT NULL 	AUTO_INCREMENT 	PRIMARY KEY
	, `model_name`		CHAR(14) 		NOT NULL
	, `year`			YEAR			NOT NULL
	, `month`			TINYINT			NOT NULL
	, `region`			CHAR(14)		NOT NULL
	, `car_cnt`			INT				NULL
	, `brand_id`		INT				NOT NULL
);

CREATE TABLE `faq` (
	  `faq_id`			INT				NOT NULL 	AUTO_INCREMENT 	PRIMARY KEY
	, `question`		VARCHAR(200)	NOT NULL
	, `answer`			VARCHAR(2000)	NOT NULL
	, `category`		CHAR(30)		NOT NULL
	, `is_most`			CHAR(1)			NULL
	, `brand_id`		INT				NOT NULL
);

CREATE TABLE `brand` (
	  `brand_id`		INT				NOT NULL	AUTO_INCREMENT 	PRIMARY KEY
	, `brand_name`		CHAR(12)		NOT NULL
);