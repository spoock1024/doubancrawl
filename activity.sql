/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50626
Source Host           : localhost:3306
Source Database       : douban

Target Server Type    : MYSQL
Target Server Version : 50626
File Encoding         : 65001

Date: 2016-05-10 00:10:30
*/

CREATE Database douban CHARACTER set utf8 COLLATE utf8_general_ci;
use douban;
grant all privileges on douban.* to whu@localhost identified by "123456";

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for activity
-- ----------------------------
DROP TABLE IF EXISTS `activity`;
CREATE TABLE `activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `eventid` int(11) DEFAULT NULL COMMENT '豆瓣id',
  `title` varchar(255) DEFAULT NULL COMMENT '活动名称',
  `activitytime` varchar(255) DEFAULT NULL COMMENT '活动时间',
  `location` varchar(255) DEFAULT NULL COMMENT ' 地点',
  `cost` varchar(255) DEFAULT NULL COMMENT '花费',
  `info` text COMMENT '花费',
  `activitytype` varchar(255) DEFAULT '' COMMENT '活动类型',
  `interestedpersonnum` int(11) DEFAULT NULL COMMENT '对活动感兴趣人的数量',
  `interestedrate` text COMMENT '城市所占的比例',
  `participatepersonnum` text COMMENT '参加活动的数量',
  `participaterate` text COMMENT '城市所占的比例',
  `organizationname` text COMMENT '发起人名称',
  `organizationid` int(11) DEFAULT NULL COMMENT '发起人的豆瓣id',
  `organizationurl` varchar(255) DEFAULT NULL COMMENT '发起人豆瓣地址',
  `organizationtype` varchar(20) DEFAULT NULL COMMENT '发起人类型(person,site)',
  `attendnum` int(11) DEFAULT NULL COMMENT '发起人要参加的活动数量',
  `wishnum` int(11) DEFAULT NULL COMMENT '发起人感兴趣的活动数量',
  `ownednum` int(11) NOT NULL COMMENT '发起人发起活动的数量',
  `groupsnum` int(11) DEFAULT NULL COMMENT '发起人参加小组的数量',
  `groupsnames` varchar(255) DEFAULT NULL COMMENT '发起人参加的小组的名称',
  `followersnum` int(11) DEFAULT NULL COMMENT '关注小站的人的数量，只有当type为site的时候才有值',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=955 DEFAULT CHARSET=utf8;