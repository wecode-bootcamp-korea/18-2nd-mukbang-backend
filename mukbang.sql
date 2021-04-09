-- MySQL dump 10.13  Distrib 8.0.23, for Linux (x86_64)
--
-- Host: localhost    Database: mukbang
-- ------------------------------------------------------
-- Server version	8.0.23-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `addresses`
--

DROP TABLE IF EXISTS `addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `latitude` decimal(25,22) NOT NULL,
  `longitude` decimal(25,22) NOT NULL,
  `full_address` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `region_1depth_name` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `region_2depth_name` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `region_3depth_name` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `road_name` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `building_name` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `store_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `store_id` (`store_id`),
  CONSTRAINT `addresses_store_id_568dae69_fk_stores_id` FOREIGN KEY (`store_id`) REFERENCES `stores` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
INSERT INTO `addresses` VALUES (32,37.4918939171295000000000,127.0321665617870000000000,'서울 강남구 강남대로66길 16','서울','강남구','역삼동','강남대로66길','',53),(38,37.3978378487211000000000,127.1291902115010000000000,'경기 성남시 분당구 방아로 2','경기','성남시 분당구','이매동','방아로','',69),(69,37.5071236207170000000000,127.0560613612410000000000,'서울 강남구 테헤란로 447','서울','강남구','삼성동','테헤란로','KB우준타워',112),(70,37.5110163357276000000000,127.0539006635530000000000,'서울 강남구 삼성로 555','서울','강남구','삼성동','삼성로','',113),(75,37.5015738831593000000000,127.0506652120910000000000,'서울 강남구 선릉로 410','서울','강남구','대치동','선릉로','문화문고',118),(77,37.5021276273398000000000,127.0583134880070000000000,'서울 강남구 삼성로71길 7','서울','강남구','대치동','삼성로71길','',120),(78,37.5056023729557000000000,127.0491627123280000000000,'서울 강남구 선릉로 514','서울','강남구','삼성동','선릉로','성원타워',121),(79,37.5031995277517000000000,127.0520011642030000000000,'서울 강남구 역삼로65길 31','서울','강남구','대치동','역삼로65길','',122),(80,37.5031717841689000000000,127.0479366455350000000000,'서울 강남구 테헤란로52길 15','서울','강남구','역삼동','테헤란로52길','금천빌딩',123),(81,37.5088926840394000000000,127.0438448431160000000000,'서울 강남구 선릉로107길 3-4','서울','강남구','역삼동','선릉로107길','',124),(82,37.5049885992418000000000,127.0467432752160000000000,'서울 강남구 선릉로93길 22','서울','강남구','역삼동','선릉로93길','',125),(83,37.5045993053356000000000,127.0561864810520000000000,'서울 강남구 삼성로85길 11','서울','강남구','대치동','삼성로85길','롯데캐슬아파트',126),(84,37.5003911830955000000000,127.0522050407500000000000,'서울 강남구 선릉로72길 13','서울','강남구','대치동','선릉로72길','',127),(85,37.5058587174282000000000,127.0471527817120000000000,'서울 강남구 테헤란로55길 20','서울','강남구','역삼동','테헤란로55길','',128),(86,37.5058149679709000000000,127.0561309560280000000000,'서울 강남구 테헤란로 440','서울','강남구','대치동','테헤란로','포스코센터',129),(87,37.5089551867803000000000,127.0568083067190000000000,'서울 강남구 삼성로96길 11','서울','강남구','삼성동','삼성로96길','',130),(88,37.5126194372996000000000,127.0555752587980000000000,'서울 강남구 봉은사로84길 10','서울','강남구','삼성동','봉은사로84길','',131),(90,37.5103568492690000000000,127.0610237829310000000000,'서울 강남구 영동대로 511','서울','강남구','삼성동','영동대로','트레이드타워',133);
/*!40000 ALTER TABLE `addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (14,'베이커리'),(17,'분식'),(23,'양식'),(20,'일식'),(24,'주점'),(21,'중식'),(18,'치킨'),(13,'카페'),(16,'패스트푸드'),(22,'퓨전'),(1,'한식');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'contenttypes','contenttype'),(2,'sessions','session'),(12,'store','address'),(6,'store','category'),(13,'store','menu'),(7,'store','metrostation'),(11,'store','metrostationstore'),(8,'store','openstatus'),(9,'store','store'),(10,'store','storeimage'),(4,'user','review'),(3,'user','user'),(5,'user','wishlist');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-03-29 20:26:38.738691'),(2,'contenttypes','0002_remove_content_type_name','2021-03-29 20:26:38.922900'),(3,'sessions','0001_initial','2021-03-29 20:26:38.984238'),(4,'store','0001_initial','2021-03-31 18:17:25.965449'),(5,'user','0001_initial','2021-03-31 18:17:27.141107'),(6,'store','0002_auto_20210331_1818','2021-03-31 18:19:58.048810'),(7,'store','0003_auto_20210401_1729','2021-04-01 17:29:37.118313'),(8,'user','0002_auto_20210404_0013','2021-04-04 00:16:07.842257');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menus`
--

DROP TABLE IF EXISTS `menus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menus` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `menu_image_url` varchar(3000) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `store_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `menus_store_id_name_f282416a_uniq` (`store_id`,`name`),
  CONSTRAINT `menus_store_id_1cb53450_fk_stores_id` FOREIGN KEY (`store_id`) REFERENCES `stores` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menus`
--

LOCK TABLES `menus` WRITE;
/*!40000 ALTER TABLE `menus` DISABLE KEYS */;
INSERT INTO `menus` VALUES (26,'시래기 국밥',8000.00,'https://s3-ap-northeast-1.amazonaws.com/dcreviewsresized/20200206030137603_photo_EnjdtHHZ6jYx.jpg',53),(27,'수육',13000.00,'https://d2t7cq5f1ua57i.cloudfront.net/images/r_images/54372/58486/54372_58486_89_0_9602_2016112213118580.jpg',53),(28,'아메리카노',3000.00,'https://file2.nocutnews.co.kr/newsroom/image/2018/03/15/20180315163346993745_0_763_677.jpg',69),(93,'점심뷔페',7500.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20201105_176%2F1604580150994XqpMN_JPEG%2FnUnNgoYBBGcVu5c18yqJUjny.jpg',112),(94,'설렁탕',12000.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20200722_84%2F1595406944444HYg4f_JPEG%2Fupload_9cac6c3904a0dcd08ff90596db43da7d.jpg',113),(95,'수육(대)',70000.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20190711_92%2F1562803484944xucEt_JPEG%2F98956547-a79f-4150-a17c-a66e41dfa4fa.jpeg',113),(96,'마레빠네',14900.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20210316_3%2F1615875588349Xezqi_JPEG%2Fupload_ca8998bbdf813ac17f28f6543e1b17f7.jpeg',118),(97,'마레크림 스파케티',12900.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20210316_118%2F16158755884564pysm_JPEG%2Fupload_f9708bca7432af2f1df878e756d07626.jpeg',118),(98,'차돌박이 파스타',13900.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fnaverbooking-phinf.pstatic.net%2F20210304_71%2F1614835526147d0yKN_JPEG%2Fimage.jpg',118),(100,'병어(회,무침,조림)',50000.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxOTA5MjJfMjIw%2FMDAxNTY5MTA5NjQ2MzUz.5Cqxd9x9KFCe-FlNT64Skw_MfI2SSHzUwM-YEKoKGp0g.vGh2dPAkxs3v5z0L6473ATd-ZNlriH-WcT2IdO3qBLog.JPEG.moondiya1%2F20190908_210216.jpg',120),(101,'[치밥 No.1] 앵그리 바베큐 치밥',8900.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTAxMjFfMjg4%2FMDAxNjExMjA5NTY3OTA0.2WftUTr5swYw-gzRiZ3kif65_OO7x42K32MKLtnmEAAg.rIM4zjbETUvdtvIJ38-Gv2UkSSpcQEA3TKD-sAiiSWcg.JPEG.53ejej9924%2F%25BE%25DE%25B1%25D7%25B8%25AE%25C4%25A1%25B9%25E4_4.jpg',121),(102,'[BEST] 깐풍 치밥',9500.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20210406_99%2F1617673702103BHpnj_JPEG%2FJ6cZpM4lBVrfHSTvm0lK35q_aCoTOoHjf0i5j0uLUA0%253D.jpg&type=h166',121),(103,'[BEST] 앵그리 김치 치밥',9500.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20210406_136%2F1617667959689wgOmt_JPEG%2F_MWFP3ZhGiLk19TAO-DJV7ciW5Ckylf1uXLTGNcc4ts%253D.jpg&type=h166',121),(104,'슈프림 양념 치밥',8900.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20210406_65%2F1617667919648Mpu0y_JPEG%2FFeqy7Xskk0LxyU8_XDw2TqgwQ3mCCpoGfpU4JWeZnSc%253D.jpg&type=h166',121),(105,'모듬족발(중)',36000.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTAxMTZfMjkg%2FMDAxNjEwNzU1Mjc4MTA2.16eMEJ0wTpOXOKMiRd01lR87RLfd7l4kYDvaNdR6lxEg.vn8M_G_DRWDlJtVCCB6wriMAr8uyB9RZK7EUIaReOZ0g.JPEG.yjhooon%2FIMG_0627.jpg',122),(106,'진풍정B',55000.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20180831_210%2F1535677233869Oyb2O_JPEG%2FNk6HFJKUpF1R20K_BBFFE87z.jpg',123),(107,'디너 스시오마카세',90000.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20200907_183%2F1599475449906LEjMu_JPEG%2Fupload_16fafd431c44359396d4dee9ccdfbe2b.jpeg',124),(108,'런치',45000.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20201107_274%2F1604737762260PCexa_JPEG%2Fupload_1d3da7f8f2cb9b7d7dea4ad4a4c2b2e8.jpeg',124),(109,'금계찜닭 (2인)',22000.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTAxMjBfMTEw%2FMDAxNjExMTUyMDA2NTky.hrACIsbyLLqgwYRcp-ycgPd8meurcS_O562MpPxMJA8g.iLIRLdfEKwlBJxh4AqVKohOz9-_B-DanJspwUAQwQAUg.JPEG.shopid0%2FKakaoTalk_20210120_230328993_11.jpg',125),(110,'참치김밥',4300.00,'https://ldb-phinf.pstatic.net/20190522_293/15584847762437QPps_JPEG/sGk7wWJE7VOrrzAd9pwNTw%3D%3D.jpg',126),(111,'마녀김밥',3500.00,'https://ldb-phinf.pstatic.net/20190522_75/1558484776230z9a8E_JPEG/fyrIIfyY1a1X5mMI4LSWOg%3D%3D.jpg',126),(112,'마녀떡볶이',5500.00,'https://ldb-phinf.pstatic.net/20190522_118/15584847766377lMao_JPEG/FFFnjTXPUkxOZftzeAJeag%3D%3D.jpg',126),(113,'멸치김밥',3900.00,'https://ldb-phinf.pstatic.net/20190522_216/1558484776256Xm8Hr_JPEG/Bf995X9l-TNEr4HYcZiITg%3D%3D.jpg',126),(114,'맥앤치즈',2500.00,'https://ldb-phinf.pstatic.net/20200225_70/1582562723906f49rz_PNG/j4NhTrCfzxgJqfViG4c4pxgB.png',127),(115,'레오버거',9900.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20210206_27%2F1612546399289sANcH_JPEG%2Fupload_309d4c86d948a37cabfd1cac286c24db.jpeg',127),(116,'마니크커리',9500.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20210126_22%2F1611639569039PHcK1_JPEG%2FAI-11HzWzDdlHXz-gC0K4xaUrbZfGuQKxvHVGkg3z7FKIpdwg2brI6aQuJDOMNEW.jpg&type=h166',128),(117,'런치 오마카세',50000.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20210406_188%2F1617688477592uaqJr_JPEG%2Fupload_4c04f3e0b950dc0a8fec2093823da3eb.jpg',130),(118,'브루클린 웍스',9800.00,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20210112_115%2F1610462445962kolU8_JPEG%2Fupload_9f1a5d75a422fa13a161d39c9b5d7170.jpeg',131);
/*!40000 ALTER TABLE `menus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metro_stations`
--

DROP TABLE IF EXISTS `metro_stations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metro_stations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `line` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `latitude` decimal(25,22) NOT NULL,
  `longitude` decimal(25,22) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `metro_stations_name_line_97ee9c3f_uniq` (`name`,`line`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metro_stations`
--

LOCK TABLES `metro_stations` WRITE;
/*!40000 ALTER TABLE `metro_stations` DISABLE KEYS */;
INSERT INTO `metro_stations` VALUES (7,'선릉역','2호선',37.5045000000000000000000,127.0490000000000000000000),(8,'강남역','2호선',37.4980854357918005348438,127.0280002750709940073648),(9,'삼성중앙역','9호선',37.5129614511319000000000,127.0530436769120000000000),(10,'선정릉역','수인분당선',37.5100010680032600000000,127.0434435173202600000000),(11,'한티역','수인분당선',37.4962857047653000000000,127.0529097494170000000000),(12,'삼성역','2호선',37.5088227390184000000000,127.0630254735330000000000),(13,'봉은사역','9호선',37.5142554489848000000000,127.0602339351140000000000);
/*!40000 ALTER TABLE `metro_stations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metro_stations_stores`
--

DROP TABLE IF EXISTS `metro_stations_stores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metro_stations_stores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `metro_station_id` int NOT NULL,
  `store_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `metro_stations_store_metro_station_id_fc0fc70d_fk_metro_sta` (`metro_station_id`),
  KEY `metro_stations_stores_store_id_99d899f2_fk_stores_id` (`store_id`),
  CONSTRAINT `metro_stations_store_metro_station_id_fc0fc70d_fk_metro_sta` FOREIGN KEY (`metro_station_id`) REFERENCES `metro_stations` (`id`),
  CONSTRAINT `metro_stations_stores_store_id_99d899f2_fk_stores_id` FOREIGN KEY (`store_id`) REFERENCES `stores` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metro_stations_stores`
--

LOCK TABLES `metro_stations_stores` WRITE;
/*!40000 ALTER TABLE `metro_stations_stores` DISABLE KEYS */;
INSERT INTO `metro_stations_stores` VALUES (12,7,53),(13,7,69),(14,8,53),(39,7,112),(40,9,113),(41,7,118),(42,7,120),(43,7,121),(44,7,122),(45,7,123),(46,10,124),(47,7,125),(48,7,126),(49,11,127),(50,7,128),(51,12,129),(52,12,130),(53,9,131),(54,13,133);
/*!40000 ALTER TABLE `metro_stations_stores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `open_status`
--

DROP TABLE IF EXISTS `open_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `open_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `status_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `open_status`
--

LOCK TABLES `open_status` WRITE;
/*!40000 ALTER TABLE `open_status` DISABLE KEYS */;
INSERT INTO `open_status` VALUES (1,'브레이크타임'),(5,'영업종료'),(2,'오픈중');
/*!40000 ALTER TABLE `open_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rating` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `content` varchar(500) COLLATE utf8mb4_general_ci NOT NULL,
  `image_url` varchar(3000) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `store_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reviews_store_id_f131ac74_fk_stores_id` (`store_id`),
  KEY `reviews_user_id_c23b0903_fk_users_id` (`user_id`),
  CONSTRAINT `reviews_store_id_f131ac74_fk_stores_id` FOREIGN KEY (`store_id`) REFERENCES `stores` (`id`),
  CONSTRAINT `reviews_user_id_c23b0903_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,'4.5','정말 맛있어요! 또올래요','http://travel.chosun.com/site/data/img_dir/2011/07/11/2011071101128_0.jpg','2021-04-04 00:08:02.064674','2021-04-04 00:08:02.064729',53,1),(3,'1','윽! 노맛.. 다신안온다','https://ww.namu.la/s/3ebae1aff6bd278d6f171970e0ecff8ce9f2c5a6798b1acfebd6bd9d9ff252b3e01c181f79458d667d8fb39f2ba0122ab8ae19ee1c3b644d08750ddc3ba9652329c3efc04e74c9d969513bd12f10180800f934e491f0e53184437cb2bf539c80610175b4d24f8caf1429dcb014d811c8','2021-04-04 19:05:05.608824','2021-04-04 19:05:05.608847',53,1),(4,'4.5','또 오고싶은 집','http://m.glambra.co.kr/web/img/home/promotion_starbucks.jpg','2021-04-06 20:17:53.827955','2021-04-06 20:17:53.828027',69,1),(12,'4.5','또 오고싶은 집','http://m.glambra.co.kr/web/img/home/promotion_starbucks.jpg','2021-04-07 14:47:11.404657','2021-04-07 14:47:11.404982',69,2),(16,'3.5','하하하',NULL,'2021-04-08 16:46:48.406740','2021-04-08 16:46:48.406776',53,2);
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_images`
--

DROP TABLE IF EXISTS `store_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `image_url` varchar(3000) COLLATE utf8mb4_general_ci NOT NULL,
  `store_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_images_store_id_801e3033_fk_stores_id` (`store_id`),
  CONSTRAINT `store_images_store_id_801e3033_fk_stores_id` FOREIGN KEY (`store_id`) REFERENCES `stores` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=308 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_images`
--

LOCK TABLES `store_images` WRITE;
/*!40000 ALTER TABLE `store_images` DISABLE KEYS */;
INSERT INTO `store_images` VALUES (135,'https://steemitimages.com/DQmf9fgCzGWsqj1gcoP9Z8YDCKykDGi1KRdanrZAdQtFLVE/20180221_190332.jpg',53),(136,'https://s3-ap-northeast-1.amazonaws.com/dcreviewsresized/20200712094922_photo1_68d1c5bf458f.jpg',53),(137,'https://s3-ap-northeast-1.amazonaws.com/dcreviewsresized/20200712094922_photo3_68d1c5bf458f.jpg',53),(153,'https://file2.nocutnews.co.kr/newsroom/image/2018/03/15/20180315163346993745_0_763_677.jpg',69),(154,'https://file2.nocutnews.co.kr/newsroom/image/2018/03/15/20180315163346993745_0_763_677.jpg',69),(155,'https://file2.nocutnews.co.kr/newsroom/image/2018/03/15/20180315163346993745_0_763_677.jpg',69),(249,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMDExMDNfMzUg%2FMDAxNjA0Mzc5MDg5NTQ2.GdB1fjDp3Gcf3CwUh9mKxAOsrcYk4_YOdpRMuaRzel4g.EDk1OcICpbZbKABJcrwf77LPD07u92ApA3MiwzDErDog.JPEG.rosa8769%2F1604378925341.jpg',112),(250,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMDExMjdfMTY5%2FMDAxNjA2NDUxNjc3NTk2.ifuoQ-2QwKibc-7klMM9hQuhB43nOmshc3EBU5Xhhskg.oCk_5ECieAcTmaUJfUJNoVLaMvj27SyDgutJcqGzQX4g.JPEG.rhaehf2006%2FIMG_2973.JPG',112),(251,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20201105_216%2F1604579964930WTu47_JPEG%2F8NGeyXsb0jsZP_neN7h7oXiz.jpg',112),(252,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20200810_92%2F1597050668790esJ9A_JPEG%2Fupload_703351733b3dc358e4660a158252adb3.jpg',113),(253,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20190825_129%2F1566708636564heiBX_JPEG%2Fupload_3fafdce2082dd0405c78efe51ef743f4.jpg',113),(254,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20200722_76%2F1595406944395fKuEg_JPEG%2Fupload_342b90f7b4a46b2820e83b561ac3d807.jpg',113),(263,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTAyMTVfMTE4%2FMDAxNjEzMzc4Njc2MzQ4.nQs9cAe_KrBv40xrv8oRVB68ltQMCdezKp7I51xulvYg.KTBlIJH9HnzGv2pD7HzcehvG4TYg2HpOnc0EP4fkkUEg.JPEG.dhrdpdnjs12%2FIMG_6986.jpg',118),(264,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMDExMDNfMjM4%2FMDAxNjA0NDA0NDI2OTUz.kOdfVNmfYISUdYE5oltKQR0tpAm7EKWK6NeXdM-giOcg.DSc4R9WTIkIZIIdbZB_Rc7YMBojn_h5ST8fkfjG-LY0g.JPEG.celine_an%2FIMG_3733.jpg',118),(265,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTAxMThfMjAg%2FMDAxNjEwOTc3MjU1Mzc2.DbqzLCrqZ0F0jOJ4kExLzOBQfMs1uoe0eXMNWxi5baQg.O_-nQmUW5rcHWvzroeqgKZx-eeGK25bnyO3MGPudfmIg.JPEG.kidtjdwns9498%2FKakaoTalk_20210118_222435409.jpg',118),(269,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20150901_144%2F1441050607769Y45iG_JPEG%2F156155408630759_0.jpg',120),(270,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20150901_41%2F14410506079510tAxo_JPEG%2F156155408630759_1.jpg',120),(271,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20150901_32%2F1441050608124tbt26_JPEG%2F156155408630759_2.jpg',120),(272,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTAyMDRfMjMw%2FMDAxNjEyNDQ3NTcwOTM4.pWL6N9Qn64s4tbeEgqI9sNUWTmT5QLGGtU81Ph363acg.s5YXaghbs2vcE2j2Xe99kXMjxOFsRTbRlkHxk9g910Yg.JPEG.cattycat1%2F%25BC%25B1%25B8%25AA%25BF%25AA_%25B8%25C0%25C1%25FD8.jpg',121),(273,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTAyMjRfMjY3%2FMDAxNjE0MTU1NTA5ODg0.ZlqPUEAkH_YL9krQobbFyVCnqej8J7kIRH2CAmXC2aQg.aS4QJGRRiz0iN6GjMNgVOo6IKFEjBf-mE4P-9sssp9Ig.JPEG.1000dmsrud%2F20210216%25A3%25DF185905.jpg',121),(274,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTAyMDZfMjMz%2FMDAxNjEyNTM5NzE0OTM3.U6biZXGeF_fxh_KveeKjpjYqzulYSj9KBFPbqB32u9Ug.kDBXJkDosWMDBFUYLa3MMw1lJnU4tp2vHlkkUK4S_wMg.JPEG.jdaeun96%2FIMG_7450.JPG',121),(275,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20161209_112%2F14812144599157O5dV_JPEG%2F177159415759626_0.jpeg',122),(276,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20171221_175%2F1513785335213dwGrL_JPEG%2F_Z3tVfy7CJOCTMlSN5JIC6uf.jpg',122),(277,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20171221_175%2F1513785335213dwGrL_JPEG%2F_Z3tVfy7CJOCTMlSN5JIC6uf.jpg',122),(278,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20190712_21%2F156290955414778emD_JPEG%2FKPJDM2i5_T304stxOQXTk_0f.JPG.jpg',123),(279,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20190821_115%2F1566380933950CiHrI_JPEG%2FVKcXwcbg-W8xAyHDxbbJyhhH.jpg',123),(280,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20190821_280%2F1566380933577NWevT_JPEG%2FHdKBamV4cyCn3JfK_oi_e2Yz.jpg',123),(281,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxOTA1MDZfNDMg%2FMDAxNTU3MTI5MjM2MjMy.2s9kC1CMAG7-JlohQP0IEzPoYfq5F7kiuVuT0TlE-k8g.JxsSvhpYqaGEbPSqfKapk4Ib9B9ZgELnRg5DihB1440g.JPEG.dkfkchlrh95%2Foutput_4074233293.jpg',124),(282,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxODA1MTJfMjYg%2FMDAxNTI2MTE2MDI1ODg0.Y5THjQkrPouaMV_V0Y3kL_fAoBUOrEo6ov4UzptNbpkg.vWePhIqdM7gfio-7-p3SYv7QnZyMlbyVZViXDVmJV3og.JPEG.cha4566%2F20180512_144627.jpg',124),(283,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxNzA1MDhfNzYg%2FMDAxNDk0MjI0MDk4OTE0.HTerby9SfI1Sh7q1AMAgIgkuN2H_oGMLZk4H6KPvy_Ag.FpdFvdAIVYQusMudLYV2DSP1Ildg3WN2EcNwL1U_fJcg.JPEG.itslisa%2F20170503_125153.jpg',124),(284,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20191108_205%2F157317796375661CnA_PNG%2FGErEpz7rzY9TvnnaJuMoxbKM.PNG.png',125),(285,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20191108_279%2F1573177963658z5UIw_PNG%2F_8nq14rTlmuJFEU95cXV3GR9.PNG.png',125),(286,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20191108_181%2F1573177963843Pzvwy_PNG%2FAxumJ5jPcEyj47E3hg3Bv4pE.PNG.png',125),(287,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTAxMTBfMjQ0%2FMDAxNjEwMjc3MDEzMDQx.tQRiuqtAnwqJx3ZI-TWC8ZJhVorEnXp7inhMh-XXsoMg.vRvQaCx1LZE_SQVAus3RdPSSRwr6h4c1iUzerA_XgcMg.JPEG.cyrupdown%2F1610277009128.jpg',127),(288,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMDA0MzBfMTM5%2FMDAxNTg4MjI3NTQ3Njg4.NT02aZEsm14Vc7m2OI4-ogIEDFk5Tm_-sbGtGyuVIfUg.8qRuLRDQU2NnI2qYLAF8SZ_bL_RVIRPNqV9Q3McRfNEg.JPEG.junlee4854%2F1588225410160.jpg',127),(289,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTAxMjNfMjE4%2FMDAxNjExNDAzMDU0NTMz.FEwNpz5xRPXnk0QefObShoJDFNLPtwb3RG2Y-bG552Eg.eRrKsOraqB7dWr32lMMc79VQ1OMqMXQsHNBNwWmULW4g.JPEG.chaelinnn94%2FIMG_4064.jpg',127),(290,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20201123_104%2F16060658304842bb1L_JPEG%2FBE3v5nY4N5ACOvAMt8qu3SIR.jpg',128),(291,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20210210_85%2F1612916961585A5FGk_JPEG%2F3dQzNm-sugrVnetO086MUaUU.jpg',128),(292,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20200910_106%2F15996785829440W9uo_JPEG%2FM3px92ChsECmd8eDODOn406e.jpg',128),(293,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20180406_281%2F1522999750979nBQie_JPEG%2FSJglMNIovCOSk4LQDzWdAcUU.jpg',129),(294,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20180406_73%2F1522999751187m0zR0_JPEG%2FjTMhWmilsUruLioQHjQi1LU0.jpg',129),(295,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20180406_237%2F1522999750922v4bkO_JPEG%2Ff3I4IiOvMNDn7pOeZfjdaD95.jpg',129),(296,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20210326_36%2F1616739096944nXXw3_JPEG%2Fupload_0ea012a41e0e1f096e3e8e28afd9115e.jpg',130),(297,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20210326_289%2F1616739084318WkIBl_JPEG%2Fupload_f2b40a748279ed74e92d0a42c56d58c4.jpg',130),(298,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20210403_167%2F1617442240443OoODR_JPEG%2Fupload_5603932672a7350e11f742faaaa18f2e.jpeg',130),(299,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20210326_85%2F16167611979112IhSB_JPEG%2Fupload_866fc331360ac6e43c68eb35ad5c79d4.jpg',131),(300,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20210404_300%2F1617535513947cOKAT_JPEG%2Fupload_9b9e174d27a72d361f89839e0847ac46.jpeg',131),(301,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fmyplace-phinf.pstatic.net%2F20210405_31%2F1617594845286eLxkt_JPEG%2Fupload_2fa4506ca4b59aa901bb5abdd7ccb65c.jpg',131),(305,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20210402_76%2F1617335849291PdVAR_JPEG%2Fresize_20315_The_Brasserie_Gyeongsang_Promotion_%25B0%25E6%25BB%25F3_%25C7%25C1%25B7%25CE%25B8%25F0%25BC%25C7.jpg',133),(306,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20191105_122%2F1572932217410lkQCG_JPEG%2F0531_The_Brasserie_%25B8%25C0%25B4%25EB%25B8%25C0_%25C7%25C1%25B7%25CE%25B8%25F0%25BC%25C7_Jeonla_vs_Kyungsang.jpg',133),(307,'https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20190827_236%2F1566882760888py8mD_JPEG%2F0730_The_Brasserie_Fresh_Market.jpg',133);
/*!40000 ALTER TABLE `store_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stores`
--

DROP TABLE IF EXISTS `stores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `one_line_introduction` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `opening_time_description` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone_number` varchar(15) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `sns_url` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `menu_pamphlet_image_url` varchar(3000) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `is_reservation` tinyint(1) NOT NULL,
  `is_wifi` tinyint(1) NOT NULL,
  `is_parking` tinyint(1) NOT NULL,
  `category_id` int NOT NULL,
  `open_status_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `stores_category_id_612c38a1_fk_categories_id` (`category_id`),
  KEY `stores_open_status_id_534b30e6_fk_open_status_id` (`open_status_id`),
  CONSTRAINT `stores_category_id_612c38a1_fk_categories_id` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `stores_open_status_id_534b30e6_fk_open_status_id` FOREIGN KEY (`open_status_id`) REFERENCES `open_status` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stores`
--

LOCK TABLES `stores` WRITE;
/*!40000 ALTER TABLE `stores` DISABLE KEYS */;
INSERT INTO `stores` VALUES (53,'순남시래기','시래기와 막걸리가 맛있는 집!','평일 09시 ~ 23시','02-427-6626','https://www.instagram.com/soonnamsiraegi/',NULL,1,1,1,1,2),(69,'스타벅스','커피가 맛있는 집','평일 1시 ~ 2시','010-1234-1234','www.naver.com',NULL,0,0,0,14,2),(112,'삼백플러스','삼백플러스에서 행복한 점심을 만들어보세요.','목요일 10:30 - 14:30 주말.공휴일 휴무','123-45-456','https://m.place.naver.com/restaurant/1973586065/home?feedId=760955',NULL,0,0,0,14,2),(113,'외고집설렁탕','설명 항상 최상의 횡성 한우만 고집하고 국산 재료(무, 배추, 고춧가루, 천일염 등)만 사용하며, 화학조미료나 기타 첨가물을 일절 사용하지 않는 최고의 설렁탕 집입니다.',' 매일 11:00 - 21:00 주문 마감시간 ','02-567-5225','홈페이지 http://oegojip.modoo.at/',NULL,0,0,0,1,2),(118,'코벤트가든 선릉점','선릉역 대치동에 있는 코벤트 가든 파스타 피자','매일 11:00 - 21:00 주문 마감시간 ','02-3453-5565','',NULL,0,0,0,23,2),(120,'오동도','하모(갯장어), 전어 등 제철 해물을 전라도식으로 요리하는 곳입니다.','매일 11:30 - 22:30 ','02-557-0039',NULL,NULL,0,0,0,1,5),(121,'앵그리치밥','설명 삼성동 선릉역에 위치하고 있는 치밥전문 브랜드 \"앵그리치밥\"입니다.','평일 11:00 - 21:00','02-6949-3680','https://www.instagram.com/angry_chibab/',NULL,0,0,0,22,2),(122,'뽕나무쟁이 ','선릉 맛집 맛있는 양념이 베어있는 뽕나무쟁이 족발','평일 12:00 - 01:00 ','02-558-9279','http://www.ppong.net/',NULL,0,0,0,1,5),(123,'진풍정 ','강남 한정식맛집 진진바라 품격있는 모임장소','매일 11:30 - 22:00 ','02-538-7733','http://www.jinpoongjeong.com',NULL,0,0,0,1,2),(124,'스시키','숙성스시를 다루는 다찌8~10석정도만 되는 작은 미들급 스시야입니다','영업시간 매일 12:00 - 15:00 런치','1441-2008','https://app.catchtable.co.kr/ct/shop/sushiki',NULL,0,0,0,20,2),(125,'일미리금계찜닭 ','선릉역 회식장소로 좋은 구름치즈찜닭','영업시간 매일 11:00 - 22:00','02-557-7077복사','http://goldjjimdak.com/',NULL,0,0,0,1,2),(126,'청담동마녀김밥 대치점','\'전지적참견시점\',\'생활의 달인\', \'생방송 아침이 좋다\'등에 소개된 중독성 강한 김밥으로 수 많은 연예인들이 직접 방문하여 맛을 인정한 청담동 마녀김밥의 직영점입니다.','매일 08:00 - 21:00','02-539-3111','https://app.catchtable.co.kr/ct/shop/sushiki',NULL,0,0,0,17,2),(127,'FIREBELL','외국인들도 샤이니 민호도 반한 수제버거집','매일 11:30 - 21:00','1414-0041','http://instagram.com/firebell.official',NULL,0,0,0,16,2),(128,'커리146 ','제대로 만들어내는 영국식 인도커리 전문점 커리146입니다.','평일 11:00 - 20:30 ','0507-1373-0164','https://www.instagram.com/curry146_gangnam/',NULL,0,0,0,22,2),(129,'테라로사','테라로사 포스코센터점카페','평일 07:30 - 21:00','033-648-2760',NULL,NULL,0,0,0,13,2),(130,'스시욘즈','업계 최고의 쉐프가 합리적인 가겨으로 최고의 시간을 만들어 드리겠습니다','12:00 - 22:00','010-5225-6210','www.instagram.com/sushi_yz/?igshid=1wbh7',NULL,0,0,0,20,1),(131,'브루클린더버거조인트 ','수제버거가 맛있는 브루클린 더 버거','매일 11:00 - 21:30','02-555-7180','http://www.menupan.com/restaurant/onepage.asp?acode=R106970',NULL,0,0,0,16,1),(133,'인터컨티넨탈 서울','인터컨티넨탈 서울 코엑스 브래서리 분위기좋은 호텔 뷔페','평일 18:00 - 22:00 ','02-3430-8585','https://seoul.intercontinental.com/iccoex/restaurant/Brasserie',NULL,0,0,0,23,5);
/*!40000 ALTER TABLE `stores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `password` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `kakao_id` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `google_id` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `kakao_id` (`kakao_id`),
  UNIQUE KEY `google_id` (`google_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,NULL,NULL,'1680851554',NULL,'2021-03-31 20:55:32.658136','2021-03-31 20:55:32.658188'),(2,NULL,NULL,'1683188795',NULL,'2021-04-02 19:33:52.199911','2021-04-02 19:33:52.199971');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlists`
--

DROP TABLE IF EXISTS `wishlists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wishlists` (
  `id` int NOT NULL AUTO_INCREMENT,
  `store_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `wishlists_user_id_store_id_461ce240_uniq` (`user_id`,`store_id`),
  KEY `wishlists_store_id_7d266ed5_fk_stores_id` (`store_id`),
  CONSTRAINT `wishlists_store_id_7d266ed5_fk_stores_id` FOREIGN KEY (`store_id`) REFERENCES `stores` (`id`),
  CONSTRAINT `wishlists_user_id_6280b16e_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlists`
--

LOCK TABLES `wishlists` WRITE;
/*!40000 ALTER TABLE `wishlists` DISABLE KEYS */;
/*!40000 ALTER TABLE `wishlists` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-09 11:12:05
