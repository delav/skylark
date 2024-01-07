
-- ----------------------------
-- Records of auth_group
-- ----------------------------
INSERT INTO `auth_group` VALUES (1, 'Team01');
INSERT INTO `auth_group` VALUES (2, 'Team02');
INSERT INTO `auth_group` VALUES (3, 'Team03');

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$260000$26iWhmWPhSS9JGwyEhbMH0$oTTYkSXSSEMsOQjnKF7Z+Xx9ZUk4E9OmLAIMh6fj8V4=', '2023-12-26 13:38:52.917057', 1, 'Admin', '', '', 'admin@163.com', 1, 1, '2022-07-06 23:04:45.230926');
INSERT INTO `auth_user` VALUES (2, 'pbkdf2_sha256$260000$m4wMTY4EN1gp4w7aKHmuyu$rinPImw3S9CVUAy7H7EIopTpp7K7RKxcvj3it0mw3Qs=', '2023-12-26 13:37:39.214525', 0, 'Test', '', '', '123456@163.com', 0, 1, '2022-08-26 17:06:01.379613');

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------
INSERT INTO `auth_user_groups` VALUES (1, 2, 1);

-- ----------------------------
-- Records of case_priority
-- ----------------------------
INSERT INTO `case_priority` VALUES (1, 'P0');
INSERT INTO `case_priority` VALUES (2, 'P1');
INSERT INTO `case_priority` VALUES (3, 'P2');
INSERT INTO `case_priority` VALUES (4, 'P3');

-- ----------------------------
-- Records of department
-- ----------------------------
INSERT INTO `department` VALUES (1, 'Department1');
INSERT INTO `department` VALUES (2, 'Department2');

-- ----------------------------
-- Records of environment
-- ----------------------------
INSERT INTO `environment` VALUES (1, 'DEV', '开发环境', 0);
INSERT INTO `environment` VALUES (2, 'TEST', '测试环境', 0);
INSERT INTO `environment` VALUES (3, 'UAT', '验收环境', 0);
INSERT INTO `environment` VALUES (4, 'STAGING', '回归环境', 0);

-- ----------------------------
-- Records of keyword_group
-- ----------------------------
INSERT INTO `keyword_group` VALUES (1, '平台组件', 2, NULL, NULL);
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
INSERT INTO `keyword_group` VALUES (98, '项目1类', 1, 1, 1);
INSERT INTO `keyword_group` VALUES (100, '团队1类', 1, NULL, 1);

-- ----------------------------
-- Records of lib_keyword
-- ----------------------------
INSERT INTO `lib_keyword` VALUES (1, 'comment', '2022-08-07 22:34:38.000000', '2022-08-09 22:34:56.000000', 'admin@163.com', 'admin@163.com', '注释', '为流程备注说明', 18, 'any', '注释说明', NULL, NULL, 1, 0, 1, 'icons/keyword/comment.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (2, 'log', '2022-08-07 21:42:10.422564', '2022-08-09 22:33:02.095732', 'admin@163.com', 'admin@163.com', '打印输出', '打印信息到日志中', 18, 'any', '打印的变量', '', '', 1, 0, 1, 'icons/keyword/log.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (4, 'set_variable', '2022-08-11 22:24:42.761485', '2022-08-11 22:24:42.761485', 'admin@163.com', 'admin@163.com', '设置变量', '设置一个自定义变量', 3, 'any', '任意参数', '${out}', '变量名称', 1, 1, 1, 'icons/keyword/should_be_equal.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (5, 'should_be_equal', '2022-08-11 22:26:15.201615', '2022-08-11 22:26:15.201615', 'admin@163.com', 'admin@163.com', '应该相等', '比较两个变量值是否相等', 4, 'value1|value2', '参数1|参数2', '', '', 1, 0, 1, 'icons/keyword/set_variable.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (6, 'create_list', '2022-08-11 22:27:00.666799', '2022-08-11 22:27:00.666799', 'admin@163.com', 'admin@163.com', '创建列表', '创建一个列表', 6, '', '列表元素', '${out}', '参数列表', 2, 1, 1, 'icons/keyword/create_list.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (7, 'sleep', '2022-08-11 22:07:35.000000', '2023-02-17 22:07:48.000000', 'admin@163.com', 'admin@163.com', '等待时间', '等待时间，单位为妙', 8, 'time', '等待的时长(s)', NULL, NULL, 1, 0, 1, 'icons/keyword/sleep.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (8, 'connect_mysql', '2022-08-11 22:26:15.201615', '2022-08-11 22:26:15.201615', 'admin@163.com', 'admin@163.com', '连接原创MySQL数据库', '连接MySQL数据库', 9, 'host|port', 'mysql主机地址|端口', '', '', 1, 0, 1, 'icons/keyword/connect_mysql.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (9, 'create_dictionary', '2022-08-11 23:29:57.000000', '2022-08-11 23:30:17.000000', 'admin@163.com', 'admin@163.com', '创建字典', '创建一个字典', 7, '', '字典键值对', '${out}', '参数字典', 3, 1, 1, 'icons/keyword/create_dictionary.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (10, 'create_timestamp', '2023-06-26 18:48:17.000000', '2023-06-26 18:48:36.000000', 'admin@163.com', 'admin@163.com', '获取时间戳', '获取当前时间戳', 8, NULL, NULL, '${out}', '当前时间戳', 0, 1, 1, 'icons/keyword/create_timestamp.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (102, 'for', '2023-08-26 11:16:35.459753', '2023-08-26 11:16:35.459753', 'admin@163.com', 'admin@163.com', 'For', '遍历一个可迭代对象，如列表、字典。必须配合使用[END]组件结束循环', 2, '', '', '', '', 2, 0, 0, 'icons/keyword/for.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (103, 'end', '2023-08-26 11:23:52.737554', '2023-08-26 11:23:52.737554', 'admin@163.com', 'admin@163.com', 'End', '用于和其他流程控制组件配合使用', 2, '', '', '', '', 0, 0, 0, 'icons/keyword/end.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (104, 'if', '2023-08-26 11:25:16.916290', '2023-08-26 11:25:16.916290', 'admin@163.com', 'admin@163.com', 'If', '通过条件判断，控制执行逻辑。必须配合使用[END]组件结束判断', 2, 'condition', '条件语句', '', '', 1, 0, 0, 'icons/keyword/if.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (105, 'else_if', '2023-08-26 11:26:04.681013', '2023-08-26 11:26:04.681013', 'admin@163.com', 'admin@163.com', 'Else If', '与[IF]组件相似，允许多个分支条件判断，必须与[IF]组件配合使用', 2, 'condition', '条件语句', '', '', 1, 0, 0, 'icons/keyword/else_if.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (106, 'else', '2023-08-26 11:26:26.617096', '2023-08-26 11:26:26.617096', 'admin@163.com', 'admin@163.com', 'Else', '执行不满足[If]/[Else If]的其他逻辑，必须与[IF]组件配合使用', 2, '', '', '', '', 0, 0, 0, 'icons/keyword/else.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (110, 'while', '2023-08-26 11:27:57.308400', '2023-08-26 11:27:57.308400', 'admin@163.com', 'admin@163.com', 'While', '', 2, 'condition', '条件语句', '', '', 1, 0, 0, 'icons/keyword/while.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (111, 'continue', '2023-08-26 11:28:23.999387', '2023-08-26 11:28:23.999387', 'admin@163.com', 'admin@163.com', 'Continue', '', 2, '', '', '', '', 0, 0, 0, 'icons/keyword/continue.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (112, 'break', '2023-08-26 11:28:41.110446', '2023-08-26 11:28:41.111444', 'admin@163.com', 'admin@163.com', 'Break', '', 2, '', '', '', '', 0, 0, 0, 'icons/keyword/break.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (113, 'return', '2023-08-26 11:28:59.964957', '2023-08-26 11:28:59.964957', 'admin@163.com', 'admin@163.com', 'Return', '', 2, 'result', '返回值', '', '', 1, 0, 0, 'icons/keyword/return.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (117, 'http_post', '2023-10-29 16:48:06.831750', '2023-10-29 16:48:06.831750', 'admin@163.com', 'admin@163.com', '发送POST请求', '发送http post请求', 10, 'url|data|header', '请求地址|请求数据|请求头', '${response}', '请求json响应', 1, 1, 3, 'icons/keyword/http_post.png', 0, 20, NULL);
INSERT INTO `lib_keyword` VALUES (118, 'http_get', '2023-11-05 00:04:37.000000', '2023-11-05 00:04:43.000000', 'admin@163.com', 'admin@163.com', '发送GET请求', '发送http get 请求', 10, 'url|header', '请求地址|请求头', '${response}', '请求响应文本数据', 1, 1, 3, 'icons/keyword/http_get.png', 0, 20, NULL);
INSERT INTO `lib_keyword` VALUES (119, 'team1_post01', '2023-11-06 11:22:16.843034', '2023-12-20 12:26:22.292957', 'admin@163.com', 'admin@163.com', 'Team1 Post请求', '发送http post请求。', 98, 'url|headers|*args|**kwargs', '请求地址|请求头', '${response}', '请求json响应。', 4, 1, 3, 'icons/keyword/team1_post01.png', 0, 30, NULL);
INSERT INTO `lib_keyword` VALUES (121, 'set_global_variable', '2023-12-03 16:14:25.506164', '2023-12-03 16:14:25.506164', 'delavpeng@163.com', 'delavpeng@163.com', '设置全局变量', '', 3, 'name|value', '变量名|变量值', NULL, '', 1, 0, 1, 'icons/keyword/set_global_variable.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (122, 'set_suite_variable', '2023-12-03 16:16:27.083363', '2023-12-03 16:16:27.083363', 'delavpeng@163.com', 'delavpeng@163.com', '设置套件变量', '', 3, 'name|value', '变量名|变量值', NULL, '', 1, 0, 1, 'icons/keyword/set_suite_variable.png', 0, 0, NULL);
INSERT INTO `lib_keyword` VALUES (123, 'set_variable_if', '2023-12-03 16:48:08.683644', '2023-12-03 16:48:08.683644', 'delavpeng@163.com', 'delavpeng@163.com', '条件设置变量', '', 3, 'condition|value1|value2', '条件|条件成立的值|条件不成立的值', '${out}', '', 1, 1, 1, 'icons/keyword/set_variable_if.png', 0, 0, NULL);


-- ----------------------------
-- Records of project
-- ----------------------------
INSERT INTO `project` VALUES (1, 'SKYLARK', '2022-08-18 23:16:32.915535', '2022-08-18 23:16:32.915535', 'admin@163.com', 'admin@163.com', 1, 0, 1);


-- ----------------------------
-- Records of python_lib
-- ----------------------------
INSERT INTO `python_lib` VALUES (1, 'BuiltIn', 0, 'BuiltIn', '', NULL);
INSERT INTO `python_lib` VALUES (2, 'HttpClient', 2, 'Public', '', NULL);
INSERT INTO `python_lib` VALUES (3, 'TestLibrary01', 2, 'Team01', '', 1);
INSERT INTO `python_lib` VALUES (4, 'TestLibrary02', 2, 'Team01', '', 1);

-- ----------------------------
-- Records of region
-- ----------------------------
INSERT INTO `region` VALUES (1, 'US', '美国', 0);
INSERT INTO `region` VALUES (2, 'UK', '英国', 0);
INSERT INTO `region` VALUES (3, 'CN', '中国', 0);

-- ----------------------------
-- Records of suite_dir
-- ----------------------------
INSERT INTO `suite_dir` VALUES (1, 'CASES', '存放测试用例的目录', 0, '2023-04-01 19:15:22.000000', '2023-04-05 19:15:16.000000', 'admin@163.com', 'admin@163.com', 1, NULL, 0);
INSERT INTO `suite_dir` VALUES (2, 'COMPS', '存放用户自定义高级组件的目录', 1, '2023-04-01 19:15:22.000000', '2023-04-05 19:15:16.000000', 'admin@163.com', 'admin@163.com', 1, NULL, 0);
INSERT INTO `suite_dir` VALUES (3, 'CONST', '存放项目公共常量的目录，支持python， yaml格式', 2, '2023-04-01 19:15:22.000000', '2023-04-05 19:15:16.000000', 'admin@163.com', 'admin@163.com', 1, NULL, 0);
INSERT INTO `suite_dir` VALUES (4, 'PROJFS', '存放项目需要的额外文件的目录', 3, '2023-04-01 19:15:22.000000', '2023-04-05 19:15:16.000000', 'admin@163.com', 'admin@163.com', 1, NULL, 0);


-- ----------------------------
-- Records of user_group
-- ----------------------------
INSERT INTO `user_group` VALUES (1, 1, 'Team01');
INSERT INTO `user_group` VALUES (1, 2, 'Team02');
INSERT INTO `user_group` VALUES (2, 3, 'Team03');

