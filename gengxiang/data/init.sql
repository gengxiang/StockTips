CREATE TABLE `gx_stock_data` (
`id` bigint unsigned NOT NULL AUTO_INCREMENT,
`code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
`name` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
`price` float(16,2) NOT NULL DEFAULT '0.00',
`volume` int NOT NULL DEFAULT '0',
`t_volume` int NOT NULL DEFAULT '0',
`t_change` float(6,2) NOT NULL DEFAULT '0.00',
`t_date` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
PRIMARY KEY (`id`),
KEY `idx_stock_code_date` (`code`,`t_date`,`price`,`t_volume`) USING BTREE
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;