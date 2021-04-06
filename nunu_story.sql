/*
 Navicat Premium Data Transfer

 Source Server         : pujic
 Source Server Type    : MySQL
 Source Server Version : 50731
 Source Host           : localhost:3306
 Source Schema         : nunu_story

 Target Server Type    : MySQL
 Target Server Version : 50731
 File Encoding         : 65001

 Date: 06/04/2021 13:18:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for author
-- ----------------------------
DROP TABLE IF EXISTS `author`;
CREATE TABLE `author`  (
  `author_id` int(11) NOT NULL AUTO_INCREMENT,
  `author_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`author_id`) USING BTREE,
  UNIQUE INDEX `author_name`(`author_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10579 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for book
-- ----------------------------
DROP TABLE IF EXISTS `book`;
CREATE TABLE `book`  (
  `author_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `chapter_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  INDEX `author_id`(`author_id`) USING BTREE,
  INDEX `book_id`(`book_id`) USING BTREE,
  CONSTRAINT `book_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `author` (`author_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `book_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `book_info` (`book_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for book_info
-- ----------------------------
DROP TABLE IF EXISTS `book_info`;
CREATE TABLE `book_info`  (
  `book_id` int(11) NOT NULL AUTO_INCREMENT,
  `book_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `author_id` int(11) NOT NULL,
  PRIMARY KEY (`book_id`) USING BTREE,
  UNIQUE INDEX `book_name`(`book_name`, `author_id`) USING BTREE,
  INDEX `author_id`(`author_id`) USING BTREE,
  CONSTRAINT `book_info_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `author` (`author_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10579 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Procedure structure for save_story_message
-- ----------------------------
DROP PROCEDURE IF EXISTS `save_story_message`;
delimiter ;;
CREATE PROCEDURE `save_story_message`(IN a_ VARCHAR ( 100 ), IN b_ VARCHAR ( 100 ), IN c_ VARCHAR ( 100 ), IN ct MEDIUMTEXT)
BEGIN
	INSERT IGNORE INTO `author` ( `author_name` )
	VALUES
		( a_ );

	SET @a_id = ( SELECT author_id FROM `author` WHERE author_name = a_ LIMIT 1 );
	INSERT IGNORE INTO `book_info` ( `author_id`, `book_name` )
	VALUES
		( @a_id, b_ );

	SET @b_id = ( SELECT book_id FROM book_info WHERE author_id = @a_id LIMIT 1 );
	INSERT IGNORE INTO `book` ( `author_id`, `book_id`, `chapter_name`, `content` )
	VALUES
		( @a_id, @b_id, c_, ct );

END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
