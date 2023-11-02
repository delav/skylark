/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80029
 Source Host           : localhost:3306
 Source Schema         : skylark

 Target Server Type    : MySQL
 Target Server Version : 80029
 File Encoding         : 65001

 Date: 29/10/2023 23:18:26
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
INSERT INTO `auth_group` VALUES (1, 'Inbound');
INSERT INTO `auth_group` VALUES (4, 'Order');
INSERT INTO `auth_group` VALUES (3, 'Wallet');

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 161 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add crontab', 7, 'add_crontabschedule');
INSERT INTO `auth_permission` VALUES (26, 'Can change crontab', 7, 'change_crontabschedule');
INSERT INTO `auth_permission` VALUES (27, 'Can delete crontab', 7, 'delete_crontabschedule');
INSERT INTO `auth_permission` VALUES (28, 'Can view crontab', 7, 'view_crontabschedule');
INSERT INTO `auth_permission` VALUES (29, 'Can add interval', 8, 'add_intervalschedule');
INSERT INTO `auth_permission` VALUES (30, 'Can change interval', 8, 'change_intervalschedule');
INSERT INTO `auth_permission` VALUES (31, 'Can delete interval', 8, 'delete_intervalschedule');
INSERT INTO `auth_permission` VALUES (32, 'Can view interval', 8, 'view_intervalschedule');
INSERT INTO `auth_permission` VALUES (33, 'Can add periodic task', 9, 'add_periodictask');
INSERT INTO `auth_permission` VALUES (34, 'Can change periodic task', 9, 'change_periodictask');
INSERT INTO `auth_permission` VALUES (35, 'Can delete periodic task', 9, 'delete_periodictask');
INSERT INTO `auth_permission` VALUES (36, 'Can view periodic task', 9, 'view_periodictask');
INSERT INTO `auth_permission` VALUES (37, 'Can add periodic tasks', 10, 'add_periodictasks');
INSERT INTO `auth_permission` VALUES (38, 'Can change periodic tasks', 10, 'change_periodictasks');
INSERT INTO `auth_permission` VALUES (39, 'Can delete periodic tasks', 10, 'delete_periodictasks');
INSERT INTO `auth_permission` VALUES (40, 'Can view periodic tasks', 10, 'view_periodictasks');
INSERT INTO `auth_permission` VALUES (41, 'Can add solar event', 11, 'add_solarschedule');
INSERT INTO `auth_permission` VALUES (42, 'Can change solar event', 11, 'change_solarschedule');
INSERT INTO `auth_permission` VALUES (43, 'Can delete solar event', 11, 'delete_solarschedule');
INSERT INTO `auth_permission` VALUES (44, 'Can view solar event', 11, 'view_solarschedule');
INSERT INTO `auth_permission` VALUES (45, 'Can add clocked', 12, 'add_clockedschedule');
INSERT INTO `auth_permission` VALUES (46, 'Can change clocked', 12, 'change_clockedschedule');
INSERT INTO `auth_permission` VALUES (47, 'Can delete clocked', 12, 'delete_clockedschedule');
INSERT INTO `auth_permission` VALUES (48, 'Can view clocked', 12, 'view_clockedschedule');
INSERT INTO `auth_permission` VALUES (49, 'Can add tag', 13, 'add_tag');
INSERT INTO `auth_permission` VALUES (50, 'Can change tag', 13, 'change_tag');
INSERT INTO `auth_permission` VALUES (51, 'Can delete tag', 13, 'delete_tag');
INSERT INTO `auth_permission` VALUES (52, 'Can view tag', 13, 'view_tag');
INSERT INTO `auth_permission` VALUES (53, 'Can add keyword group', 14, 'add_keywordgroup');
INSERT INTO `auth_permission` VALUES (54, 'Can change keyword group', 14, 'change_keywordgroup');
INSERT INTO `auth_permission` VALUES (55, 'Can delete keyword group', 14, 'delete_keywordgroup');
INSERT INTO `auth_permission` VALUES (56, 'Can view keyword group', 14, 'view_keywordgroup');
INSERT INTO `auth_permission` VALUES (57, 'Can add lib keyword', 15, 'add_libkeyword');
INSERT INTO `auth_permission` VALUES (58, 'Can change lib keyword', 15, 'change_libkeyword');
INSERT INTO `auth_permission` VALUES (59, 'Can delete lib keyword', 15, 'delete_libkeyword');
INSERT INTO `auth_permission` VALUES (60, 'Can view lib keyword', 15, 'view_libkeyword');
INSERT INTO `auth_permission` VALUES (61, 'Can add project', 16, 'add_project');
INSERT INTO `auth_permission` VALUES (62, 'Can change project', 16, 'change_project');
INSERT INTO `auth_permission` VALUES (63, 'Can delete project', 16, 'delete_project');
INSERT INTO `auth_permission` VALUES (64, 'Can view project', 16, 'view_project');
INSERT INTO `auth_permission` VALUES (65, 'Can add suite dir', 17, 'add_suitedir');
INSERT INTO `auth_permission` VALUES (66, 'Can change suite dir', 17, 'change_suitedir');
INSERT INTO `auth_permission` VALUES (67, 'Can delete suite dir', 17, 'delete_suitedir');
INSERT INTO `auth_permission` VALUES (68, 'Can view suite dir', 17, 'view_suitedir');
INSERT INTO `auth_permission` VALUES (69, 'Can add test suite', 18, 'add_testsuite');
INSERT INTO `auth_permission` VALUES (70, 'Can change test suite', 18, 'change_testsuite');
INSERT INTO `auth_permission` VALUES (71, 'Can delete test suite', 18, 'delete_testsuite');
INSERT INTO `auth_permission` VALUES (72, 'Can view test suite', 18, 'view_testsuite');
INSERT INTO `auth_permission` VALUES (73, 'Can add test case', 19, 'add_testcase');
INSERT INTO `auth_permission` VALUES (74, 'Can change test case', 19, 'change_testcase');
INSERT INTO `auth_permission` VALUES (75, 'Can delete test case', 19, 'delete_testcase');
INSERT INTO `auth_permission` VALUES (76, 'Can view test case', 19, 'view_testcase');
INSERT INTO `auth_permission` VALUES (77, 'Can add case entity', 20, 'add_caseentity');
INSERT INTO `auth_permission` VALUES (78, 'Can change case entity', 20, 'change_caseentity');
INSERT INTO `auth_permission` VALUES (79, 'Can delete case entity', 20, 'delete_caseentity');
INSERT INTO `auth_permission` VALUES (80, 'Can view case entity', 20, 'view_caseentity');
INSERT INTO `auth_permission` VALUES (81, 'Can add user keyword', 21, 'add_userkeyword');
INSERT INTO `auth_permission` VALUES (82, 'Can change user keyword', 21, 'change_userkeyword');
INSERT INTO `auth_permission` VALUES (83, 'Can delete user keyword', 21, 'delete_userkeyword');
INSERT INTO `auth_permission` VALUES (84, 'Can view user keyword', 21, 'view_userkeyword');
INSERT INTO `auth_permission` VALUES (85, 'Can add setup teardown', 22, 'add_setupteardown');
INSERT INTO `auth_permission` VALUES (86, 'Can change setup teardown', 22, 'change_setupteardown');
INSERT INTO `auth_permission` VALUES (87, 'Can delete setup teardown', 22, 'delete_setupteardown');
INSERT INTO `auth_permission` VALUES (88, 'Can view setup teardown', 22, 'view_setupteardown');
INSERT INTO `auth_permission` VALUES (89, 'Can add variable', 23, 'add_variable');
INSERT INTO `auth_permission` VALUES (90, 'Can change variable', 23, 'change_variable');
INSERT INTO `auth_permission` VALUES (91, 'Can delete variable', 23, 'delete_variable');
INSERT INTO `auth_permission` VALUES (92, 'Can view variable', 23, 'view_variable');
INSERT INTO `auth_permission` VALUES (93, 'Can add virtual file', 24, 'add_virtualfile');
INSERT INTO `auth_permission` VALUES (94, 'Can change virtual file', 24, 'change_virtualfile');
INSERT INTO `auth_permission` VALUES (95, 'Can delete virtual file', 24, 'delete_virtualfile');
INSERT INTO `auth_permission` VALUES (96, 'Can view virtual file', 24, 'view_virtualfile');
INSERT INTO `auth_permission` VALUES (97, 'Can add builder', 25, 'add_builder');
INSERT INTO `auth_permission` VALUES (98, 'Can change builder', 25, 'change_builder');
INSERT INTO `auth_permission` VALUES (99, 'Can delete builder', 25, 'delete_builder');
INSERT INTO `auth_permission` VALUES (100, 'Can view builder', 25, 'view_builder');
INSERT INTO `auth_permission` VALUES (101, 'Can add build plan', 26, 'add_buildplan');
INSERT INTO `auth_permission` VALUES (102, 'Can change build plan', 26, 'change_buildplan');
INSERT INTO `auth_permission` VALUES (103, 'Can delete build plan', 26, 'delete_buildplan');
INSERT INTO `auth_permission` VALUES (104, 'Can view build plan', 26, 'view_buildplan');
INSERT INTO `auth_permission` VALUES (105, 'Can add build history', 27, 'add_buildhistory');
INSERT INTO `auth_permission` VALUES (106, 'Can change build history', 27, 'change_buildhistory');
INSERT INTO `auth_permission` VALUES (107, 'Can delete build history', 27, 'delete_buildhistory');
INSERT INTO `auth_permission` VALUES (108, 'Can view build history', 27, 'view_buildhistory');
INSERT INTO `auth_permission` VALUES (109, 'Can add history detail', 28, 'add_historydetail');
INSERT INTO `auth_permission` VALUES (110, 'Can change history detail', 28, 'change_historydetail');
INSERT INTO `auth_permission` VALUES (111, 'Can delete history detail', 28, 'delete_historydetail');
INSERT INTO `auth_permission` VALUES (112, 'Can view history detail', 28, 'view_historydetail');
INSERT INTO `auth_permission` VALUES (113, 'Can add environment', 29, 'add_environment');
INSERT INTO `auth_permission` VALUES (114, 'Can change environment', 29, 'change_environment');
INSERT INTO `auth_permission` VALUES (115, 'Can delete environment', 29, 'delete_environment');
INSERT INTO `auth_permission` VALUES (116, 'Can view environment', 29, 'view_environment');
INSERT INTO `auth_permission` VALUES (117, 'Can add case priority', 30, 'add_casepriority');
INSERT INTO `auth_permission` VALUES (118, 'Can change case priority', 30, 'change_casepriority');
INSERT INTO `auth_permission` VALUES (119, 'Can delete case priority', 30, 'delete_casepriority');
INSERT INTO `auth_permission` VALUES (120, 'Can view case priority', 30, 'view_casepriority');
INSERT INTO `auth_permission` VALUES (121, 'Can add python lib', 31, 'add_pythonlib');
INSERT INTO `auth_permission` VALUES (122, 'Can change python lib', 31, 'change_pythonlib');
INSERT INTO `auth_permission` VALUES (123, 'Can delete python lib', 31, 'delete_pythonlib');
INSERT INTO `auth_permission` VALUES (124, 'Can view python lib', 31, 'view_pythonlib');
INSERT INTO `auth_permission` VALUES (125, 'Can add project version', 32, 'add_projectversion');
INSERT INTO `auth_permission` VALUES (126, 'Can change project version', 32, 'change_projectversion');
INSERT INTO `auth_permission` VALUES (127, 'Can delete project version', 32, 'delete_projectversion');
INSERT INTO `auth_permission` VALUES (128, 'Can view project version', 32, 'view_projectversion');
INSERT INTO `auth_permission` VALUES (129, 'Can add region', 33, 'add_region');
INSERT INTO `auth_permission` VALUES (130, 'Can change region', 33, 'change_region');
INSERT INTO `auth_permission` VALUES (131, 'Can delete region', 33, 'delete_region');
INSERT INTO `auth_permission` VALUES (132, 'Can view region', 33, 'view_region');
INSERT INTO `auth_permission` VALUES (133, 'Can add build record', 34, 'add_buildrecord');
INSERT INTO `auth_permission` VALUES (134, 'Can change build record', 34, 'change_buildrecord');
INSERT INTO `auth_permission` VALUES (135, 'Can delete build record', 34, 'delete_buildrecord');
INSERT INTO `auth_permission` VALUES (136, 'Can view build record', 34, 'view_buildrecord');
INSERT INTO `auth_permission` VALUES (137, 'Can add notice', 35, 'add_notice');
INSERT INTO `auth_permission` VALUES (138, 'Can change notice', 35, 'change_notice');
INSERT INTO `auth_permission` VALUES (139, 'Can delete notice', 35, 'delete_notice');
INSERT INTO `auth_permission` VALUES (140, 'Can view notice', 35, 'view_notice');
INSERT INTO `auth_permission` VALUES (141, 'Can add department', 36, 'add_department');
INSERT INTO `auth_permission` VALUES (142, 'Can change department', 36, 'change_department');
INSERT INTO `auth_permission` VALUES (143, 'Can delete department', 36, 'delete_department');
INSERT INTO `auth_permission` VALUES (144, 'Can view department', 36, 'view_department');
INSERT INTO `auth_permission` VALUES (145, 'Can add product', 37, 'add_product');
INSERT INTO `auth_permission` VALUES (146, 'Can change product', 37, 'change_product');
INSERT INTO `auth_permission` VALUES (147, 'Can delete product', 37, 'delete_product');
INSERT INTO `auth_permission` VALUES (148, 'Can view product', 37, 'view_product');
INSERT INTO `auth_permission` VALUES (149, 'Can add user group', 38, 'add_usergroup');
INSERT INTO `auth_permission` VALUES (150, 'Can change user group', 38, 'change_usergroup');
INSERT INTO `auth_permission` VALUES (151, 'Can delete user group', 38, 'delete_usergroup');
INSERT INTO `auth_permission` VALUES (152, 'Can view user group', 38, 'view_usergroup');
INSERT INTO `auth_permission` VALUES (153, 'Can add project permission', 39, 'add_projectpermission');
INSERT INTO `auth_permission` VALUES (154, 'Can change project permission', 39, 'change_projectpermission');
INSERT INTO `auth_permission` VALUES (155, 'Can delete project permission', 39, 'delete_projectpermission');
INSERT INTO `auth_permission` VALUES (156, 'Can view project permission', 39, 'view_projectpermission');
INSERT INTO `auth_permission` VALUES (157, 'Can add system ext', 40, 'add_systemext');
INSERT INTO `auth_permission` VALUES (158, 'Can change system ext', 40, 'change_systemext');
INSERT INTO `auth_permission` VALUES (159, 'Can delete system ext', 40, 'delete_systemext');
INSERT INTO `auth_permission` VALUES (160, 'Can view system ext', 40, 'view_systemext');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$260000$E08IL4QHoVj0O8wevCYntf$apfiWgyXyV+em3wdzEgjfmScFQq3i5GRKo95MzsKdDo=', '2023-10-29 15:07:09.499110', 1, 'Delav', '', '', 'delavpeng@163.com', 1, 1, '2022-07-06 23:04:45.230926');
INSERT INTO `auth_user` VALUES (6, 'pbkdf2_sha256$260000$m4wMTY4EN1gp4w7aKHmuyu$rinPImw3S9CVUAy7H7EIopTpp7K7RKxcvj3it0mw3Qs=', '2023-10-28 18:59:50.840191', 0, 'Test', '', '', '123456@163.com', 0, 1, '2022-08-26 17:06:01.379613');
INSERT INTO `auth_user` VALUES (7, 'pbkdf2_sha256$260000$xvojjZ85hJPaQJhLwkRrve$z4Vbx/+l+3tlNJiC1p5OMNoek09BcOnxF0O1hbEq3u8=', NULL, 0, 'Test01', '', '', '456123@163.com', 0, 1, '2022-08-26 17:07:42.165178');
INSERT INTO `auth_user` VALUES (8, 'pbkdf2_sha256$260000$qKcEPwe52Mbt63iXiTgbV0$gPAc0XEGSs4u1h4oL2mLTfcdWq28yRWZcan5gGv1C0E=', NULL, 0, 'Test02', '', '', '456789@163.com', 0, 1, '2022-08-26 17:07:58.922635');
INSERT INTO `auth_user` VALUES (9, 'pbkdf2_sha256$260000$cyEXv6MaJnXvmamK4cifoy$Qag40aXlrXpmdKugqMQ8GiJ38EVnFX1whR5lSk726oA=', NULL, 0, 'Test03', '', '', '123789@163.com', 0, 1, '2022-08-26 17:08:15.608047');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------
INSERT INTO `auth_user_groups` VALUES (3, 6, 1);
INSERT INTO `auth_user_groups` VALUES (4, 7, 1);
INSERT INTO `auth_user_groups` VALUES (5, 8, 1);
INSERT INTO `auth_user_groups` VALUES (6, 9, 1);

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for build_history
-- ----------------------------
DROP TABLE IF EXISTS `build_history`;
CREATE TABLE `build_history`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `total_case` int NOT NULL,
  `failed_case` int NOT NULL,
  `passed_case` int NOT NULL,
  `skipped_case` int NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `start_time` datetime(6) NULL DEFAULT NULL,
  `end_time` datetime(6) NULL DEFAULT NULL,
  `status` int NOT NULL,
  `batch` int NOT NULL,
  `celery_task` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `report_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `env_id` int NOT NULL,
  `region_id` int NULL DEFAULT NULL,
  `record_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of build_history
-- ----------------------------
INSERT INTO `build_history` VALUES (4, 2, 0, 0, 0, '2023-04-27 20:51:43.073253', '2023-04-27 20:51:43.224924', '2023-04-27 20:51:43.329623', 0, 1, 'a516fa24-153d-4f32-b462-664ee6dc7973', 'C:\\Users\\Delav\\Desktop\\skylark\\report\\2023\\4\\27\\4', 2, 2, 15);
INSERT INTO `build_history` VALUES (5, 2, 0, 0, 0, '2023-05-20 15:01:06.562347', '2023-05-20 15:01:06.774921', '2023-05-20 15:01:06.839062', 0, 1, '6af65ad4-6bd5-4cf1-8801-49754bfa85bc', 'C:\\Users\\Delav\\Desktop\\skylark\\report\\2023\\5\\20\\5', 2, 2, 16);
INSERT INTO `build_history` VALUES (6, 2, 0, 0, 0, '2023-05-20 15:06:25.517000', '2023-05-20 15:06:25.545951', '2023-05-20 15:06:25.609158', 0, 1, '1f3ba446-ea17-489c-8563-c8f4d5b0f857', 'C:\\Users\\Delav\\Desktop\\skylark\\report\\2023\\5\\20\\6', 2, 2, 17);
INSERT INTO `build_history` VALUES (7, 2, 0, 0, 0, '2023-05-20 15:09:58.900309', '2023-05-20 15:09:58.928837', '2023-05-20 15:09:58.972718', 0, 1, 'e1db4689-102a-42cb-bbcc-8e591c92e522', 'C:\\Users\\Delav\\Desktop\\skylark\\report\\2023\\5\\20\\7', 2, 2, 18);
INSERT INTO `build_history` VALUES (8, 2, 0, 0, 0, '2023-05-20 15:18:46.500540', '2023-05-20 15:18:46.540416', '2023-05-20 15:18:46.610231', 0, 1, '46b9521c-753b-4375-a4bb-fc29abedb705', 'C:\\Users\\Delav\\Desktop\\skylark\\report\\2023\\5\\20\\8', 2, 2, 19);
INSERT INTO `build_history` VALUES (9, 2, 0, 0, 0, '2023-05-20 15:19:26.665046', '2023-05-20 15:19:26.711506', '2023-05-20 15:19:26.752009', 0, 1, '19a9301a-1291-447a-93fe-9de59dc795c8', 'C:\\Users\\Delav\\Desktop\\skylark\\report\\2023\\5\\20\\9', 2, 2, 20);
INSERT INTO `build_history` VALUES (18, 2, 0, 0, 0, '2023-09-03 13:44:57.689747', '2023-09-03 13:44:57.844887', '2023-09-03 13:44:57.923985', 0, 1, '7026ae1a-c746-4c9f-8fad-391861fb5180', 'C:\\Users\\Delav\\Desktop\\skylark\\report\\SKYLARK\\2023\\9\\3\\18', 4, 2, 47);
INSERT INTO `build_history` VALUES (19, 3, 0, 0, 0, '2023-10-05 18:00:41.583102', NULL, NULL, -1, 1, 'ff11a74c-4a14-45df-bd19-0e89798f0303', '', 3, 2, 54);
INSERT INTO `build_history` VALUES (20, 3, 0, 3, 0, '2023-10-05 18:34:56.168626', '2023-10-05 18:34:56.350141', '2023-10-05 18:34:56.471468', 1, 1, '4345d046-5342-4bfe-af9d-df9173a81128', 'C:/Users/Delav/Desktop/skylark/report/SKYLARK/2023/10/05/20', 2, 2, 55);
INSERT INTO `build_history` VALUES (21, 3, 0, 3, 0, '2023-10-08 14:26:08.140447', '2023-10-08 14:26:10.466831', '2023-10-08 14:26:11.188195', 1, 1, '81a94fd5-57fc-4ea3-859f-899118f9dbbd', 'C:/Users/Delav/Desktop/skylark/report/SKYLARK/2023/10/08/21', 2, 2, 56);
INSERT INTO `build_history` VALUES (22, 4, 0, 4, 0, '2023-10-29 19:18:36.279622', '2023-10-29 19:18:36.611576', '2023-10-29 19:18:36.742227', 2, 1, '9d9dc705-54a6-45cb-8447-efba6587ba12', 'C:/Users/Delav/Desktop/skylark/report/SKYLARK/2023/10/29/22', 2, 1, 57);
INSERT INTO `build_history` VALUES (23, 0, 0, 0, 0, '2023-10-29 19:18:36.476750', NULL, NULL, 0, 1, '280efe2e-1a87-476e-8337-d6fa5df5c631', '', 2, 2, 57);
INSERT INTO `build_history` VALUES (24, 4, 0, 4, 0, '2023-10-29 22:01:26.716050', '2023-10-29 22:01:28.577860', '2023-10-29 22:01:28.931748', 2, 1, 'd773d5e8-fdf2-4bd6-90e0-2d9c98ca1b7b', 'C:/Users/Delav/Desktop/skylark/report/SKYLARK/2023/10/29/24', 2, 1, 58);
INSERT INTO `build_history` VALUES (25, 4, 0, 4, 0, '2023-10-29 22:02:55.185421', '2023-10-29 22:02:55.222324', '2023-10-29 22:02:55.500613', 2, 1, '837d6f60-2d9c-4c36-bab8-76a2c6c2b33a', 'C:/Users/Delav/Desktop/skylark/report/SKYLARK/2023/10/29/25', 2, 1, 59);
INSERT INTO `build_history` VALUES (26, 0, 0, 0, 0, '2023-10-29 22:02:55.217369', NULL, NULL, 0, 1, 'f5940c7a-6002-443e-ae20-ec6c3b7d9a6d', '', 2, 2, 59);
INSERT INTO `build_history` VALUES (27, 4, 0, 4, 0, '2023-10-29 22:43:32.987371', '2023-10-29 22:43:33.216740', '2023-10-29 22:43:33.496247', 2, 1, 'd4c35f60-099a-4a07-a1d2-c7cf8149625a', 'C:/Users/Delav/Desktop/skylark/report/SKYLARK/2023/10/29/27', 1, 1, 62);
INSERT INTO `build_history` VALUES (28, 4, 0, 4, 0, '2023-10-29 22:43:33.026250', '2023-10-29 22:43:33.217738', '2023-10-29 22:43:33.496247', 2, 1, 'b07b421f-25e3-4689-987a-173296418068', 'C:/Users/Delav/Desktop/skylark/report/SKYLARK/2023/10/29/28', 1, 2, 62);

-- ----------------------------
-- Table structure for build_plan
-- ----------------------------
DROP TABLE IF EXISTS `build_plan`;
CREATE TABLE `build_plan`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `total_case` int NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `build_cases` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `periodic_expr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `periodic_task_id` int NULL DEFAULT NULL,
  `periodic_switch` tinyint(1) NOT NULL,
  `envs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `project_id` int NOT NULL,
  `branch` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expect_pass` double NOT NULL,
  `regions` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `notice_open` tinyint(1) NOT NULL,
  `status` int NOT NULL,
  `auto_latest` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 38 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of build_plan
-- ----------------------------
INSERT INTO `build_plan` VALUES (8, '测试计划001', 4, '2023-04-15 10:02:11.722770', '2023-04-15 10:02:11.722770', '123456@163.com', '123456@163.com', '1,2,3,4', '', NULL, 0, '2', 1, 'v1.0.0', 90, '2', 0, 0, 0);
INSERT INTO `build_plan` VALUES (9, '定时计划001', 4, '2023-04-15 18:19:02.575542', '2023-04-15 18:19:02.656399', '123456@163.com', '123456@163.com', '1,2,3,4', '0 10 * * *', 3, 1, '1,2', 1, 'v1.1.0', 90, '2', 0, 0, 0);
INSERT INTO `build_plan` VALUES (10, '测试计划002', 3, '2023-04-15 18:21:25.195850', '2023-04-15 18:21:25.195850', '123456@163.com', '123456@163.com', '1,3,4', '', NULL, 0, '3', 1, 'v1.0.0', 90, '1', 0, 0, 0);
INSERT INTO `build_plan` VALUES (11, '定时计划002', 4, '2023-04-15 18:22:28.606938', '2023-04-15 18:22:28.645835', '123456@163.com', '123456@163.com', '1,2,3,4', '0 18 1 * *', 4, 1, '4', 1, 'v1.1.0', 90, '1,2', 0, 0, 0);
INSERT INTO `build_plan` VALUES (32, '回归测试2.0', 2, '2023-09-03 10:38:52.659339', '2023-09-03 10:38:52.661060', '123456@163.com', '123456@163.com', '1,2', NULL, NULL, 0, '2', 1, 'v2.0.0', 100, '2', 0, 0, 0);
INSERT INTO `build_plan` VALUES (34, 'Regression-7.0.1', 3, '2023-10-06 20:20:55.021292', '2023-10-06 20:20:55.021292', '123456@163.com', '123456@163.com', '2,23,1', NULL, NULL, 0, '2,3', 1, 'v2.0.0', 100, '2', 0, 0, 0);
INSERT INTO `build_plan` VALUES (36, 'Regression-8.0.1', 3, '2023-10-06 20:39:00.941052', '2023-10-06 20:39:00.979945', '123456@163.com', '123456@163.com', '2,23,1', '0 20 * * *', 5, 1, '2', 1, 'v1.1.0', 100, '2', 0, 0, 0);
INSERT INTO `build_plan` VALUES (37, '新-测试计划001', 3, '2023-10-28 14:29:25.586638', '2023-10-28 14:29:25.586638', '123456@163.com', '123456@163.com', '2,23,1', NULL, NULL, 0, '2', 1, 'v2.0.0', 96, '2,1', 0, 0, 1);

-- ----------------------------
-- Table structure for build_record
-- ----------------------------
DROP TABLE IF EXISTS `build_record`;
CREATE TABLE `build_record`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `create_at` datetime(6) NOT NULL,
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `plan_id` int NULL DEFAULT NULL,
  `project_id` int NOT NULL,
  `envs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `regions` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `periodic` tinyint(1) NOT NULL,
  `status` int NOT NULL,
  `branch` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `desc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `finish_at` datetime(6) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 63 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of build_record
-- ----------------------------
INSERT INTO `build_record` VALUES (1, '2023-04-20 23:35:46.025853', '123456@163.com', 30, 1, '2', '1', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (2, '2023-04-20 23:40:34.544576', '123456@163.com', 30, 1, '2', '1', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (3, '2023-04-20 23:42:41.835194', '123456@163.com', 30, 1, '2', '1', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (4, '2023-04-20 23:53:40.737471', '123456@163.com', 30, 1, '2', '1', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (5, '2023-04-22 10:47:15.776781', '123456@163.com', 30, 1, '2', '1', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (6, '2023-04-22 10:49:52.319915', '123456@163.com', 30, 1, '2', '1', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (7, '2023-04-22 10:54:19.637327', '123456@163.com', 30, 1, '2', '1', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (8, '2023-04-22 10:59:38.506394', '123456@163.com', 30, 1, '2', '1,2', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (9, '2023-04-22 11:05:55.537747', '123456@163.com', 30, 1, '2', '1,2', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (10, '2023-04-25 21:47:03.990906', '123456@163.com', 30, 1, '2', '1', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (11, '2023-04-25 21:52:19.090734', '123456@163.com', 30, 1, '2', '1', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (12, '2023-04-25 22:05:00.420683', '123456@163.com', 30, 1, '2', '1', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (13, '2023-04-25 22:11:01.106463', '123456@163.com', 30, 1, '2', '1', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (14, '2023-04-27 20:38:26.904593', '123456@163.com', 30, 1, '2', '1', 0, 1, 'v1.1.0', '测试23の243', NULL);
INSERT INTO `build_record` VALUES (15, '2023-04-27 20:51:41.530291', '123456@163.com', 31, 1, '2', '2', 0, 1, 'v1.0.0', 'new测试001', NULL);
INSERT INTO `build_record` VALUES (16, '2023-05-20 15:01:05.475935', '123456@163.com', 31, 1, '2', '2', 0, 1, 'v1.0.0', 'new测试001', NULL);
INSERT INTO `build_record` VALUES (17, '2023-05-20 15:06:25.022635', '123456@163.com', 31, 1, '2', '2', 0, 1, 'v1.0.0', 'new测试001', NULL);
INSERT INTO `build_record` VALUES (18, '2023-05-20 15:09:58.334622', '123456@163.com', 31, 1, '2', '2', 0, 1, 'v1.0.0', 'new测试001', NULL);
INSERT INTO `build_record` VALUES (19, '2023-05-20 15:18:45.393845', '123456@163.com', 31, 1, '2', '2', 0, 1, 'v1.0.0', 'new测试001', NULL);
INSERT INTO `build_record` VALUES (20, '2023-05-20 15:19:26.565764', '123456@163.com', 31, 1, '2', '2', 0, 1, 'v1.0.0', 'new测试001', NULL);
INSERT INTO `build_record` VALUES (21, '2023-09-02 08:15:53.895024', '123456@163.com', 8, 1, '2', '2', 0, 1, 'v1.0.0', '测试计划001', NULL);
INSERT INTO `build_record` VALUES (22, '2023-09-02 08:20:13.931495', '123456@163.com', 8, 1, '2', '2', 0, 1, 'v1.0.0', '测试计划001', NULL);
INSERT INTO `build_record` VALUES (23, '2023-09-03 10:50:57.935278', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (24, '2023-09-03 11:08:21.564235', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (25, '2023-09-03 11:20:40.193217', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (26, '2023-09-03 11:21:10.650704', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (27, '2023-09-03 11:25:34.029381', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (28, '2023-09-03 11:33:15.721892', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (29, '2023-09-03 11:37:37.588412', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (30, '2023-09-03 11:41:14.113466', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (31, '2023-09-03 12:01:56.800229', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (32, '2023-09-03 12:03:12.617813', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (33, '2023-09-03 12:07:26.403631', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (34, '2023-09-03 12:09:14.194989', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (35, '2023-09-03 12:25:05.854070', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (36, '2023-09-03 12:28:08.668105', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (37, '2023-09-03 12:35:54.884871', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (38, '2023-09-03 12:50:00.577719', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (39, '2023-09-03 12:55:57.277327', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (40, '2023-09-03 13:02:44.095629', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (41, '2023-09-03 13:16:35.257296', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (42, '2023-09-03 13:24:31.760764', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (43, '2023-09-03 13:29:54.347494', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (44, '2023-09-03 13:36:36.065734', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (45, '2023-09-03 13:39:08.138431', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (46, '2023-09-03 13:43:10.630427', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (47, '2023-09-03 13:44:56.440403', '123456@163.com', 33, 1, '4', '2', 0, 1, 'v2.0.0', '回归测试3.0', NULL);
INSERT INTO `build_record` VALUES (48, '2023-09-16 14:30:01.989351', '123456@163.com', 11, 1, '4', '1', 0, 1, 'v1.1.0', '定时计划002', NULL);
INSERT INTO `build_record` VALUES (49, '2023-09-16 14:40:35.118345', '123456@163.com', 11, 1, '4', '1', 0, 1, 'v1.1.0', '定时计划002', NULL);
INSERT INTO `build_record` VALUES (50, '2023-09-16 14:45:45.425082', '123456@163.com', 11, 1, '4', '1', 0, 1, 'v1.1.0', '定时计划002', NULL);
INSERT INTO `build_record` VALUES (51, '2023-09-16 14:59:33.042571', '123456@163.com', 11, 1, '4', '1', 0, 1, 'v1.1.0', '定时计划002', NULL);
INSERT INTO `build_record` VALUES (52, '2023-10-05 15:32:32.922250', '123456@163.com', NULL, 1, '2', '2', 0, 1, 'v2.0.0', 'QuickBuild-@SKYLARK', NULL);
INSERT INTO `build_record` VALUES (53, '2023-10-05 17:42:40.621845', '123456@163.com', NULL, 1, '2', '2', 0, 1, 'v2.0.0', 'QuickBuild-@SKYLARK', NULL);
INSERT INTO `build_record` VALUES (54, '2023-10-05 18:00:41.433030', '123456@163.com', NULL, 1, '3', '2', 0, 1, 'v2.0.0', 'QuickBuild-@SKYLARK', NULL);
INSERT INTO `build_record` VALUES (55, '2023-10-05 18:34:56.106153', '123456@163.com', NULL, 1, '2', '2', 0, 1, 'v2.0.0', 'QuickBuild-@SKYLARK', '2023-10-05 18:34:57.646322');
INSERT INTO `build_record` VALUES (56, '2023-10-08 14:26:07.252548', '123456@163.com', 36, 1, '2', '2', 0, 1, 'v1.1.0', 'Regression-8.0.1', '2023-10-08 14:26:11.925855');
INSERT INTO `build_record` VALUES (62, '2023-10-29 22:43:31.435929', '123456@163.com', 37, 1, '1', '1,2', 0, 1, 'v2.0.0', '新-测试计划001', '2023-10-29 22:43:33.607163');

-- ----------------------------
-- Table structure for builder
-- ----------------------------
DROP TABLE IF EXISTS `builder`;
CREATE TABLE `builder`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `create_at` datetime(6) NOT NULL,
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of builder
-- ----------------------------

-- ----------------------------
-- Table structure for case_entity
-- ----------------------------
DROP TABLE IF EXISTS `case_entity`;
CREATE TABLE `case_entity`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `input_args` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `output_args` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `keyword_id` int NOT NULL,
  `keyword_type` int NOT NULL,
  `test_case_id` bigint NOT NULL,
  `order` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `case_entity_test_case_id_order_df6f2779_uniq`(`test_case_id` ASC, `order` ASC) USING BTREE,
  INDEX `case_entity_test_case_id_82d7fc7e`(`test_case_id` ASC) USING BTREE,
  CONSTRAINT `case_entity_test_case_id_82d7fc7e_fk_test_case_id` FOREIGN KEY (`test_case_id`) REFERENCES `test_case` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 194 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of case_entity
-- ----------------------------
INSERT INTO `case_entity` VALUES (4, '1#@#2', '${out}', 6, 1, 3, 0);
INSERT INTO `case_entity` VALUES (5, '1#@#2', '', 5, 1, 4, 0);
INSERT INTO `case_entity` VALUES (40, '127.0.0.1', '${host}', 4, 1, 17, 0);
INSERT INTO `case_entity` VALUES (41, '${host}', '', 2, 1, 17, 1);
INSERT INTO `case_entity` VALUES (42, '', '${outputComputerFiles}', 4, 1, 17, 2);
INSERT INTO `case_entity` VALUES (43, '456#@#123#@#789', '${out}', 6, 1, 17, 3);
INSERT INTO `case_entity` VALUES (44, '127.0.0.1', '${host}', 4, 1, 19, 0);
INSERT INTO `case_entity` VALUES (45, '${host}', '', 2, 1, 19, 1);
INSERT INTO `case_entity` VALUES (46, '', '${outputComputerFiles}', 4, 1, 19, 2);
INSERT INTO `case_entity` VALUES (47, '456#@#123#@#789', '${out}', 6, 1, 19, 3);
INSERT INTO `case_entity` VALUES (48, '127.0.0.1', '${host}', 4, 1, 20, 0);
INSERT INTO `case_entity` VALUES (49, '${host}', '', 2, 1, 20, 1);
INSERT INTO `case_entity` VALUES (50, '', '${outputComputerFiles}', 4, 1, 20, 2);
INSERT INTO `case_entity` VALUES (51, '456#@#123#@#789', '${out}', 6, 1, 20, 3);
INSERT INTO `case_entity` VALUES (82, '${host}', '', 2, 1, 21, 0);
INSERT INTO `case_entity` VALUES (83, '127.0.0.1', '${host}', 4, 1, 21, 1);
INSERT INTO `case_entity` VALUES (84, '123#@#456#@#789', '${out}', 6, 1, 21, 2);
INSERT INTO `case_entity` VALUES (85, '', '${outputComputerFiles}', 4, 1, 21, 3);
INSERT INTO `case_entity` VALUES (86, '1#@#1', '', 5, 1, 22, 0);
INSERT INTO `case_entity` VALUES (87, 'host|port', '', 8, 1, 22, 1);
INSERT INTO `case_entity` VALUES (94, 'env=${ENV}#@#region=${REGION}', '', 9, 1, 14, 0);
INSERT INTO `case_entity` VALUES (95, '添加银行卡', '${caseName}', 4, 1, 15, 0);
INSERT INTO `case_entity` VALUES (96, '设置默认银行卡', '', 2, 1, 16, 0);
INSERT INTO `case_entity` VALUES (97, 'test#@#123456', '${token}', 101, 1, 7, 0);
INSERT INTO `case_entity` VALUES (102, '测试套件前置步骤', '', 2, 1, 6, 0);
INSERT INTO `case_entity` VALUES (103, '', '', 1, 2, 13, 0);
INSERT INTO `case_entity` VALUES (104, '1#@#1', '', 5, 1, 13, 1);
INSERT INTO `case_entity` VALUES (145, 'a=1#@#b=2', '', 9, 1, 12, 0);
INSERT INTO `case_entity` VALUES (146, '${cur_env}', '', 2, 1, 1, 0);
INSERT INTO `case_entity` VALUES (147, '789#@#456#@#123', '${out}', 6, 1, 1, 1);
INSERT INTO `case_entity` VALUES (148, '${index}#@#IN#@#1#@#2#@#3', '', 102, 1, 1, 2);
INSERT INTO `case_entity` VALUES (149, '${index}', '', 2, 1, 1, 3);
INSERT INTO `case_entity` VALUES (150, '', '', 103, 1, 1, 4);
INSERT INTO `case_entity` VALUES (151, '{\"key\":10001, \"value\":\"dict\"}', '${request}', 4, 1, 1, 5);
INSERT INTO `case_entity` VALUES (167, '${10013801}', '${channel}', 4, 1, 2, 0);
INSERT INTO `case_entity` VALUES (168, '${CURDIR}', '', 2, 1, 2, 1);
INSERT INTO `case_entity` VALUES (169, '${TEMPDIR}', '', 2, 1, 2, 2);
INSERT INTO `case_entity` VALUES (170, '${EXECDIR}', '', 2, 1, 2, 3);
INSERT INTO `case_entity` VALUES (171, '${FILEDIR}', '', 2, 1, 2, 4);
INSERT INTO `case_entity` VALUES (182, '${ENV}', '', 2, 1, 23, 0);
INSERT INTO `case_entity` VALUES (183, '${ACCOUNT}', '', 2, 1, 23, 1);
INSERT INTO `case_entity` VALUES (184, '${ACCOUNT[\'username\']}', '', 2, 1, 23, 2);
INSERT INTO `case_entity` VALUES (190, 'a=1#@#b=2', '', 9, 1, 25, 0);
INSERT INTO `case_entity` VALUES (191, '${REGION}', '', 2, 1, 25, 1);
INSERT INTO `case_entity` VALUES (192, 'https://baidu.com#@#{}#@#{}', '${response}', 117, 1, 25, 2);
INSERT INTO `case_entity` VALUES (193, '1#@#1', '', 5, 1, 25, 3);

-- ----------------------------
-- Table structure for case_priority
-- ----------------------------
DROP TABLE IF EXISTS `case_priority`;
CREATE TABLE `case_priority`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of case_priority
-- ----------------------------
INSERT INTO `case_priority` VALUES (1, 'P0');
INSERT INTO `case_priority` VALUES (2, 'P1');
INSERT INTO `case_priority` VALUES (3, 'P2');
INSERT INTO `case_priority` VALUES (4, 'P3');
INSERT INTO `case_priority` VALUES (5, 'P4');

-- ----------------------------
-- Table structure for department
-- ----------------------------
DROP TABLE IF EXISTS `department`;
CREATE TABLE `department`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of department
-- ----------------------------
INSERT INTO `department` VALUES (1, 'ShopeePay');
INSERT INTO `department` VALUES (2, 'MarketPlace');

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_celery_beat_clockedschedule
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_clockedschedule`;
CREATE TABLE `django_celery_beat_clockedschedule`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `clocked_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_celery_beat_clockedschedule
-- ----------------------------

-- ----------------------------
-- Table structure for django_celery_beat_crontabschedule
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_crontabschedule`;
CREATE TABLE `django_celery_beat_crontabschedule`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `minute` varchar(240) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `hour` varchar(96) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `day_of_week` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `day_of_month` varchar(124) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `month_of_year` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `timezone` varchar(63) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_celery_beat_crontabschedule
-- ----------------------------
INSERT INTO `django_celery_beat_crontabschedule` VALUES (3, '0', '12', '*', '*', '*', 'UTC');
INSERT INTO `django_celery_beat_crontabschedule` VALUES (4, '0', '10', '*', '*', '*', 'UTC');
INSERT INTO `django_celery_beat_crontabschedule` VALUES (5, '0', '18', '1', '*', '*', 'UTC');
INSERT INTO `django_celery_beat_crontabschedule` VALUES (6, '0', '20', '*', '*', '*', 'UTC');

-- ----------------------------
-- Table structure for django_celery_beat_intervalschedule
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_intervalschedule`;
CREATE TABLE `django_celery_beat_intervalschedule`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `every` int NOT NULL,
  `period` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_celery_beat_intervalschedule
-- ----------------------------

-- ----------------------------
-- Table structure for django_celery_beat_periodictask
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_periodictask`;
CREATE TABLE `django_celery_beat_periodictask`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `task` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `args` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `kwargs` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `queue` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `exchange` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `routing_key` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `expires` datetime(6) NULL DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) NULL DEFAULT NULL,
  `total_run_count` int UNSIGNED NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `crontab_id` int NULL DEFAULT NULL,
  `interval_id` int NULL DEFAULT NULL,
  `solar_id` int NULL DEFAULT NULL,
  `one_off` tinyint(1) NOT NULL,
  `start_time` datetime(6) NULL DEFAULT NULL,
  `priority` int UNSIGNED NULL DEFAULT NULL,
  `headers` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `clocked_id` int NULL DEFAULT NULL,
  `expire_seconds` int UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE,
  INDEX `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce`(`crontab_id` ASC) USING BTREE,
  INDEX `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce`(`interval_id` ASC) USING BTREE,
  INDEX `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce`(`solar_id` ASC) USING BTREE,
  INDEX `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce`(`clocked_id` ASC) USING BTREE,
  CONSTRAINT `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` FOREIGN KEY (`clocked_id`) REFERENCES `django_celery_beat_clockedschedule` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` FOREIGN KEY (`crontab_id`) REFERENCES `django_celery_beat_crontabschedule` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` FOREIGN KEY (`interval_id`) REFERENCES `django_celery_beat_intervalschedule` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` FOREIGN KEY (`solar_id`) REFERENCES `django_celery_beat_solarschedule` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_celery_beat_periodictask_chk_1` CHECK (`total_run_count` >= 0),
  CONSTRAINT `django_celery_beat_periodictask_chk_2` CHECK (`priority` >= 0),
  CONSTRAINT `django_celery_beat_periodictask_chk_3` CHECK (`expire_seconds` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_celery_beat_periodictask
-- ----------------------------
INSERT INTO `django_celery_beat_periodictask` VALUES (2, 'PLAN-7', 'task.builder.tasks.periodic_builder', '7', '{}', 'builder', NULL, 'periodic.builder', NULL, 1, NULL, 0, '2023-04-08 17:14:31.378761', '', 3, NULL, NULL, 0, NULL, NULL, '{}', NULL, NULL);
INSERT INTO `django_celery_beat_periodictask` VALUES (3, 'PLAN-9', 'task.builder.tasks.periodic_builder', '9', '{}', 'builder', NULL, 'periodic.builder', NULL, 1, NULL, 0, '2023-04-15 18:19:02.653376', '', 4, NULL, NULL, 0, NULL, NULL, '{}', NULL, NULL);
INSERT INTO `django_celery_beat_periodictask` VALUES (4, 'PLAN-11', 'task.builder.tasks.periodic_builder', '11', '{}', 'builder', NULL, 'periodic.builder', NULL, 1, NULL, 0, '2023-04-15 18:22:28.640852', '', 5, NULL, NULL, 0, NULL, NULL, '{}', NULL, NULL);
INSERT INTO `django_celery_beat_periodictask` VALUES (5, 'PLAN-36', 'task.builder.tasks.periodic_builder', '36', '{}', 'builder', NULL, 'periodic.builder', NULL, 1, NULL, 0, '2023-10-06 20:39:00.976952', '', 6, NULL, NULL, 0, NULL, NULL, '{}', NULL, NULL);

-- ----------------------------
-- Table structure for django_celery_beat_periodictasks
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_periodictasks`;
CREATE TABLE `django_celery_beat_periodictasks`  (
  `ident` smallint NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_celery_beat_periodictasks
-- ----------------------------
INSERT INTO `django_celery_beat_periodictasks` VALUES (1, '2023-10-06 20:39:00.977950');

-- ----------------------------
-- Table structure for django_celery_beat_solarschedule
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_solarschedule`;
CREATE TABLE `django_celery_beat_solarschedule`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `event` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `latitude` decimal(9, 6) NOT NULL,
  `longitude` decimal(9, 6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq`(`event` ASC, `latitude` ASC, `longitude` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_celery_beat_solarschedule
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 41 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (25, 'builder', 'builder');
INSERT INTO `django_content_type` VALUES (27, 'buildhistory', 'buildhistory');
INSERT INTO `django_content_type` VALUES (28, 'buildhistory', 'historydetail');
INSERT INTO `django_content_type` VALUES (26, 'buildplan', 'buildplan');
INSERT INTO `django_content_type` VALUES (34, 'buildrecord', 'buildrecord');
INSERT INTO `django_content_type` VALUES (20, 'caseentity', 'caseentity');
INSERT INTO `django_content_type` VALUES (30, 'casepriority', 'casepriority');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (36, 'department', 'department');
INSERT INTO `django_content_type` VALUES (12, 'django_celery_beat', 'clockedschedule');
INSERT INTO `django_content_type` VALUES (7, 'django_celery_beat', 'crontabschedule');
INSERT INTO `django_content_type` VALUES (8, 'django_celery_beat', 'intervalschedule');
INSERT INTO `django_content_type` VALUES (9, 'django_celery_beat', 'periodictask');
INSERT INTO `django_content_type` VALUES (10, 'django_celery_beat', 'periodictasks');
INSERT INTO `django_content_type` VALUES (11, 'django_celery_beat', 'solarschedule');
INSERT INTO `django_content_type` VALUES (29, 'environment', 'environment');
INSERT INTO `django_content_type` VALUES (14, 'keywordgroup', 'keywordgroup');
INSERT INTO `django_content_type` VALUES (15, 'libkeyword', 'libkeyword');
INSERT INTO `django_content_type` VALUES (35, 'notice', 'notice');
INSERT INTO `django_content_type` VALUES (37, 'product', 'product');
INSERT INTO `django_content_type` VALUES (16, 'project', 'project');
INSERT INTO `django_content_type` VALUES (39, 'projectpermission', 'projectpermission');
INSERT INTO `django_content_type` VALUES (32, 'projectversion', 'projectversion');
INSERT INTO `django_content_type` VALUES (31, 'pythonlib', 'pythonlib');
INSERT INTO `django_content_type` VALUES (33, 'region', 'region');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (22, 'setupteardown', 'setupteardown');
INSERT INTO `django_content_type` VALUES (17, 'suitedir', 'suitedir');
INSERT INTO `django_content_type` VALUES (40, 'systemext', 'systemext');
INSERT INTO `django_content_type` VALUES (13, 'tag', 'tag');
INSERT INTO `django_content_type` VALUES (19, 'testcase', 'testcase');
INSERT INTO `django_content_type` VALUES (18, 'testsuite', 'testsuite');
INSERT INTO `django_content_type` VALUES (38, 'usergroup', 'usergroup');
INSERT INTO `django_content_type` VALUES (21, 'userkeyword', 'userkeyword');
INSERT INTO `django_content_type` VALUES (23, 'variable', 'variable');
INSERT INTO `django_content_type` VALUES (24, 'virtualfile', 'virtualfile');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 165 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2023-04-05 18:35:30.473453');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2023-04-05 18:35:30.998023');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2023-04-05 18:35:31.130316');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2023-04-05 18:35:31.139328');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2023-04-05 18:35:31.148269');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2023-04-05 18:35:31.216154');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2023-04-05 18:35:31.264026');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2023-04-05 18:35:31.286967');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2023-04-05 18:35:31.295942');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2023-04-05 18:35:31.354783');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2023-04-05 18:35:31.359772');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2023-04-05 18:35:31.371740');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2023-04-05 18:35:31.430583');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2023-04-05 18:35:31.488428');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2023-04-05 18:35:31.506380');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2023-04-05 18:35:31.517387');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2023-04-05 18:35:31.567218');
INSERT INTO `django_migrations` VALUES (18, 'builder', '0001_initial', '2023-04-05 18:35:31.590066');
INSERT INTO `django_migrations` VALUES (19, 'buildhistory', '0001_initial', '2023-04-05 18:35:31.641928');
INSERT INTO `django_migrations` VALUES (20, 'buildplan', '0001_initial', '2023-04-05 18:35:31.673171');
INSERT INTO `django_migrations` VALUES (21, 'project', '0001_initial', '2023-04-05 18:35:31.704091');
INSERT INTO `django_migrations` VALUES (22, 'suitedir', '0001_initial', '2023-04-05 18:35:31.844941');
INSERT INTO `django_migrations` VALUES (23, 'testsuite', '0001_initial', '2023-04-05 18:35:31.950511');
INSERT INTO `django_migrations` VALUES (24, 'testcase', '0001_initial', '2023-04-05 18:35:32.054828');
INSERT INTO `django_migrations` VALUES (25, 'caseentity', '0001_initial', '2023-04-05 18:35:32.142986');
INSERT INTO `django_migrations` VALUES (26, 'casepriority', '0001_initial', '2023-04-05 18:35:32.167308');
INSERT INTO `django_migrations` VALUES (27, 'django_celery_beat', '0001_initial', '2023-04-05 18:35:32.395114');
INSERT INTO `django_migrations` VALUES (28, 'django_celery_beat', '0002_auto_20161118_0346', '2023-04-05 18:35:32.484019');
INSERT INTO `django_migrations` VALUES (29, 'django_celery_beat', '0003_auto_20161209_0049', '2023-04-05 18:35:32.510034');
INSERT INTO `django_migrations` VALUES (30, 'django_celery_beat', '0004_auto_20170221_0000', '2023-04-05 18:35:32.517312');
INSERT INTO `django_migrations` VALUES (31, 'django_celery_beat', '0005_add_solarschedule_events_choices', '2023-04-05 18:35:32.524310');
INSERT INTO `django_migrations` VALUES (32, 'django_celery_beat', '0006_auto_20180322_0932', '2023-04-05 18:35:32.603629');
INSERT INTO `django_migrations` VALUES (33, 'django_celery_beat', '0007_auto_20180521_0826', '2023-04-05 18:35:32.664908');
INSERT INTO `django_migrations` VALUES (34, 'django_celery_beat', '0008_auto_20180914_1922', '2023-04-05 18:35:32.683053');
INSERT INTO `django_migrations` VALUES (35, 'django_celery_beat', '0006_auto_20180210_1226', '2023-04-05 18:35:32.699167');
INSERT INTO `django_migrations` VALUES (36, 'django_celery_beat', '0006_periodictask_priority', '2023-04-05 18:35:32.768032');
INSERT INTO `django_migrations` VALUES (37, 'django_celery_beat', '0009_periodictask_headers', '2023-04-05 18:35:32.834111');
INSERT INTO `django_migrations` VALUES (38, 'django_celery_beat', '0010_auto_20190429_0326', '2023-04-05 18:35:32.939986');
INSERT INTO `django_migrations` VALUES (39, 'django_celery_beat', '0011_auto_20190508_0153', '2023-04-05 18:35:33.038999');
INSERT INTO `django_migrations` VALUES (40, 'django_celery_beat', '0012_periodictask_expire_seconds', '2023-04-05 18:35:33.115875');
INSERT INTO `django_migrations` VALUES (41, 'django_celery_beat', '0013_auto_20200609_0727', '2023-04-05 18:35:33.127205');
INSERT INTO `django_migrations` VALUES (42, 'django_celery_beat', '0014_remove_clockedschedule_enabled', '2023-04-05 18:35:33.153040');
INSERT INTO `django_migrations` VALUES (43, 'django_celery_beat', '0015_edit_solarschedule_events_choices', '2023-04-05 18:35:33.161005');
INSERT INTO `django_migrations` VALUES (44, 'django_celery_beat', '0016_alter_crontabschedule_timezone', '2023-04-05 18:35:33.168896');
INSERT INTO `django_migrations` VALUES (45, 'environment', '0001_initial', '2023-04-05 18:35:33.193981');
INSERT INTO `django_migrations` VALUES (46, 'keywordgroup', '0001_initial', '2023-04-05 18:35:33.219792');
INSERT INTO `django_migrations` VALUES (47, 'libkeyword', '0001_initial', '2023-04-05 18:35:33.257316');
INSERT INTO `django_migrations` VALUES (48, 'projectversion', '0001_initial', '2023-04-05 18:35:33.289147');
INSERT INTO `django_migrations` VALUES (49, 'pythonlib', '0001_initial', '2023-04-05 18:35:33.314007');
INSERT INTO `django_migrations` VALUES (50, 'sessions', '0001_initial', '2023-04-05 18:35:33.347932');
INSERT INTO `django_migrations` VALUES (51, 'setupteardown', '0001_initial', '2023-04-05 18:35:33.380052');
INSERT INTO `django_migrations` VALUES (52, 'tag', '0001_initial', '2023-04-05 18:35:33.404012');
INSERT INTO `django_migrations` VALUES (53, 'userkeyword', '0001_initial', '2023-04-05 18:35:33.482345');
INSERT INTO `django_migrations` VALUES (54, 'variable', '0001_initial', '2023-04-05 18:35:33.515009');
INSERT INTO `django_migrations` VALUES (55, 'virtualfile', '0001_initial', '2023-04-05 18:35:33.545209');
INSERT INTO `django_migrations` VALUES (56, 'testcase', '0002_alter_testcase_priority_id', '2023-04-05 21:14:50.557919');
INSERT INTO `django_migrations` VALUES (57, 'projectversion', '0002_alter_projectversion_version', '2023-04-05 21:49:24.609361');
INSERT INTO `django_migrations` VALUES (58, 'buildplan', '0002_alter_buildplan_periodic_task_id', '2023-04-08 15:33:11.947403');
INSERT INTO `django_migrations` VALUES (59, 'buildplan', '0003_alter_buildplan_expect_pass', '2023-04-08 23:21:43.012819');
INSERT INTO `django_migrations` VALUES (60, 'region', '0001_initial', '2023-04-08 23:21:43.274048');
INSERT INTO `django_migrations` VALUES (61, 'variable', '0002_variable_region_id', '2023-04-08 23:24:42.441145');
INSERT INTO `django_migrations` VALUES (62, 'variable', '0003_alter_variable_region_id', '2023-04-09 12:42:18.626924');
INSERT INTO `django_migrations` VALUES (63, 'virtualfile', '0002_auto_20230409_1242', '2023-04-09 12:42:18.719561');
INSERT INTO `django_migrations` VALUES (64, 'region', '0002_region_default', '2023-04-09 15:44:52.429558');
INSERT INTO `django_migrations` VALUES (65, 'buildplan', '0004_auto_20230409_1954', '2023-04-09 19:54:55.401022');
INSERT INTO `django_migrations` VALUES (66, 'buildhistory', '0002_auto_20230409_2235', '2023-04-09 22:35:35.962968');
INSERT INTO `django_migrations` VALUES (67, 'buildhistory', '0003_auto_20230416_1156', '2023-04-16 11:56:16.376395');
INSERT INTO `django_migrations` VALUES (68, 'buildrecord', '0001_initial', '2023-04-16 11:56:16.735596');
INSERT INTO `django_migrations` VALUES (69, 'buildrecord', '0002_auto_20230417_2238', '2023-04-17 22:39:16.082612');
INSERT INTO `django_migrations` VALUES (70, 'buildplan', '0005_auto_20230420_2228', '2023-04-20 22:28:14.034824');
INSERT INTO `django_migrations` VALUES (71, 'buildplan', '0006_alter_buildplan_periodic_expr', '2023-04-20 23:25:29.551812');
INSERT INTO `django_migrations` VALUES (72, 'project', '0002_alter_project_status', '2023-04-23 23:10:12.740631');
INSERT INTO `django_migrations` VALUES (73, 'project', '0003_alter_project_status', '2023-04-23 23:10:12.764750');
INSERT INTO `django_migrations` VALUES (74, 'projectversion', '0003_auto_20230423_2308', '2023-04-23 23:10:13.111655');
INSERT INTO `django_migrations` VALUES (75, 'suitedir', '0002_auto_20230423_2308', '2023-04-23 23:10:13.123593');
INSERT INTO `django_migrations` VALUES (76, 'suitedir', '0003_alter_suitedir_status', '2023-04-23 23:10:13.132420');
INSERT INTO `django_migrations` VALUES (77, 'testcase', '0003_auto_20230423_2308', '2023-04-23 23:10:13.147678');
INSERT INTO `django_migrations` VALUES (78, 'testcase', '0004_alter_testcase_status', '2023-04-23 23:10:13.157870');
INSERT INTO `django_migrations` VALUES (79, 'testsuite', '0002_auto_20230423_2308', '2023-04-23 23:10:13.172527');
INSERT INTO `django_migrations` VALUES (80, 'testsuite', '0003_alter_testsuite_status', '2023-04-23 23:10:13.182715');
INSERT INTO `django_migrations` VALUES (81, 'region', '0003_region_status', '2023-04-25 21:43:15.440417');
INSERT INTO `django_migrations` VALUES (82, 'variable', '0004_auto_20230429_1004', '2023-04-29 10:04:34.300101');
INSERT INTO `django_migrations` VALUES (83, 'variable', '0005_alter_variable_env_id', '2023-04-29 12:13:58.918272');
INSERT INTO `django_migrations` VALUES (84, 'virtualfile', '0003_virtualfile_file_path', '2023-05-16 11:29:39.888250');
INSERT INTO `django_migrations` VALUES (85, 'virtualfile', '0004_virtualfile_file_name', '2023-05-17 10:14:04.648431');
INSERT INTO `django_migrations` VALUES (86, 'virtualfile', '0005_virtualfile_save_mode', '2023-05-20 10:52:30.501396');
INSERT INTO `django_migrations` VALUES (87, 'virtualfile', '0006_virtualfile_edit_file', '2023-05-20 10:55:31.641322');
INSERT INTO `django_migrations` VALUES (88, 'buildrecord', '0003_buildrecord_desc', '2023-05-27 19:00:56.929395');
INSERT INTO `django_migrations` VALUES (89, 'environment', '0002_environment_desc', '2023-05-28 23:39:31.258722');
INSERT INTO `django_migrations` VALUES (90, 'region', '0004_auto_20230528_2339', '2023-05-28 23:39:31.318562');
INSERT INTO `django_migrations` VALUES (91, 'keywordgroup', '0002_keywordgroup_group_type', '2023-06-05 22:54:06.847990');
INSERT INTO `django_migrations` VALUES (92, 'caseentity', '0002_alter_caseentity_keyword_type', '2023-06-07 23:38:57.064314');
INSERT INTO `django_migrations` VALUES (93, 'libkeyword', '0002_alter_libkeyword_input_type', '2023-06-07 23:38:57.079393');
INSERT INTO `django_migrations` VALUES (94, 'project', '0004_alter_project_status', '2023-06-07 23:38:57.089127');
INSERT INTO `django_migrations` VALUES (95, 'setupteardown', '0002_alter_setupteardown_module_type', '2023-06-07 23:38:57.096710');
INSERT INTO `django_migrations` VALUES (96, 'suitedir', '0004_auto_20230607_2338', '2023-06-07 23:38:57.110007');
INSERT INTO `django_migrations` VALUES (97, 'tag', '0002_alter_tag_module_type', '2023-06-07 23:38:57.116528');
INSERT INTO `django_migrations` VALUES (98, 'testcase', '0005_auto_20230607_2338', '2023-06-07 23:38:57.131556');
INSERT INTO `django_migrations` VALUES (99, 'testsuite', '0004_auto_20230607_2338', '2023-06-07 23:38:57.144587');
INSERT INTO `django_migrations` VALUES (100, 'variable', '0006_auto_20230607_2338', '2023-06-07 23:38:57.156425');
INSERT INTO `django_migrations` VALUES (101, 'project', '0005_project_personal', '2023-06-08 22:23:08.882094');
INSERT INTO `django_migrations` VALUES (102, 'environment', '0003_auto_20230610_1217', '2023-06-10 12:17:15.662145');
INSERT INTO `django_migrations` VALUES (103, 'region', '0005_remove_region_default', '2023-06-10 12:17:15.696057');
INSERT INTO `django_migrations` VALUES (104, 'userkeyword', '0002_userkeyword_status', '2023-06-12 22:35:53.490852');
INSERT INTO `django_migrations` VALUES (105, 'virtualfile', '0007_virtualfile_status', '2023-06-12 22:35:53.561535');
INSERT INTO `django_migrations` VALUES (106, 'libkeyword', '0003_libkeyword_status', '2023-06-14 23:28:45.279789');
INSERT INTO `django_migrations` VALUES (107, 'virtualfile', '0008_auto_20230617_1724', '2023-06-17 17:25:03.348928');
INSERT INTO `django_migrations` VALUES (108, 'userkeyword', '0003_auto_20230618_1339', '2023-06-18 13:39:42.225586');
INSERT INTO `django_migrations` VALUES (109, 'virtualfile', '0009_virtualfile_update_time', '2023-07-01 11:03:14.392062');
INSERT INTO `django_migrations` VALUES (110, 'libkeyword', '0004_libkeyword_output_type', '2023-07-04 22:31:20.222964');
INSERT INTO `django_migrations` VALUES (111, 'keywordgroup', '0003_keywordgroup_project_id', '2023-07-04 23:30:29.480453');
INSERT INTO `django_migrations` VALUES (112, 'libkeyword', '0005_libkeyword_keyword_type', '2023-07-04 23:30:29.555628');
INSERT INTO `django_migrations` VALUES (113, 'libkeyword', '0006_remove_libkeyword_keyword_type', '2023-07-04 23:42:43.986323');
INSERT INTO `django_migrations` VALUES (114, 'libkeyword', '0007_libkeyword_source', '2023-07-24 22:52:18.754678');
INSERT INTO `django_migrations` VALUES (115, 'buildplan', '0007_buildplan_notice_open', '2023-07-29 17:04:14.790722');
INSERT INTO `django_migrations` VALUES (116, 'libkeyword', '0008_alter_libkeyword_image', '2023-07-29 17:04:14.950597');
INSERT INTO `django_migrations` VALUES (117, 'notice', '0001_initial', '2023-07-29 17:04:14.994233');
INSERT INTO `django_migrations` VALUES (118, 'department', '0001_initial', '2023-08-10 22:58:21.335604');
INSERT INTO `django_migrations` VALUES (119, 'product', '0001_initial', '2023-08-10 22:58:21.389564');
INSERT INTO `django_migrations` VALUES (120, 'project', '0006_project_group_id', '2023-08-10 22:58:21.574629');
INSERT INTO `django_migrations` VALUES (121, 'product', '0002_product_department_id', '2023-08-10 23:01:42.148842');
INSERT INTO `django_migrations` VALUES (122, 'testcase', '0006_testcase_project_id', '2023-08-10 23:11:20.871045');
INSERT INTO `django_migrations` VALUES (123, 'testsuite', '0005_testsuite_project_id', '2023-08-10 23:11:20.929921');
INSERT INTO `django_migrations` VALUES (124, 'usergroup', '0001_initial', '2023-08-15 22:54:14.035240');
INSERT INTO `django_migrations` VALUES (125, 'usergroup', '0002_remove_usergroup_product_id', '2023-08-15 22:59:05.016265');
INSERT INTO `django_migrations` VALUES (126, 'usergroup', '0003_usergroup_product_id', '2023-08-15 22:59:41.543244');
INSERT INTO `django_migrations` VALUES (127, 'usergroup', '0004_delete_usergroup', '2023-08-15 23:02:20.416211');
INSERT INTO `django_migrations` VALUES (128, 'usergroup', '0005_usergroup', '2023-08-16 22:47:09.388912');
INSERT INTO `django_migrations` VALUES (129, 'usergroup', '0006_auto_20230816_2246', '2023-08-16 22:47:09.579401');
INSERT INTO `django_migrations` VALUES (130, 'usergroup', '0007_auto_20230816_2249', '2023-08-16 22:49:55.049575');
INSERT INTO `django_migrations` VALUES (131, 'projectpermission', '0001_initial', '2023-08-18 22:02:01.246548');
INSERT INTO `django_migrations` VALUES (132, 'buildrecord', '0004_buildrecord_finish_at', '2023-09-10 15:30:21.420787');
INSERT INTO `django_migrations` VALUES (133, 'libkeyword', '0009_alter_libkeyword_source', '2023-09-10 15:30:21.434598');
INSERT INTO `django_migrations` VALUES (134, 'buildplan', '0008_buildplan_status', '2023-09-16 09:47:53.905860');
INSERT INTO `django_migrations` VALUES (135, 'buildplan', '0009_remove_buildplan_project_name', '2023-09-16 09:51:51.029711');
INSERT INTO `django_migrations` VALUES (136, 'libkeyword', '0010_libkeyword_category', '2023-09-19 23:52:11.353452');
INSERT INTO `django_migrations` VALUES (137, 'suitedir', '0005_alter_suitedir_options', '2023-09-20 22:11:50.081151');
INSERT INTO `django_migrations` VALUES (138, 'testcase', '0007_auto_20230920_2211', '2023-09-20 22:11:50.378291');
INSERT INTO `django_migrations` VALUES (139, 'testsuite', '0006_alter_testsuite_options', '2023-09-20 22:11:50.387736');
INSERT INTO `django_migrations` VALUES (140, 'caseentity', '0003_caseentity_order', '2023-09-21 23:44:55.888950');
INSERT INTO `django_migrations` VALUES (141, 'caseentity', '0004_auto_20230921_2348', '2023-09-21 23:48:27.657683');
INSERT INTO `django_migrations` VALUES (142, 'buildhistory', '0004_alter_buildhistory_status', '2023-10-06 20:15:59.916308');
INSERT INTO `django_migrations` VALUES (143, 'buildplan', '0010_remove_buildplan_extra_data', '2023-10-06 20:16:00.049166');
INSERT INTO `django_migrations` VALUES (144, 'keywordgroup', '0004_keywordgroup_user_group_id', '2023-10-11 22:32:38.368393');
INSERT INTO `django_migrations` VALUES (145, 'systemext', '0001_initial', '2023-10-11 22:32:38.425309');
INSERT INTO `django_migrations` VALUES (146, 'usergroup', '0008_usergroup_library_path', '2023-10-14 10:21:38.452459');
INSERT INTO `django_migrations` VALUES (147, 'buildhistory', '0005_alter_buildhistory_status', '2023-10-16 20:24:53.261174');
INSERT INTO `django_migrations` VALUES (148, 'buildplan', '0011_alter_buildplan_status', '2023-10-16 20:24:53.287420');
INSERT INTO `django_migrations` VALUES (149, 'buildrecord', '0005_alter_buildrecord_status', '2023-10-16 20:24:53.295385');
INSERT INTO `django_migrations` VALUES (150, 'environment', '0004_alter_environment_status', '2023-10-16 20:24:53.303316');
INSERT INTO `django_migrations` VALUES (151, 'libkeyword', '0011_auto_20231016_2024', '2023-10-16 20:24:53.312146');
INSERT INTO `django_migrations` VALUES (152, 'project', '0007_alter_project_status', '2023-10-16 20:24:53.321149');
INSERT INTO `django_migrations` VALUES (153, 'projectversion', '0004_alter_projectversion_status', '2023-10-16 20:24:53.329116');
INSERT INTO `django_migrations` VALUES (154, 'region', '0006_alter_region_status', '2023-10-16 20:24:53.337342');
INSERT INTO `django_migrations` VALUES (155, 'suitedir', '0006_alter_suitedir_status', '2023-10-16 20:24:53.348755');
INSERT INTO `django_migrations` VALUES (156, 'testcase', '0008_alter_testcase_status', '2023-10-16 20:24:53.358794');
INSERT INTO `django_migrations` VALUES (157, 'testsuite', '0007_alter_testsuite_status', '2023-10-16 20:24:53.368934');
INSERT INTO `django_migrations` VALUES (158, 'userkeyword', '0004_alter_userkeyword_status', '2023-10-16 20:24:53.379689');
INSERT INTO `django_migrations` VALUES (159, 'virtualfile', '0010_alter_virtualfile_status', '2023-10-16 20:24:53.387973');
INSERT INTO `django_migrations` VALUES (160, 'libkeyword', '0012_alter_libkeyword_ext_name', '2023-10-16 23:17:50.585465');
INSERT INTO `django_migrations` VALUES (161, 'buildplan', '0012_buildplan_auto_latest', '2023-10-26 23:31:02.417932');
INSERT INTO `django_migrations` VALUES (162, 'projectversion', '0005_projectversion_total_case', '2023-10-28 12:07:11.554726');
INSERT INTO `django_migrations` VALUES (163, 'keywordgroup', '0005_remove_keywordgroup_image', '2023-10-28 18:57:02.780095');
INSERT INTO `django_migrations` VALUES (164, 'libkeyword', '0013_alter_libkeyword_image', '2023-10-28 18:57:02.800781');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------

-- ----------------------------
-- Table structure for environment
-- ----------------------------
DROP TABLE IF EXISTS `environment`;
CREATE TABLE `environment`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of environment
-- ----------------------------
INSERT INTO `environment` VALUES (1, 'DEV', '开发', 0);
INSERT INTO `environment` VALUES (2, 'TEST', '测试', 0);
INSERT INTO `environment` VALUES (3, 'UAT', '验收', 0);
INSERT INTO `environment` VALUES (4, 'STAGING', '容灾', 0);

-- ----------------------------
-- Table structure for history_detail
-- ----------------------------
DROP TABLE IF EXISTS `history_detail`;
CREATE TABLE `history_detail`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `case_id` int NOT NULL,
  `start_time` datetime(6) NULL DEFAULT NULL,
  `end_time` datetime(6) NULL DEFAULT NULL,
  `result` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `history_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of history_detail
-- ----------------------------
INSERT INTO `history_detail` VALUES (1, 1, '2023-05-20 15:19:26.744457', '2023-05-20 15:19:26.746454', 'PASS', 9);
INSERT INTO `history_detail` VALUES (2, 2, '2023-05-20 15:19:26.746454', '2023-05-20 15:19:26.747409', 'PASS', 9);
INSERT INTO `history_detail` VALUES (3, 2, '2023-09-03 13:44:57.917973', '2023-09-03 13:44:57.919968', 'PASS', 18);
INSERT INTO `history_detail` VALUES (4, 1, '2023-09-03 13:44:57.908999', '2023-09-03 13:44:57.917973', 'PASS', 18);
INSERT INTO `history_detail` VALUES (5, 1, '2023-10-05 18:34:56.453516', '2023-10-05 18:34:56.466489', 'PASS', 20);
INSERT INTO `history_detail` VALUES (6, 23, '2023-10-05 18:34:56.450525', '2023-10-05 18:34:56.453516', 'PASS', 20);
INSERT INTO `history_detail` VALUES (7, 2, '2023-10-05 18:34:56.438556', '2023-10-05 18:34:56.449526', 'PASS', 20);
INSERT INTO `history_detail` VALUES (8, 1, '2023-10-08 14:26:11.170888', '2023-10-08 14:26:11.176470', 'PASS', 21);
INSERT INTO `history_detail` VALUES (9, 2, '2023-10-08 14:26:11.160824', '2023-10-08 14:26:11.167664', 'PASS', 21);
INSERT INTO `history_detail` VALUES (10, 23, '2023-10-08 14:26:11.168440', '2023-10-08 14:26:11.170679', 'PASS', 21);
INSERT INTO `history_detail` VALUES (11, 25, '2023-10-29 19:18:36.726271', '2023-10-29 19:18:36.729263', 'PASS', 22);
INSERT INTO `history_detail` VALUES (12, 1, '2023-10-29 19:18:36.719293', '2023-10-29 19:18:36.726271', 'PASS', 22);
INSERT INTO `history_detail` VALUES (13, 2, '2023-10-29 19:18:36.705326', '2023-10-29 19:18:36.713307', 'PASS', 22);
INSERT INTO `history_detail` VALUES (14, 23, '2023-10-29 19:18:36.713307', '2023-10-29 19:18:36.718293', 'PASS', 22);
INSERT INTO `history_detail` VALUES (15, 25, '2023-10-29 22:01:28.915787', '2023-10-29 22:01:28.918816', 'PASS', 24);
INSERT INTO `history_detail` VALUES (16, 1, '2023-10-29 22:01:28.910674', '2023-10-29 22:01:28.915787', 'PASS', 24);
INSERT INTO `history_detail` VALUES (17, 2, '2023-10-29 22:01:28.901663', '2023-10-29 22:01:28.907673', 'PASS', 24);
INSERT INTO `history_detail` VALUES (18, 23, '2023-10-29 22:01:28.907673', '2023-10-29 22:01:28.909667', 'PASS', 24);
INSERT INTO `history_detail` VALUES (19, 25, '2023-10-29 22:02:55.485618', '2023-10-29 22:02:55.489611', 'PASS', 25);
INSERT INTO `history_detail` VALUES (20, 1, '2023-10-29 22:02:55.480632', '2023-10-29 22:02:55.485618', 'PASS', 25);
INSERT INTO `history_detail` VALUES (21, 2, '2023-10-29 22:02:55.468663', '2023-10-29 22:02:55.477640', 'PASS', 25);
INSERT INTO `history_detail` VALUES (22, 23, '2023-10-29 22:02:55.477640', '2023-10-29 22:02:55.479634', 'PASS', 25);
INSERT INTO `history_detail` VALUES (23, 25, '2023-10-29 22:43:33.477445', '2023-10-29 22:43:33.478924', 'PASS', 28);
INSERT INTO `history_detail` VALUES (24, 1, '2023-10-29 22:43:33.471500', '2023-10-29 22:43:33.476483', 'PASS', 28);
INSERT INTO `history_detail` VALUES (25, 2, '2023-10-29 22:43:33.462370', '2023-10-29 22:43:33.468509', 'PASS', 28);
INSERT INTO `history_detail` VALUES (26, 23, '2023-10-29 22:43:33.469466', '2023-10-29 22:43:33.471500', 'PASS', 28);
INSERT INTO `history_detail` VALUES (27, 25, '2023-10-29 22:43:33.477445', '2023-10-29 22:43:33.478924', 'PASS', 27);
INSERT INTO `history_detail` VALUES (28, 1, '2023-10-29 22:43:33.471500', '2023-10-29 22:43:33.476483', 'PASS', 27);
INSERT INTO `history_detail` VALUES (29, 2, '2023-10-29 22:43:33.463367', '2023-10-29 22:43:33.468509', 'PASS', 27);
INSERT INTO `history_detail` VALUES (30, 23, '2023-10-29 22:43:33.469466', '2023-10-29 22:43:33.471500', 'PASS', 27);

-- ----------------------------
-- Table structure for keyword_group
-- ----------------------------
DROP TABLE IF EXISTS `keyword_group`;
CREATE TABLE `keyword_group`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `group_type` int NOT NULL,
  `project_id` int NULL DEFAULT NULL,
  `user_group_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 100 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of keyword_group
-- ----------------------------
INSERT INTO `keyword_group` VALUES (1, '平台组件', 1, NULL, NULL);
INSERT INTO `keyword_group` VALUES (2, '流程控制', 0, NULL, NULL);
INSERT INTO `keyword_group` VALUES (3, '变量操作', 0, NULL, NULL);
INSERT INTO `keyword_group` VALUES (4, '结果校验', 0, NULL, NULL);
INSERT INTO `keyword_group` VALUES (5, '字符操作', 0, NULL, NULL);
INSERT INTO `keyword_group` VALUES (6, '列表操作', 0, NULL, NULL);
INSERT INTO `keyword_group` VALUES (7, '字典操作', 0, NULL, NULL);
INSERT INTO `keyword_group` VALUES (8, '时间操作', 0, NULL, NULL);
INSERT INTO `keyword_group` VALUES (9, '数据库操作', 0, NULL, NULL);
INSERT INTO `keyword_group` VALUES (10, 'HTTP请求', 0, NULL, NULL);
INSERT INTO `keyword_group` VALUES (18, '其他类', 0, NULL, NULL);
INSERT INTO `keyword_group` VALUES (98, '项目1类', 2, 1, 1);
INSERT INTO `keyword_group` VALUES (99, '项目2类', 2, 2, 1);

-- ----------------------------
-- Table structure for lib_keyword
-- ----------------------------
DROP TABLE IF EXISTS `lib_keyword`;
CREATE TABLE `lib_keyword`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `ext_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `desc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `group_id` int NOT NULL,
  `input_params` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `input_desc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `output_params` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `output_desc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `input_type` int NOT NULL,
  `image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `mark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` int NOT NULL,
  `output_type` int NOT NULL,
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `category` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE,
  UNIQUE INDEX `lib_keyword_ext_name_f2103d5b_uniq`(`ext_name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 118 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of lib_keyword
-- ----------------------------
INSERT INTO `lib_keyword` VALUES (2, 'log', '2022-08-07 21:42:10.422564', '2022-08-09 22:33:02.095732', '打印输出', '打印信息到日志中', 18, 'any', '打印的变量', '', '', 1, 'icons/keyword/log.png', NULL, 0, 0, 'BuiltIn', 1);
INSERT INTO `lib_keyword` VALUES (4, 'set_variable', '2022-08-11 22:24:42.761485', '2022-08-11 22:24:42.761485', '设置变量', '设置一个自定义变量', 3, 'any', '任意参数', '${out}', '变量名称', 1, 'icons/keyword/should_be_equal.png', NULL, 0, 1, 'BuiltIn', 1);
INSERT INTO `lib_keyword` VALUES (5, 'should_be_equal', '2022-08-11 22:26:15.201615', '2022-08-11 22:26:15.201615', '应该相等', '比较两个变量值是否相等', 4, 'value1|value2', '参数1|参数2', '', '', 2, 'icons/keyword/set_variable.png', NULL, 0, 0, 'BuiltIn', 1);
INSERT INTO `lib_keyword` VALUES (6, 'create_list', '2022-08-11 22:27:00.666799', '2022-08-11 22:27:00.666799', '创建列表', '创建一个列表', 6, 'list', '列表元素', '${out}', '参数列表', 3, 'icons/keyword/create_list.png', NULL, 0, 1, 'BuiltIn', 1);
INSERT INTO `lib_keyword` VALUES (7, 'sleep', '2022-08-11 22:07:35.000000', '2023-02-17 22:07:48.000000', '等待时间', '等待时间，单位为妙', 8, 'time', '等待的时长(s)', NULL, NULL, 1, 'icons/keyword/sleep.png', NULL, 0, 0, 'BuiltIn', 1);
INSERT INTO `lib_keyword` VALUES (8, 'connect_mysql', '2022-08-11 22:26:15.201615', '2022-08-11 22:26:15.201615', '连接原创MySQL数据库', '连接MySQL数据库', 9, 'host|port', 'mysql主机地址|端口', '', '', 2, 'icons/keyword/connect_mysql.png', NULL, 0, 0, 'BuiltIn', 1);
INSERT INTO `lib_keyword` VALUES (9, 'create_dictionary', '2022-08-11 23:29:57.000000', '2022-08-11 23:30:17.000000', '创建字典', '创建一个字典', 7, 'dict', '字典键值对', '${out}', '参数字典', 4, 'icons/keyword/create_dictionary.png', NULL, 0, 1, 'BuiltIn', 1);
INSERT INTO `lib_keyword` VALUES (10, 'create_timestamp', '2023-06-26 18:48:17.000000', '2023-06-26 18:48:36.000000', '获取时间戳', '获取当前时间戳', 8, NULL, NULL, '${out}', '当前时间戳', 0, 'icons/keyword/create_timestamp.png', NULL, 0, 1, 'BuiltIn', 1);
INSERT INTO `lib_keyword` VALUES (102, 'for', '2023-08-26 11:16:35.459753', '2023-08-26 11:16:35.459753', 'For', '', 2, '@{args}', '', '', '', 3, 'icons/keyword/for.png', NULL, 0, 0, 'BuiltIn', 0);
INSERT INTO `lib_keyword` VALUES (103, 'end', '2023-08-26 11:23:52.737554', '2023-08-26 11:23:52.737554', 'End', '', 2, '', '', '', '', 0, 'icons/keyword/end.png', NULL, 0, 0, 'BuiltIn', 0);
INSERT INTO `lib_keyword` VALUES (104, 'if', '2023-08-26 11:25:16.916290', '2023-08-26 11:25:16.916290', 'If', '', 2, 'condition', '条件语句', '', '', 1, 'icons/keyword/if.png', NULL, 0, 0, 'BuiltIn', 0);
INSERT INTO `lib_keyword` VALUES (105, 'else_if', '2023-08-26 11:26:04.681013', '2023-08-26 11:26:04.681013', 'Else If', '', 2, 'condition', '条件语句', '', '', 1, 'icons/keyword/else_if.png', NULL, 0, 0, 'BuiltIn', 0);
INSERT INTO `lib_keyword` VALUES (106, 'else', '2023-08-26 11:26:26.617096', '2023-08-26 11:26:26.617096', 'Else', '', 2, '', '', '', '', 0, 'icons/keyword/else.png', NULL, 0, 0, 'BuiltIn', 0);
INSERT INTO `lib_keyword` VALUES (110, 'while', '2023-08-26 11:27:57.308400', '2023-08-26 11:27:57.308400', 'While', '', 2, 'condition', '条件语句', '', '', 1, 'icons/keyword/while.png', NULL, 0, 0, 'BuiltIn', 0);
INSERT INTO `lib_keyword` VALUES (111, 'continue', '2023-08-26 11:28:23.999387', '2023-08-26 11:28:23.999387', 'Continue', '', 2, '', '', '', '', 0, 'icons/keyword/continue.png', NULL, 0, 0, 'BuiltIn', 0);
INSERT INTO `lib_keyword` VALUES (112, 'break', '2023-08-26 11:28:41.110446', '2023-08-26 11:28:41.111444', 'Break', '', 2, '', '', '', '', 0, 'icons/keyword/break.png', NULL, 0, 0, 'BuiltIn', 0);
INSERT INTO `lib_keyword` VALUES (113, 'return', '2023-08-26 11:28:59.964957', '2023-08-26 11:28:59.964957', 'Return', '', 2, 'result', '返回值', '', '', 1, 'icons/keyword/return.png', NULL, 0, 0, 'BuiltIn', 0);
INSERT INTO `lib_keyword` VALUES (117, 'http_post', '2023-10-29 16:48:06.831750', '2023-10-29 16:48:06.831750', '发送POST请求', '发送http post请求', 10, 'url|data|header', '请求地址|请求数据|请求头', '${response}', '请求json响应', 2, 'icons/keyword/http_post.png', NULL, 0, 1, 'HttpClient', 3);

-- ----------------------------
-- Table structure for notice
-- ----------------------------
DROP TABLE IF EXISTS `notice`;
CREATE TABLE `notice`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ding_token` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `ding_keyword` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `wecom_token` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `wecom_keyword` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `lark_token` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `lark_keyword` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `notice_mode` int NOT NULL,
  `notice_switch` tinyint(1) NOT NULL,
  `rcv_email` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `email_switch` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notice
-- ----------------------------
INSERT INTO `notice` VALUES (1, 1, '2023-10-17 22:59:34.710316', '2023-10-17 23:02:35.451711', '123456@163.com', '123456@163.com', '', '', 'wechattokenforauto123', '自动化', '', '', 1, 1, '456123@163.com', 1);

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` int NOT NULL,
  `personal` tinyint(1) NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 28 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of project
-- ----------------------------
INSERT INTO `project` VALUES (1, 'SKYLARK', '2022-08-18 23:16:32.915535', '2022-08-18 23:16:32.915535', '123456@163.com', 'delavpeng@163.com', 0, 0, 1);
INSERT INTO `project` VALUES (25, 'Test001', '2023-08-20 16:25:29.049549', '2023-10-15 23:45:40.668037', '123456@163.com', '123456@163.com', 0, 1, 1);

-- ----------------------------
-- Table structure for project_permission
-- ----------------------------
DROP TABLE IF EXISTS `project_permission`;
CREATE TABLE `project_permission`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `project_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of project_permission
-- ----------------------------
INSERT INTO `project_permission` VALUES (7, 6, 25);
INSERT INTO `project_permission` VALUES (8, 6, 1);

-- ----------------------------
-- Table structure for project_version
-- ----------------------------
DROP TABLE IF EXISTS `project_version`;
CREATE TABLE `project_version`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `create_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `project_id` int NOT NULL,
  `branch` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `version` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sources` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `remark` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` int NOT NULL,
  `nodes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `run_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `total_case` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of project_version
-- ----------------------------
INSERT INTO `project_version` VALUES (1, '2023-04-05 21:50:52.706705', '2023-10-28 14:41:53.495524', 1, 'v1.0.0', '123456@163.com', '123456@163.com', '1.0.0', '{\"1\": {\"1\": {\"base_resources\": {\"SKYLARK/1_1_common.resource\": \"*** Variables ***\\r\\n${RedisPass}        123456\\r\\n${RedisPort}        10061\\r\\n${phone}        1889111\\r\\n${password}        147258\\r\\n${adyen}        10012801\\r\\n${apcc}        10013801\\r\\n${ebanx}        10016201\\r\\n${santander}        10014800\\r\\n${AdminDomain}        admin.com\\r\\n${AdminDomain}        admin.com\\r\\n${AdminDomain}        admin.com\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/1_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/1_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}, \"2\": {\"base_resources\": {\"SKYLARK/1_2_common.resource\": \"*** Variables ***\\r\\n${RedisPass}        123456\\r\\n${RedisPort}        10061\\r\\n${phone}        00866660102\\r\\n${password}        123456\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/1_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/1_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}}, \"2\": {\"1\": {\"base_resources\": {\"SKYLARK/2_1_common.resource\": \"*** Variables ***\\r\\n${phone}        1889111\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/2_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/2_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}, \"2\": {\"base_resources\": {\"SKYLARK/2_2_common.resource\": \"*** Variables ***\\r\\n${password}        123456\\r\\n${phone}        00866660102\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/2_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/2_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}}, \"3\": {\"1\": {\"base_resources\": {\"SKYLARK/3_1_common.resource\": \"*** Variables ***\\r\\n${phone}        1889111\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/3_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/3_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}, \"2\": {\"base_resources\": {\"SKYLARK/3_2_common.resource\": \"*** Variables ***\\r\\n${password}        123456\\r\\n${phone}        00866660102\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/3_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/3_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}}, \"4\": {\"1\": {\"base_resources\": {\"SKYLARK/4_1_common.resource\": \"*** Variables ***\\r\\n${phone}        1889111\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/4_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/4_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}, \"2\": {\"base_resources\": {\"SKYLARK/4_2_common.resource\": \"*** Variables ***\\r\\n${password}        123456\\r\\n${phone}        00866660102\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/4_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/4_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}}}', 'update', 0, '[{\"mid\": 1, \"id\": \"147639f4-755d-11ee-9420-283a4d1530de\", \"pid\": 0, \"name\": \"CASES\", \"desc\": \"D\", \"extra\": {}}, {\"mid\": 9, \"id\": \"147723a8-755d-11ee-8191-283a4d1530de\", \"pid\": \"147639f4-755d-11ee-9420-283a4d1530de\", \"name\": \"examples\", \"desc\": \"D\", \"extra\": {}}, {\"mid\": 1, \"id\": \"14785b6e-755d-11ee-a7e9-283a4d1530de\", \"pid\": \"147723a8-755d-11ee-8191-283a4d1530de\", \"name\": \"wechat\", \"desc\": \"S\", \"extra\": {}}, {\"mid\": 2, \"id\": \"147a44fa-755d-11ee-b3f8-283a4d1530de\", \"pid\": \"14785b6e-755d-11ee-a7e9-283a4d1530de\", \"name\": \"case002\", \"desc\": \"C\", \"extra\": {\"tag\": [\"Ayden\", \"ID\"], \"pri\": 3}}, {\"mid\": 23, \"id\": \"147ab9e4-755d-11ee-8385-283a4d1530de\", \"pid\": \"14785b6e-755d-11ee-a7e9-283a4d1530de\", \"name\": \"case003\", \"desc\": \"C\", \"extra\": {\"tag\": [\"ID\", \"Santander\", \"Airpay\"], \"pri\": 2}}, {\"mid\": 1, \"id\": \"147ba418-755d-11ee-a7ba-283a4d1530de\", \"pid\": \"14785b6e-755d-11ee-a7e9-283a4d1530de\", \"name\": \"case001\", \"desc\": \"C\", \"extra\": {\"tag\": [\"Pix\", \"Ayden\", \"BR\"], \"pri\": 1}}, {\"mid\": 25, \"id\": \"147c6664-755d-11ee-b5d6-283a4d1530de\", \"pid\": \"14785b6e-755d-11ee-a7e9-283a4d1530de\", \"name\": \"case004\", \"desc\": \"C\", \"extra\": {\"tag\": [\"Santander\"], \"pri\": 4}}]', '[{\"id\": 1, \"name\": \"CASES\", \"category\": 0, \"project_id\": 1, \"parent_dir_id\": null, \"extra_data\": {\"variables\": [], \"fixtures\": {\"suite_setup\": \"\\u6253\\u5370\\u8f93\\u51fa|\\u6d4b\\u8bd5\\u7528\\u4f8b\\u76ee\\u5f55\\uff1aCASES\", \"suite_teardown\": \"\", \"test_setup\": \"\", \"test_teardown\": \"\"}, \"tags\": []}, \"type\": \"D\", \"children\": [{\"id\": 9, \"name\": \"examples\", \"category\": 0, \"project_id\": 1, \"parent_dir_id\": 1, \"extra_data\": {\"variables\": [], \"fixtures\": {\"suite_setup\": \"Login\", \"suite_teardown\": \"\", \"test_setup\": \"\", \"test_teardown\": \"\"}, \"tags\": []}, \"type\": \"D\", \"children\": [{\"id\": 1, \"name\": \"wechat\", \"category\": 0, \"suite_dir_id\": 9, \"timeout\": null, \"extra_data\": {\"variables\": [{\"name\": \"${suiteHost}\", \"value\": \"9901\"}, {\"name\": \"${suitePort}\", \"value\": \"8088\"}, {\"name\": \"${password}\", \"value\": \"123456\"}], \"fixtures\": {\"suite_setup\": \"\\u6253\\u5370\\u8f93\\u51fa|wechat\\u524d\\u7f6e\\u6b65\\u9aa4\", \"suite_teardown\": null, \"test_setup\": null, \"test_teardown\": null}, \"tags\": []}, \"type\": \"S\", \"children\": [{\"id\": 2, \"name\": \"case002\", \"category\": 0, \"test_suite_id\": 1, \"inputs\": null, \"outputs\": null, \"timeout\": \"2 minutes\", \"extra_data\": {\"variables\": [], \"fixtures\": {}, \"entities\": [{\"input_args\": \"${10013801}\", \"output_args\": \"${channel}\", \"keyword_id\": 4, \"keyword_type\": 1}, {\"input_args\": \"${CURDIR}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${TEMPDIR}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${EXECDIR}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${FILEDIR}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}]}, \"type\": \"C\"}, {\"id\": 23, \"name\": \"case003\", \"category\": 0, \"test_suite_id\": 1, \"inputs\": null, \"outputs\": null, \"timeout\": null, \"extra_data\": {\"variables\": [], \"fixtures\": {}, \"entities\": [{\"input_args\": \"${Failed}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${ACCOUNT}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${ACCOUNT[\'username\']}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}]}, \"type\": \"C\"}, {\"id\": 1, \"name\": \"case001\", \"category\": 0, \"test_suite_id\": 1, \"inputs\": null, \"outputs\": null, \"timeout\": \"3 seconds\", \"extra_data\": {\"variables\": [], \"fixtures\": {}, \"entities\": [{\"input_args\": \"${cur_env}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"789#@#456#@#123\", \"output_args\": \"${out}\", \"keyword_id\": 6, \"keyword_type\": 1}, {\"input_args\": \"${index}#@#IN#@#1#@#2#@#3\", \"output_args\": \"\", \"keyword_id\": 102, \"keyword_type\": 1}, {\"input_args\": \"${index}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"\", \"output_args\": \"\", \"keyword_id\": 103, \"keyword_type\": 1}, {\"input_args\": \"{\\\"key\\\":10001, \\\"value\\\":\\\"dict\\\"}\", \"output_args\": \"${request}\", \"keyword_id\": 4, \"keyword_type\": 1}]}, \"type\": \"C\"}, {\"id\": 25, \"name\": \"case004\", \"category\": 0, \"test_suite_id\": 1, \"inputs\": null, \"outputs\": null, \"timeout\": null, \"extra_data\": {\"variables\": [], \"fixtures\": {}, \"entities\": [{\"input_args\": \"a=1#@#b=2\", \"output_args\": \"\", \"keyword_id\": 9, \"keyword_type\": 1}]}, \"type\": \"C\"}]}]}]}]', 4);
INSERT INTO `project_version` VALUES (2, '2023-04-14 21:54:58.553496', '2023-10-28 14:41:39.262757', 1, 'v1.1.0', '123456@163.com', '123456@163.com', '1.0.0', '{\"1\": {\"1\": {\"base_resources\": {\"SKYLARK/1_1_common.resource\": \"*** Variables ***\\r\\n${RedisPass}        123456\\r\\n${RedisPort}        10061\\r\\n${phone}        1889111\\r\\n${password}        147258\\r\\n${adyen}        10012801\\r\\n${apcc}        10013801\\r\\n${ebanx}        10016201\\r\\n${santander}        10014800\\r\\n${AdminDomain}        admin.com\\r\\n${AdminDomain}        admin.com\\r\\n${AdminDomain}        admin.com\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/1_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/1_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}, \"2\": {\"base_resources\": {\"SKYLARK/1_2_common.resource\": \"*** Variables ***\\r\\n${RedisPass}        123456\\r\\n${RedisPort}        10061\\r\\n${phone}        00866660102\\r\\n${password}        123456\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/1_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/1_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}}, \"2\": {\"1\": {\"base_resources\": {\"SKYLARK/2_1_common.resource\": \"*** Variables ***\\r\\n${phone}        1889111\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/2_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/2_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}, \"2\": {\"base_resources\": {\"SKYLARK/2_2_common.resource\": \"*** Variables ***\\r\\n${password}        123456\\r\\n${phone}        00866660102\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/2_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/2_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}}, \"3\": {\"1\": {\"base_resources\": {\"SKYLARK/3_1_common.resource\": \"*** Variables ***\\r\\n${phone}        1889111\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/3_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/3_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}, \"2\": {\"base_resources\": {\"SKYLARK/3_2_common.resource\": \"*** Variables ***\\r\\n${password}        123456\\r\\n${phone}        00866660102\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/3_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/3_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}}, \"4\": {\"1\": {\"base_resources\": {\"SKYLARK/4_1_common.resource\": \"*** Variables ***\\r\\n${phone}        1889111\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/4_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/4_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}, \"2\": {\"base_resources\": {\"SKYLARK/4_2_common.resource\": \"*** Variables ***\\r\\n${password}        123456\\r\\n${phone}        00866660102\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/4_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/4_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dict    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}}}', 'update', 0, '[{\"mid\": 1, \"id\": \"0bf55302-755d-11ee-a543-283a4d1530de\", \"pid\": 0, \"name\": \"CASES\", \"desc\": \"D\", \"extra\": {}}, {\"mid\": 9, \"id\": \"0bf663c2-755d-11ee-beaf-283a4d1530de\", \"pid\": \"0bf55302-755d-11ee-a543-283a4d1530de\", \"name\": \"examples\", \"desc\": \"D\", \"extra\": {}}, {\"mid\": 1, \"id\": \"0bf83740-755d-11ee-96ca-283a4d1530de\", \"pid\": \"0bf663c2-755d-11ee-beaf-283a4d1530de\", \"name\": \"wechat\", \"desc\": \"S\", \"extra\": {}}, {\"mid\": 2, \"id\": \"0bfa31c0-755d-11ee-82cd-283a4d1530de\", \"pid\": \"0bf83740-755d-11ee-96ca-283a4d1530de\", \"name\": \"case002\", \"desc\": \"C\", \"extra\": {\"tag\": [\"Ayden\", \"ID\"], \"pri\": 3}}, {\"mid\": 23, \"id\": \"0bfaa7ee-755d-11ee-8d81-283a4d1530de\", \"pid\": \"0bf83740-755d-11ee-96ca-283a4d1530de\", \"name\": \"case003\", \"desc\": \"C\", \"extra\": {\"tag\": [\"ID\", \"Santander\", \"Airpay\"], \"pri\": 2}}, {\"mid\": 1, \"id\": \"0bfb6ade-755d-11ee-8e84-283a4d1530de\", \"pid\": \"0bf83740-755d-11ee-96ca-283a4d1530de\", \"name\": \"case001\", \"desc\": \"C\", \"extra\": {\"tag\": [\"Pix\", \"Ayden\", \"BR\"], \"pri\": 1}}, {\"mid\": 25, \"id\": \"0bfc547e-755d-11ee-84b9-283a4d1530de\", \"pid\": \"0bf83740-755d-11ee-96ca-283a4d1530de\", \"name\": \"case004\", \"desc\": \"C\", \"extra\": {\"tag\": [\"Santander\"], \"pri\": 4}}]', '[{\"id\": 1, \"name\": \"CASES\", \"category\": 0, \"project_id\": 1, \"parent_dir_id\": null, \"extra_data\": {\"variables\": [], \"fixtures\": {\"suite_setup\": \"\\u6253\\u5370\\u8f93\\u51fa|\\u6d4b\\u8bd5\\u7528\\u4f8b\\u76ee\\u5f55\\uff1aCASES\", \"suite_teardown\": \"\", \"test_setup\": \"\", \"test_teardown\": \"\"}, \"tags\": []}, \"type\": \"D\", \"children\": [{\"id\": 9, \"name\": \"examples\", \"category\": 0, \"project_id\": 1, \"parent_dir_id\": 1, \"extra_data\": {\"variables\": [], \"fixtures\": {\"suite_setup\": \"Login\", \"suite_teardown\": \"\", \"test_setup\": \"\", \"test_teardown\": \"\"}, \"tags\": []}, \"type\": \"D\", \"children\": [{\"id\": 1, \"name\": \"wechat\", \"category\": 0, \"suite_dir_id\": 9, \"timeout\": null, \"extra_data\": {\"variables\": [{\"name\": \"${suiteHost}\", \"value\": \"9901\"}, {\"name\": \"${suitePort}\", \"value\": \"8088\"}, {\"name\": \"${password}\", \"value\": \"123456\"}], \"fixtures\": {\"suite_setup\": \"\\u6253\\u5370\\u8f93\\u51fa|wechat\\u524d\\u7f6e\\u6b65\\u9aa4\", \"suite_teardown\": null, \"test_setup\": null, \"test_teardown\": null}, \"tags\": []}, \"type\": \"S\", \"children\": [{\"id\": 2, \"name\": \"case002\", \"category\": 0, \"test_suite_id\": 1, \"inputs\": null, \"outputs\": null, \"timeout\": \"2 minutes\", \"extra_data\": {\"variables\": [], \"fixtures\": {}, \"entities\": [{\"input_args\": \"${10013801}\", \"output_args\": \"${channel}\", \"keyword_id\": 4, \"keyword_type\": 1}, {\"input_args\": \"${CURDIR}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${TEMPDIR}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${EXECDIR}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${FILEDIR}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}]}, \"type\": \"C\"}, {\"id\": 23, \"name\": \"case003\", \"category\": 0, \"test_suite_id\": 1, \"inputs\": null, \"outputs\": null, \"timeout\": null, \"extra_data\": {\"variables\": [], \"fixtures\": {}, \"entities\": [{\"input_args\": \"${Failed}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${ACCOUNT}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${ACCOUNT[\'username\']}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}]}, \"type\": \"C\"}, {\"id\": 1, \"name\": \"case001\", \"category\": 0, \"test_suite_id\": 1, \"inputs\": null, \"outputs\": null, \"timeout\": \"3 seconds\", \"extra_data\": {\"variables\": [], \"fixtures\": {}, \"entities\": [{\"input_args\": \"${cur_env}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"789#@#456#@#123\", \"output_args\": \"${out}\", \"keyword_id\": 6, \"keyword_type\": 1}, {\"input_args\": \"${index}#@#IN#@#1#@#2#@#3\", \"output_args\": \"\", \"keyword_id\": 102, \"keyword_type\": 1}, {\"input_args\": \"${index}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"\", \"output_args\": \"\", \"keyword_id\": 103, \"keyword_type\": 1}, {\"input_args\": \"{\\\"key\\\":10001, \\\"value\\\":\\\"dict\\\"}\", \"output_args\": \"${request}\", \"keyword_id\": 4, \"keyword_type\": 1}]}, \"type\": \"C\"}, {\"id\": 25, \"name\": \"case004\", \"category\": 0, \"test_suite_id\": 1, \"inputs\": null, \"outputs\": null, \"timeout\": null, \"extra_data\": {\"variables\": [], \"fixtures\": {}, \"entities\": [{\"input_args\": \"a=1#@#b=2\", \"output_args\": \"\", \"keyword_id\": 9, \"keyword_type\": 1}]}, \"type\": \"C\"}]}]}]}]', 4);
INSERT INTO `project_version` VALUES (3, '2023-09-02 17:06:35.682956', '2023-10-29 19:11:40.928993', 1, 'v2.0.0', '123456@163.com', '123456@163.com', '1.0.0', '{\"1\": {\"1\": {\"base_resources\": {\"SKYLARK/1_1_common.resource\": \"*** Settings ***\\r\\nLibrary        C:/Users/Delav/Desktop/skylarklibrary/libraries/Public/HttpClient.py\\r\\n\\r\\n*** Variables ***\\r\\n${RedisPass}        123456\\r\\n${RedisPort}        10061\\r\\n${phone}        1889111\\r\\n${password}        147258\\r\\n${adyen}        10012801\\r\\n${apcc}        10013801\\r\\n${ebanx}        10016201\\r\\n${santander}        10014800\\r\\n${AdminDomain}        admin.com\\r\\n${AdminDomain}        admin.com\\r\\n${AdminDomain}        admin.com\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/1_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/1_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dictionary    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}, \"2\": {\"base_resources\": {\"SKYLARK/1_2_common.resource\": \"*** Settings ***\\r\\nLibrary        C:/Users/Delav/Desktop/skylarklibrary/libraries/Public/HttpClient.py\\r\\n\\r\\n*** Variables ***\\r\\n${RedisPass}        123456\\r\\n${RedisPort}        10061\\r\\n${phone}        00866660102\\r\\n${password}        123456\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/1_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/1_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dictionary    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}}, \"2\": {\"1\": {\"base_resources\": {\"SKYLARK/2_1_common.resource\": \"*** Settings ***\\r\\nLibrary        C:/Users/Delav/Desktop/skylarklibrary/libraries/Public/HttpClient.py\\r\\n\\r\\n*** Variables ***\\r\\n${phone}        1889111\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/2_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/2_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dictionary    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}, \"2\": {\"base_resources\": {\"SKYLARK/2_2_common.resource\": \"*** Settings ***\\r\\nLibrary        C:/Users/Delav/Desktop/skylarklibrary/libraries/Public/HttpClient.py\\r\\n\\r\\n*** Variables ***\\r\\n${password}        123456\\r\\n${phone}        00866660102\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/2_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/2_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dictionary    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}}, \"3\": {\"1\": {\"base_resources\": {\"SKYLARK/3_1_common.resource\": \"*** Settings ***\\r\\nLibrary        C:/Users/Delav/Desktop/skylarklibrary/libraries/Public/HttpClient.py\\r\\n\\r\\n*** Variables ***\\r\\n${phone}        1889111\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/3_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/3_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dictionary    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}, \"2\": {\"base_resources\": {\"SKYLARK/3_2_common.resource\": \"*** Settings ***\\r\\nLibrary        C:/Users/Delav/Desktop/skylarklibrary/libraries/Public/HttpClient.py\\r\\n\\r\\n*** Variables ***\\r\\n${password}        123456\\r\\n${phone}        00866660102\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/3_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/3_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dictionary    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}}, \"4\": {\"1\": {\"base_resources\": {\"SKYLARK/4_1_common.resource\": \"*** Settings ***\\r\\nLibrary        C:/Users/Delav/Desktop/skylarklibrary/libraries/Public/HttpClient.py\\r\\n\\r\\n*** Variables ***\\r\\n${phone}        1889111\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/4_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/4_1_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dictionary    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}, \"2\": {\"base_resources\": {\"SKYLARK/4_2_common.resource\": \"*** Settings ***\\r\\nLibrary        C:/Users/Delav/Desktop/skylarklibrary/libraries/Public/HttpClient.py\\r\\n\\r\\n*** Variables ***\\r\\n${password}        123456\\r\\n${phone}        00866660102\\r\\n\"}, \"user_keywords\": {\"SKYLARK/COMPOS/payment.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/4_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nLogin\\r\\n    log    \\u6d4b\\u8bd5\\u5957\\u4ef6\\u524d\\u7f6e\\u6b65\\u9aa4\\r\\n\\r\\n\", \"SKYLARK/COMPOS/refund.resource\": \"*** Settings ***\\r\\nResource        SKYLARK/4_2_common.resource\\r\\n\\r\\n*** Keywords ***\\r\\nToBank\\r\\n    [Arguments]    ${ar}\\r\\n    create_dictionary    a=1    b=2\\r\\n    [Return]    ${out}\\r\\n\\r\\n\"}, \"variable_files\": {\"SKYLARK/CONSTS/Python/0_0_1696058874_myvariable.py\": \"def get_variables(env, region):\\n    variables = {\'cur_env\': env, \'cur_region\': region}\\n    return variables\\n\\nVARIABLE = \\\"An example string, not valid\\\"\\nSTRINGS = [\\\"one\\\", \\\"two\\\", \\\"kolme\\\", \\\"four\\\"]\", \"SKYLARK/CONSTS/Yaml/0_0_1695552547_TestFile.yaml\": \"account:\\n  username: vuer\\n  password: 123456\"}, \"project_files\": {\"SKYLARK/PROFILES/HelpFiles/change001.txt\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"change001.txt\"}, \"key\": \"123!@#\", \"mtime\": 1695984556}, \"SKYLARK/PROFILES/HelpFiles/Keywords.xlsx\": {\"url\": \"127.0.0.1:8000/api/internal/download_file\", \"params\": {\"path\": \"SKYLARK/PROFILES/HelpFiles\", \"name\": \"Keywords.xlsx\"}, \"key\": \"123!@#\", \"mtime\": 1696059561}}}}}', 'update', 0, '[{\"mid\": 1, \"id\": \"ef5a4924-764b-11ee-9ee6-283a4d1530de\", \"pid\": 0, \"name\": \"CASES\", \"desc\": \"D\", \"extra\": {}}, {\"mid\": 9, \"id\": \"ef5b4a1e-764b-11ee-a657-283a4d1530de\", \"pid\": \"ef5a4924-764b-11ee-9ee6-283a4d1530de\", \"name\": \"examples\", \"desc\": \"D\", \"extra\": {}}, {\"mid\": 1, \"id\": \"ef5d335c-764b-11ee-9bcb-283a4d1530de\", \"pid\": \"ef5b4a1e-764b-11ee-a657-283a4d1530de\", \"name\": \"wechat\", \"desc\": \"S\", \"extra\": {}}, {\"mid\": 2, \"id\": \"ef5ef9f0-764b-11ee-ae50-283a4d1530de\", \"pid\": \"ef5d335c-764b-11ee-9bcb-283a4d1530de\", \"name\": \"case002\", \"desc\": \"C\", \"extra\": {\"tag\": [\"Ayden\", \"ID\"], \"pri\": 3}}, {\"mid\": 23, \"id\": \"ef5fb4e4-764b-11ee-9ecc-283a4d1530de\", \"pid\": \"ef5d335c-764b-11ee-9bcb-283a4d1530de\", \"name\": \"case003\", \"desc\": \"C\", \"extra\": {\"tag\": [\"ID\", \"Santander\", \"Airpay\"], \"pri\": 2}}, {\"mid\": 1, \"id\": \"ef6029e2-764b-11ee-8154-283a4d1530de\", \"pid\": \"ef5d335c-764b-11ee-9bcb-283a4d1530de\", \"name\": \"case001\", \"desc\": \"C\", \"extra\": {\"tag\": [\"Pix\", \"Ayden\", \"BR\"], \"pri\": 1}}, {\"mid\": 25, \"id\": \"ef60af58-764b-11ee-a2e9-283a4d1530de\", \"pid\": \"ef5d335c-764b-11ee-9bcb-283a4d1530de\", \"name\": \"case004\", \"desc\": \"C\", \"extra\": {\"tag\": [\"Santander\"], \"pri\": 4}}]', '[{\"id\": 1, \"name\": \"CASES\", \"category\": 0, \"project_id\": 1, \"parent_dir_id\": null, \"extra_data\": {\"variables\": [], \"fixtures\": {\"suite_setup\": \"\\u6253\\u5370\\u8f93\\u51fa|\\u6d4b\\u8bd5\\u7528\\u4f8b\\u76ee\\u5f55\\uff1aCASES\", \"suite_teardown\": \"\", \"test_setup\": \"\", \"test_teardown\": \"\"}, \"tags\": []}, \"type\": \"D\", \"children\": [{\"id\": 9, \"name\": \"examples\", \"category\": 0, \"project_id\": 1, \"parent_dir_id\": 1, \"extra_data\": {\"variables\": [], \"fixtures\": {\"suite_setup\": \"Login\", \"suite_teardown\": \"\", \"test_setup\": \"\", \"test_teardown\": \"\"}, \"tags\": []}, \"type\": \"D\", \"children\": [{\"id\": 1, \"name\": \"wechat\", \"category\": 0, \"suite_dir_id\": 9, \"timeout\": null, \"extra_data\": {\"variables\": [{\"name\": \"${suiteHost}\", \"value\": \"9901\"}, {\"name\": \"${suitePort}\", \"value\": \"8088\"}, {\"name\": \"${password}\", \"value\": \"123456\"}], \"fixtures\": {\"suite_setup\": \"\\u6253\\u5370\\u8f93\\u51fa|wechat\\u524d\\u7f6e\\u6b65\\u9aa4\", \"suite_teardown\": null, \"test_setup\": null, \"test_teardown\": null}, \"tags\": []}, \"type\": \"S\", \"children\": [{\"id\": 2, \"name\": \"case002\", \"category\": 0, \"test_suite_id\": 1, \"inputs\": null, \"outputs\": null, \"timeout\": \"2 minutes\", \"extra_data\": {\"variables\": [], \"fixtures\": {}, \"entities\": [{\"input_args\": \"${10013801}\", \"output_args\": \"${channel}\", \"keyword_id\": 4, \"keyword_type\": 1}, {\"input_args\": \"${CURDIR}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${TEMPDIR}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${EXECDIR}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${FILEDIR}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}]}, \"type\": \"C\"}, {\"id\": 23, \"name\": \"case003\", \"category\": 0, \"test_suite_id\": 1, \"inputs\": null, \"outputs\": null, \"timeout\": null, \"extra_data\": {\"variables\": [], \"fixtures\": {}, \"entities\": [{\"input_args\": \"${ENV}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${ACCOUNT}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"${ACCOUNT[\'username\']}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}]}, \"type\": \"C\"}, {\"id\": 1, \"name\": \"case001\", \"category\": 0, \"test_suite_id\": 1, \"inputs\": null, \"outputs\": null, \"timeout\": \"3 seconds\", \"extra_data\": {\"variables\": [], \"fixtures\": {}, \"entities\": [{\"input_args\": \"${cur_env}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"789#@#456#@#123\", \"output_args\": \"${out}\", \"keyword_id\": 6, \"keyword_type\": 1}, {\"input_args\": \"${index}#@#IN#@#1#@#2#@#3\", \"output_args\": \"\", \"keyword_id\": 102, \"keyword_type\": 1}, {\"input_args\": \"${index}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"\", \"output_args\": \"\", \"keyword_id\": 103, \"keyword_type\": 1}, {\"input_args\": \"{\\\"key\\\":10001, \\\"value\\\":\\\"dict\\\"}\", \"output_args\": \"${request}\", \"keyword_id\": 4, \"keyword_type\": 1}]}, \"type\": \"C\"}, {\"id\": 25, \"name\": \"case004\", \"category\": 0, \"test_suite_id\": 1, \"inputs\": null, \"outputs\": null, \"timeout\": null, \"extra_data\": {\"variables\": [], \"fixtures\": {}, \"entities\": [{\"input_args\": \"a=1#@#b=2\", \"output_args\": \"\", \"keyword_id\": 9, \"keyword_type\": 1}, {\"input_args\": \"${REGION}\", \"output_args\": \"\", \"keyword_id\": 2, \"keyword_type\": 1}, {\"input_args\": \"https://baidu.com#@#{}#@#{}\", \"output_args\": \"${response}\", \"keyword_id\": 117, \"keyword_type\": 1}, {\"input_args\": \"1#@#1\", \"output_args\": \"\", \"keyword_id\": 5, \"keyword_type\": 1}]}, \"type\": \"C\"}]}]}]}]', 4);

-- ----------------------------
-- Table structure for python_lib
-- ----------------------------
DROP TABLE IF EXISTS `python_lib`;
CREATE TABLE `python_lib`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `lib_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `lib_type` int NOT NULL,
  `lib_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `lib_desc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of python_lib
-- ----------------------------
INSERT INTO `python_lib` VALUES (1, 'HttpClient', 2, 'Public', 'common library');

-- ----------------------------
-- Table structure for region
-- ----------------------------
DROP TABLE IF EXISTS `region`;
CREATE TABLE `region`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` int NOT NULL,
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of region
-- ----------------------------
INSERT INTO `region` VALUES (1, 'ID', 0, '印尼');
INSERT INTO `region` VALUES (2, 'BR', 0, '巴西');

-- ----------------------------
-- Table structure for setup_teardown
-- ----------------------------
DROP TABLE IF EXISTS `setup_teardown`;
CREATE TABLE `setup_teardown`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `module_id` int NOT NULL,
  `module_type` int NOT NULL,
  `suite_setup` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `suite_teardown` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `suite_setup_desc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `suite_teardown_desc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `test_setup` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `test_teardown` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `test_setup_desc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `test_teardown_desc` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of setup_teardown
-- ----------------------------
INSERT INTO `setup_teardown` VALUES (1, 9, 1, 'Login', '', '', '', '', '', '', '');
INSERT INTO `setup_teardown` VALUES (2, 1, 1, '打印输出|测试用例目录：CASES', '', '', '', '', '', '', '');
INSERT INTO `setup_teardown` VALUES (3, 12, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `setup_teardown` VALUES (4, 1, 2, '打印输出|wechat前置步骤', NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for suite_dir
-- ----------------------------
DROP TABLE IF EXISTS `suite_dir`;
CREATE TABLE `suite_dir`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `document` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `category` int NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` int NOT NULL,
  `parent_dir_id` bigint NULL DEFAULT NULL,
  `project_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `suite_dir_project_id_parent_dir_id_name_cdcbafae_uniq`(`project_id` ASC, `parent_dir_id` ASC, `name` ASC) USING BTREE,
  INDEX `suite_dir_parent_dir_id_af60759c_fk_suite_dir_id`(`parent_dir_id` ASC) USING BTREE,
  CONSTRAINT `suite_dir_parent_dir_id_af60759c_fk_suite_dir_id` FOREIGN KEY (`parent_dir_id`) REFERENCES `suite_dir` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `suite_dir_project_id_6e9806d7_fk_project_id` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 121 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of suite_dir
-- ----------------------------
INSERT INTO `suite_dir` VALUES (1, 'CASES', '存放测试用例的目录', 0, '2023-04-01 19:15:22.000000', '2023-04-05 19:15:16.000000', '123456@163.com', 'delavpeng@163.com', 0, NULL, 1);
INSERT INTO `suite_dir` VALUES (2, 'COMPOS', '存放用户自定义高级组件的目录', 1, '2023-04-01 19:15:22.000000', '2023-04-05 19:15:16.000000', '123456@163.com', 'delavpeng@163.com', 0, NULL, 1);
INSERT INTO `suite_dir` VALUES (3, 'CONSTS', '存放项目公共常量的目录，支持python， yaml格式', 2, '2023-04-01 19:15:22.000000', '2023-04-05 19:15:16.000000', '123456@163.com', 'delavpeng@163.com', 0, NULL, 1);
INSERT INTO `suite_dir` VALUES (4, 'PROFILES', '存放项目需要的额外文件的目录', 3, '2023-04-01 19:15:22.000000', '2023-04-05 19:15:16.000000', '123456@163.com', 'delavpeng@163.com', 0, NULL, 1);
INSERT INTO `suite_dir` VALUES (9, 'examples', NULL, 0, '2023-04-05 21:02:40.615999', '2023-08-26 11:45:03.277248', '123456@163.com', '123456@163.com', 0, 1, 1);
INSERT INTO `suite_dir` VALUES (10, 'refund-021469', NULL, 0, '2023-04-05 21:03:21.638049', '2023-08-26 11:44:29.250890', '123456@163.com', '123456@163.com', 2, 1, 1);
INSERT INTO `suite_dir` VALUES (11, 'channels', NULL, 0, '2023-04-05 21:44:30.127088', '2023-04-05 21:44:30.127088', '123456@163.com', '123456@163.com', 2, 10, 1);
INSERT INTO `suite_dir` VALUES (12, 'addcard-021490', NULL, 0, '2023-04-22 16:52:32.209475', '2023-08-26 11:44:50.025952', '123456@163.com', '123456@163.com', 2, 1, 1);
INSERT INTO `suite_dir` VALUES (13, 'pix', NULL, 0, '2023-04-22 16:55:58.658906', '2023-04-22 16:55:58.658906', '123456@163.com', '123456@163.com', 2, 12, 1);
INSERT INTO `suite_dir` VALUES (14, 'cc', NULL, 0, '2023-04-25 23:45:29.152807', '2023-04-25 23:45:29.152807', '123456@163.com', '123456@163.com', 2, 12, 1);
INSERT INTO `suite_dir` VALUES (15, 'Python', NULL, 2, '2023-05-08 21:47:15.576001', '2023-05-14 16:01:45.512809', '123456@163.com', '123456@163.com', 0, 3, 1);
INSERT INTO `suite_dir` VALUES (16, 'santander', NULL, 3, '2023-05-08 21:57:23.453088', '2023-05-08 21:57:23.453088', '123456@163.com', '123456@163.com', 2, 4, 1);
INSERT INTO `suite_dir` VALUES (17, 'Yaml', NULL, 2, '2023-05-14 16:02:12.108618', '2023-09-24 13:04:00.922498', '123456@163.com', '123456@163.com', 0, 3, 1);
INSERT INTO `suite_dir` VALUES (105, 'CASES', '存放测试用例的目录', 0, '2023-08-20 16:25:29.053538', '2023-08-20 16:25:29.053538', '', '', 0, NULL, 25);
INSERT INTO `suite_dir` VALUES (106, 'PROFILES', '存放项目需要的额外文件的目录', 3, '2023-08-20 16:25:29.053538', '2023-08-20 16:25:29.053538', '', '', 0, NULL, 25);
INSERT INTO `suite_dir` VALUES (107, 'COMPOS', '存放用户自定义高级组件的目录', 1, '2023-08-20 16:25:29.053538', '2023-08-20 16:25:29.053538', '', '', 0, NULL, 25);
INSERT INTO `suite_dir` VALUES (108, 'CONSTS', '存放项目公共常量的目录', 2, '2023-08-20 16:25:29.053538', '2023-08-20 16:25:29.053538', '', '', 0, NULL, 25);
INSERT INTO `suite_dir` VALUES (117, 'Json-651874-652102-652226', NULL, 2, '2023-09-24 14:01:18.282141', '2023-09-25 22:30:26.518491', '123456@163.com', '123456@163.com', 2, 3, 1);
INSERT INTO `suite_dir` VALUES (119, 'HelpFiles', NULL, 3, '2023-09-27 22:48:34.804549', '2023-09-27 22:48:34.804549', '123456@163.com', '123456@163.com', 0, 4, 1);

-- ----------------------------
-- Table structure for system_ext
-- ----------------------------
DROP TABLE IF EXISTS `system_ext`;
CREATE TABLE `system_ext`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `info_type` int NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `extra_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_ext
-- ----------------------------

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `project_id` int NOT NULL,
  `module_id` int NOT NULL,
  `module_type` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tag
-- ----------------------------
INSERT INTO `tag` VALUES (4, 'Ayden', 1, 2, 3);
INSERT INTO `tag` VALUES (7, 'Pix', 1, 1, 3);
INSERT INTO `tag` VALUES (10, 'BR', 1, 19, 3);
INSERT INTO `tag` VALUES (11, 'Pix', 1, 19, 3);
INSERT INTO `tag` VALUES (12, 'Ayden', 1, 19, 3);
INSERT INTO `tag` VALUES (13, 'BR', 1, 20, 3);
INSERT INTO `tag` VALUES (14, 'Pix', 1, 20, 3);
INSERT INTO `tag` VALUES (15, 'Ayden', 1, 20, 3);
INSERT INTO `tag` VALUES (16, 'BR', 1, 21, 3);
INSERT INTO `tag` VALUES (17, 'Pix', 1, 21, 3);
INSERT INTO `tag` VALUES (18, 'Ayden', 1, 21, 3);
INSERT INTO `tag` VALUES (19, 'BR', 1, 22, 3);
INSERT INTO `tag` VALUES (20, 'Ayden', 1, 22, 3);
INSERT INTO `tag` VALUES (22, 'Ayden', 1, 1, 3);
INSERT INTO `tag` VALUES (23, 'BR', 1, 1, 3);
INSERT INTO `tag` VALUES (24, 'ID', 1, 23, 3);
INSERT INTO `tag` VALUES (25, 'Santander', 1, 23, 3);
INSERT INTO `tag` VALUES (26, 'Airpay', 1, 23, 3);
INSERT INTO `tag` VALUES (31, 'ID', 1, 2, 3);
INSERT INTO `tag` VALUES (32, 'Santander', 1, 25, 3);

-- ----------------------------
-- Table structure for test_case
-- ----------------------------
DROP TABLE IF EXISTS `test_case`;
CREATE TABLE `test_case`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `category` int NOT NULL,
  `document` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `create_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `priority_id` int NULL DEFAULT NULL,
  `inputs` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `outputs` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `timeout` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` int NOT NULL,
  `test_suite_id` bigint NOT NULL,
  `project_id` int NOT NULL,
  `order` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `test_case_name_test_suite_id_492f1f61_uniq`(`name` ASC, `test_suite_id` ASC) USING BTREE,
  INDEX `test_case_test_suite_id_f175d151_fk_test_suite_id`(`test_suite_id` ASC) USING BTREE,
  CONSTRAINT `test_case_test_suite_id_f175d151_fk_test_suite_id` FOREIGN KEY (`test_suite_id`) REFERENCES `test_suite` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of test_case
-- ----------------------------
INSERT INTO `test_case` VALUES (1, 'case001', 0, 'this is  a test case update by me', '2023-04-05 21:15:35.352376', '2023-10-02 23:21:00.859710', '123456@163.com', '123456@163.com', 1, NULL, NULL, '3 seconds', 0, 1, 1, 4);
INSERT INTO `test_case` VALUES (2, 'case002', 0, NULL, '2023-04-05 21:15:48.073311', '2023-10-18 23:10:19.781372', '123456@163.com', '123456@163.com', 3, NULL, NULL, '2 minutes', 0, 1, 1, 1);
INSERT INTO `test_case` VALUES (3, 'case006', 0, NULL, '2023-04-05 21:45:24.528561', '2023-04-05 21:45:45.947860', '123456@163.com', '123456@163.com', NULL, NULL, NULL, NULL, 0, 2, 1, NULL);
INSERT INTO `test_case` VALUES (4, 'case007-021461', 0, NULL, '2023-04-05 21:45:30.134509', '2023-08-26 11:44:21.320276', '123456@163.com', '123456@163.com', NULL, NULL, NULL, NULL, 2, 2, 1, NULL);
INSERT INTO `test_case` VALUES (6, 'Login', 1, '登录shopee获取token', '2023-04-06 11:41:14.444441', '2023-10-02 22:21:09.525653', '123456@163.com', '123456@163.com', NULL, NULL, NULL, NULL, 0, 3, 1, NULL);
INSERT INTO `test_case` VALUES (7, 'add_visa_card', 0, NULL, '2023-04-22 16:57:07.054918', '2023-07-15 18:40:49.037430', '123456@163.com', '123456@163.com', NULL, NULL, NULL, NULL, 0, 5, 1, NULL);
INSERT INTO `test_case` VALUES (12, 'ToBank', 1, NULL, '2023-04-25 23:51:16.174671', '2023-08-28 23:32:40.464532', '123456@163.com', '123456@163.com', NULL, '${ar}', '${out}', NULL, 0, 4, 1, NULL);
INSERT INTO `test_case` VALUES (13, '支付流程', 0, NULL, '2023-05-28 12:48:47.592870', '2023-08-05 19:06:07.577454', '123456@163.com', '123456@163.com', NULL, NULL, NULL, NULL, 0, 9, 1, NULL);
INSERT INTO `test_case` VALUES (14, '退款流程', 0, NULL, '2023-05-28 12:49:07.189685', '2023-07-15 18:37:48.575969', '123456@163.com', '123456@163.com', NULL, NULL, NULL, NULL, 0, 9, 1, NULL);
INSERT INTO `test_case` VALUES (15, '添加银行卡', 0, NULL, '2023-05-28 13:03:52.888636', '2023-07-15 18:38:41.395732', '123456@163.com', '123456@163.com', NULL, NULL, NULL, NULL, 0, 6, 1, NULL);
INSERT INTO `test_case` VALUES (16, '设置默认卡', 0, NULL, '2023-05-28 13:04:03.583020', '2023-07-15 18:39:00.479184', '123456@163.com', '123456@163.com', NULL, NULL, NULL, NULL, 0, 6, 1, NULL);
INSERT INTO `test_case` VALUES (17, 'case005', 0, '这个一个测试用例', '2023-06-11 19:14:48.904286', '2023-06-15 22:27:06.466997', '123456@163.com', '123456@163.com', 1, NULL, NULL, '10 seconds', 0, 2, 1, NULL);
INSERT INTO `test_case` VALUES (19, 'case001-copy-417665', 0, '这个一个测试用例', '2023-06-15 22:27:27.991902', '2023-07-15 18:41:05.401767', '123456@163.com', '123456@163.com', 1, NULL, NULL, '10 seconds', 2, 2, 1, NULL);
INSERT INTO `test_case` VALUES (20, 'case001-32125copy-417554', 0, 'this is  a test case', '2023-06-20 11:35:25.628537', '2023-07-15 18:39:14.568848', '123456@163.com', '123456@163.com', 1, NULL, NULL, '10 seconds', 2, 5, 1, NULL);
INSERT INTO `test_case` VALUES (21, 'case001-62294copy', 0, 'this is  a test case', '2023-06-28 22:24:54.205443', '2023-06-28 22:24:54.205443', '123456@163.com', '', 1, NULL, NULL, '10 seconds', 0, 22, 1, NULL);
INSERT INTO `test_case` VALUES (22, 'case002-62294copy', 0, NULL, '2023-06-28 22:24:54.211700', '2023-06-28 22:24:54.211700', '123456@163.com', '', 2, NULL, NULL, '2 minutes', 0, 22, 1, NULL);
INSERT INTO `test_case` VALUES (23, 'case003', 0, NULL, '2023-09-11 23:00:01.021746', '2023-10-28 15:00:35.409755', '123456@163.com', '123456@163.com', 2, NULL, NULL, NULL, 0, 1, 1, 2);
INSERT INTO `test_case` VALUES (25, 'case004', 0, NULL, '2023-10-17 22:58:32.831427', '2023-10-29 18:02:13.004051', '123456@163.com', '123456@163.com', 4, NULL, NULL, NULL, 0, 1, 1, NULL);

-- ----------------------------
-- Table structure for test_suite
-- ----------------------------
DROP TABLE IF EXISTS `test_suite`;
CREATE TABLE `test_suite`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `document` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `category` int NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `create_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `update_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `timeout` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` int NOT NULL,
  `suite_dir_id` bigint NOT NULL,
  `project_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `test_suite_name_suite_dir_id_158da50d_uniq`(`name` ASC, `suite_dir_id` ASC) USING BTREE,
  INDEX `test_suite_suite_dir_id_97cfeed7_fk_suite_dir_id`(`suite_dir_id` ASC) USING BTREE,
  CONSTRAINT `test_suite_suite_dir_id_97cfeed7_fk_suite_dir_id` FOREIGN KEY (`suite_dir_id`) REFERENCES `suite_dir` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of test_suite
-- ----------------------------
INSERT INTO `test_suite` VALUES (1, 'wechat', 'Test document', 0, '2023-04-05 21:04:50.598309', '2023-09-30 15:11:52.411372', '123456@163.com', '123456@163.com', NULL, 0, 9, 1);
INSERT INTO `test_suite` VALUES (2, 'alipay', NULL, 0, '2023-04-05 21:45:11.674395', '2023-04-05 21:45:11.674395', '123456@163.com', '123456@163.com', NULL, 0, 11, 1);
INSERT INTO `test_suite` VALUES (3, 'payment', NULL, 1, '2023-04-06 11:36:11.845802', '2023-04-06 11:36:11.845802', '123456@163.com', '123456@163.com', NULL, 0, 2, 1);
INSERT INTO `test_suite` VALUES (4, 'refund', NULL, 1, '2023-04-06 11:36:19.741832', '2023-04-06 11:36:19.741832', '123456@163.com', '123456@163.com', NULL, 0, 2, 1);
INSERT INTO `test_suite` VALUES (5, 'spiny', NULL, 0, '2023-04-22 16:56:23.741517', '2023-04-22 16:56:23.741517', '123456@163.com', '123456@163.com', NULL, 0, 13, 1);
INSERT INTO `test_suite` VALUES (6, 'ayden', NULL, 0, '2023-04-22 16:56:38.454290', '2023-04-22 16:56:38.454290', '123456@163.com', '123456@163.com', NULL, 0, 13, 1);
INSERT INTO `test_suite` VALUES (9, 'apcc', NULL, 0, '2023-04-25 23:45:55.395724', '2023-04-25 23:45:55.395724', '123456@163.com', '123456@163.com', NULL, 0, 14, 1);
INSERT INTO `test_suite` VALUES (16, 'change.txt', NULL, 3, '2023-05-16 09:46:58.349833', '2023-05-17 11:01:26.968905', '123456@163.com', '', NULL, 0, 16, 1);
INSERT INTO `test_suite` VALUES (18, 'color.txt', NULL, 3, '2023-05-17 11:00:42.810367', '2023-05-17 11:00:42.810367', '123456@163.com', '', NULL, 0, 16, 1);
INSERT INTO `test_suite` VALUES (19, 'icon.txt', NULL, 3, '2023-05-18 10:01:09.946501', '2023-05-18 10:01:09.946501', '123456@163.com', '', NULL, 0, 16, 1);
INSERT INTO `test_suite` VALUES (20, '发布博客.txt', NULL, 3, '2023-05-18 10:01:09.967446', '2023-05-18 10:01:09.967446', '123456@163.com', '', NULL, 0, 16, 1);
INSERT INTO `test_suite` VALUES (21, 'myvariable.py', NULL, 2, '2023-06-17 15:02:17.960308', '2023-07-09 18:37:00.882572', '123456@163.com', '123456@163.com', NULL, 0, 15, 1);
INSERT INTO `test_suite` VALUES (22, 'wechat-62294copy-965460', NULL, 0, '2023-06-28 22:24:54.189450', '2023-06-28 23:17:40.363892', '123456@163.com', '123456@163.com', NULL, 2, 11, 1);
INSERT INTO `test_suite` VALUES (23, 'TestFile.yaml', NULL, 2, '2023-09-24 13:09:06.099609', '2023-09-24 13:09:06.100621', '123456@163.com', '123456@163.com', NULL, 0, 17, 1);
INSERT INTO `test_suite` VALUES (24, 'TestJson.json', NULL, 2, '2023-09-24 14:03:29.320796', '2023-09-24 14:03:29.320796', '123456@163.com', '123456@163.com', NULL, 0, 117, 1);
INSERT INTO `test_suite` VALUES (25, 'change001.txt', NULL, 3, '2023-09-29 18:49:16.567249', '2023-09-29 22:11:26.855380', '123456@163.com', '123456@163.com', NULL, 0, 119, 1);
INSERT INTO `test_suite` VALUES (26, 'Keywords.xlsx', NULL, 3, '2023-09-30 15:39:21.415744', '2023-09-30 15:39:21.416741', '123456@163.com', '', NULL, 0, 119, 1);

-- ----------------------------
-- Table structure for user_group
-- ----------------------------
DROP TABLE IF EXISTS `user_group`;
CREATE TABLE `user_group`  (
  `department_id` int NOT NULL,
  `group_id` int NOT NULL,
  `library_path` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`group_id`) USING BTREE,
  CONSTRAINT `usergroup_usergroup_group_id_6eab3432_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_group
-- ----------------------------
INSERT INTO `user_group` VALUES (1, 1, '');
INSERT INTO `user_group` VALUES (1, 3, '');
INSERT INTO `user_group` VALUES (2, 4, '');

-- ----------------------------
-- Table structure for user_keyword
-- ----------------------------
DROP TABLE IF EXISTS `user_keyword`;
CREATE TABLE `user_keyword`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `project_id` int NOT NULL,
  `test_case_id` bigint NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_keyword_test_case_id_43769215_fk_test_case_id`(`test_case_id` ASC) USING BTREE,
  CONSTRAINT `user_keyword_test_case_id_43769215_fk_test_case_id` FOREIGN KEY (`test_case_id`) REFERENCES `test_case` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_keyword
-- ----------------------------
INSERT INTO `user_keyword` VALUES (1, 99, 'icons/keyword/user.png', 1, 6, 0);
INSERT INTO `user_keyword` VALUES (2, 99, 'icons/keyword/user.png', 1, 12, 0);

-- ----------------------------
-- Table structure for variable
-- ----------------------------
DROP TABLE IF EXISTS `variable`;
CREATE TABLE `variable`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `module_id` int NOT NULL,
  `module_type` int NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `value` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `value_type` int NOT NULL,
  `env_id` int NULL DEFAULT NULL,
  `seq_number` int NOT NULL,
  `remark` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `region_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 41 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of variable
-- ----------------------------
INSERT INTO `variable` VALUES (1, 1, 0, '${phone}', '00866660102', 0, 1, 0, 'test', 2);
INSERT INTO `variable` VALUES (2, 1, 0, '${password}', '123456', 0, 1, 0, '登录密码', 2);
INSERT INTO `variable` VALUES (3, 1, 0, '${password}', '123456', 0, 2, 0, '登录密码', 2);
INSERT INTO `variable` VALUES (4, 1, 0, '${phone}', '00866660102', 0, 2, 0, 'BR号码', 2);
INSERT INTO `variable` VALUES (5, 1, 0, '${phone}', '1889111', 0, 2, 0, '号码', 1);
INSERT INTO `variable` VALUES (6, 1, 0, '${MysqlHost}', '127.0.0.2', 0, 2, 0, '数据库地址', 0);
INSERT INTO `variable` VALUES (7, 1, 0, '${MysqlPort}', '6606', 0, 2, 0, '端口地址', 0);
INSERT INTO `variable` VALUES (8, 1, 0, '${phone}', '1889111', 0, 1, 0, '号码', 1);
INSERT INTO `variable` VALUES (11, 1, 0, '${MysqlHost}', '127.0.0.1', 0, 1, 0, '数据库本地地址', 0);
INSERT INTO `variable` VALUES (12, 1, 0, '${MysqlPort}', '6606', 0, 1, 0, '端口地址', 0);
INSERT INTO `variable` VALUES (13, 1, 0, '${phone}', '1889111', 0, 3, 0, '号码', 1);
INSERT INTO `variable` VALUES (14, 1, 0, '${password}', '123456', 0, 3, 0, '登录密码', 2);
INSERT INTO `variable` VALUES (16, 1, 0, '${phone}', '00866660102', 0, 3, 0, '', 2);
INSERT INTO `variable` VALUES (18, 1, 0, '${MysqlHost}', '127.0.0.2', 0, 3, 0, '数据库地址', 0);
INSERT INTO `variable` VALUES (19, 1, 0, '${MysqlPort}', '6606', 0, 3, 0, '端口地址', 0);
INSERT INTO `variable` VALUES (20, 1, 0, '${phone}', '1889111', 0, 4, 0, '号码', 1);
INSERT INTO `variable` VALUES (21, 1, 0, '${password}', '123456', 0, 4, 0, '登录密码', 2);
INSERT INTO `variable` VALUES (22, 1, 0, '${phone}', '00866660102', 0, 4, 0, '', 2);
INSERT INTO `variable` VALUES (23, 1, 0, '${MysqlHost}', '127.0.0.2', 0, 4, 0, '数据库地址', 0);
INSERT INTO `variable` VALUES (24, 1, 0, '${MysqlPort}', '6606', 0, 4, 0, '端口地址', 0);
INSERT INTO `variable` VALUES (25, 1, 0, '${RedisHost}', '10.0.0.1', 0, 1, 0, 'redis主机地址', 0);
INSERT INTO `variable` VALUES (26, 1, 2, '${suiteHost}', '9901', 0, NULL, 0, '特特', NULL);
INSERT INTO `variable` VALUES (27, 22, 2, '${suiteHost}', '9901', 0, NULL, 0, '', NULL);
INSERT INTO `variable` VALUES (28, 1, 0, '${password}', '147258', 0, 1, 0, '登录密码', 1);
INSERT INTO `variable` VALUES (29, 1, 2, '${suitePort}', '8088', 0, NULL, 0, '端口', NULL);
INSERT INTO `variable` VALUES (30, 1, 2, '${password}', '123456', 0, NULL, 0, '密码', NULL);
INSERT INTO `variable` VALUES (31, 1, 0, '${adyen}', '10012801', 0, 1, 0, '', 1);
INSERT INTO `variable` VALUES (32, 1, 0, '${apcc}', '10013801', 0, 1, 0, '', 1);
INSERT INTO `variable` VALUES (33, 1, 0, '${ebanx}', '10016201', 0, 1, 0, '', 1);
INSERT INTO `variable` VALUES (34, 1, 0, '${santander}', '10014800', 0, 1, 0, '', 1);
INSERT INTO `variable` VALUES (35, 1, 0, '${RedisPass}', '123456', 0, 1, 0, '', NULL);
INSERT INTO `variable` VALUES (36, 1, 0, '${RedisPort}', '10061', 0, 1, 0, '', NULL);
INSERT INTO `variable` VALUES (38, 1, 0, '${AdminDomain}', 'admin.com', 0, 1, 0, '', 1);
INSERT INTO `variable` VALUES (39, 1, 0, '${AdminDomain}', 'admin.com', 0, 1, 0, '', 1);
INSERT INTO `variable` VALUES (40, 1, 0, '${AdminDomain}', 'admin.com', 0, 1, 0, '', 1);

-- ----------------------------
-- Table structure for virtual_file
-- ----------------------------
DROP TABLE IF EXISTS `virtual_file`;
CREATE TABLE `virtual_file`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `env_id` int NULL DEFAULT NULL,
  `file_text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `suite_id` int NOT NULL,
  `remark` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `region_id` int NULL DEFAULT NULL,
  `file_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `save_mode` int NOT NULL,
  `edit_file` tinyint(1) NOT NULL,
  `status` int NOT NULL,
  `file_suffix` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `update_time` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of virtual_file
-- ----------------------------
INSERT INTO `virtual_file` VALUES (6, NULL, 'color: #3f6f9f', 16, NULL, NULL, '/SKYLARK/FILES/santander', 'change.txt', 1, 1, 0, '.txt', 0);
INSERT INTO `virtual_file` VALUES (7, NULL, '<generator object InMemoryUploadedFile.chunks at 0x0000022495721D48>', 18, NULL, NULL, '/SKYLARK/FILES/santander', 'color.txt', 2, 0, 0, '.txt', 0);
INSERT INTO `virtual_file` VALUES (8, NULL, '<generator object InMemoryUploadedFile.chunks at 0x000002249563FAC8>', 16, NULL, NULL, '/SKYLARK/FILES/santander', 'change.txt', 2, 0, 0, '.txt', 0);
INSERT INTO `virtual_file` VALUES (9, NULL, '<generator object InMemoryUploadedFile.chunks at 0x000001598970CDC8>', 19, NULL, NULL, '/SKYLARK/FILES/santander', 'icon.txt', 2, 0, 0, '.txt', 0);
INSERT INTO `virtual_file` VALUES (10, NULL, '<generator object InMemoryUploadedFile.chunks at 0x00000159898E0F48>', 20, NULL, NULL, '/SKYLARK/FILES/santander', '发布博客.txt', 2, 0, 0, '.txt', 0);
INSERT INTO `virtual_file` VALUES (11, NULL, 'def get_variables(env, region):\n    variables = {\'cur_env\': env, \'cur_region\': region}\n    return variables\n\nVARIABLE = \"An example string, not valid\"\nSTRINGS = [\"one\", \"two\", \"kolme\", \"four\"]', 21, NULL, NULL, 'SKYLARK/CONSTS/Python', 'myvariable.py', 1, 1, 0, '.py', 1696058874);
INSERT INTO `virtual_file` VALUES (12, NULL, '{\"host\":\"127.0.0.1\",\"post\":6606}', 24, NULL, NULL, 'SKYLARK/CONSTS/Json', 'TestJson.json', 1, 1, 0, '.json', 1695552535);
INSERT INTO `virtual_file` VALUES (13, NULL, 'account:\n  username: vuer\n  password: 123456', 23, NULL, NULL, 'SKYLARK/CONSTS/Yaml', 'TestFile.yaml', 1, 1, 0, '.yaml', 1695552547);
INSERT INTO `virtual_file` VALUES (14, NULL, NULL, 25, NULL, NULL, 'SKYLARK/PROFILES/HelpFiles', 'change001.txt', 2, 0, 0, '.txt', 1695984556);
INSERT INTO `virtual_file` VALUES (15, NULL, NULL, 26, NULL, NULL, 'SKYLARK/PROFILES/HelpFiles', 'Keywords.xlsx', 2, 0, 0, '.xlsx', 1696059561);

SET FOREIGN_KEY_CHECKS = 1;
