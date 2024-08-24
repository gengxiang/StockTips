/*
 Navicat Premium Data Transfer

 Source Server         : 耿翔
 Source Server Type    : MySQL
 Source Server Version : 80030
 Source Host           : localhost:3366
 Source Schema         : stock_tips

 Target Server Type    : MySQL
 Target Server Version : 80030
 File Encoding         : 65001

 Date: 15/05/2024 23:20:56
*/

SET NAMES utf8mb4;
SET
FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for stock_data_detail
-- ----------------------------
DROP TABLE IF EXISTS `stock_data_detail`;
CREATE TABLE `stock_data_detail`
(
    `id`    bigint(0) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id\r\n',
    `code`  varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '代码',
    `name`  varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '名称',
    `date`  varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '时间',
    `price` float(16, 2
) NOT NULL DEFAULT 0.00 COMMENT '价格',
  `stop_price` float(16, 2) NOT NULL COMMENT '涨停价',
  `amp` float(6, 2) NOT NULL DEFAULT 0.00 COMMENT '涨跌幅%',
  `amo` int(0) NOT NULL DEFAULT 0 COMMENT '成交额（万元）',
  `mc` float(16, 2) NOT NULL DEFAULT 0.00 COMMENT '总市值',
  `qrr` float(20, 2) NOT NULL DEFAULT 0.00 COMMENT '量比',
  `hs` float(6, 2) NOT NULL DEFAULT 0.00 COMMENT '换手率%',
  `per` float(20, 2) NOT NULL DEFAULT 0.00 COMMENT '市盈率',
  `pb` float(20, 2) NOT NULL DEFAULT 0.00 COMMENT '市净率',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_code_date`(`code`, `date`) USING BTREE,
  INDEX `idx_name_date`(`name`, `date`) USING BTREE,
  INDEX `idx_date`(`date`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1204382 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET
FOREIGN_KEY_CHECKS = 1;
