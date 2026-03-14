-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: myNetworkdb
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES (1,'SENA','Pasto'),(2,'Colegio Mayor','Popayan'),(3,'ICESI','Cali'),(4,'Universidad del Valle','Cali');
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modem`
--

DROP TABLE IF EXISTS `modem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modem` (
  `id` int(11) NOT NULL,
  `modulation_type` varchar(50) NOT NULL,
  `downstream_speed_mbps` int(11) NOT NULL,
  `upstream_speed_mbps` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_modem_networkdevice` FOREIGN KEY (`id`) REFERENCES `networkdevice` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modem`
--

LOCK TABLES `modem` WRITE;
/*!40000 ALTER TABLE `modem` DISABLE KEYS */;
INSERT INTO `modem` VALUES (3,'DOCSIS 3.1',1000,100),(4,'GPON',300,150);
/*!40000 ALTER TABLE `modem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `networkdevice`
--

DROP TABLE IF EXISTS `networkdevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `networkdevice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_name` varchar(100) NOT NULL,
  `manufacturer` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  `company_id` int(11) NOT NULL,
  `device_type` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_networkdevice_company` (`company_id`),
  CONSTRAINT `fk_networkdevice_company` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_device_type` CHECK (`device_type` in ('router','modem','switch'))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `networkdevice`
--

LOCK TABLES `networkdevice` WRITE;
/*!40000 ALTER TABLE `networkdevice` DISABLE KEYS */;
INSERT INTO `networkdevice` VALUES (1,'Cisco Router 1','Cisco','RV340',1,'router'),(2,'Huawei Router 1','Huawei','AR1220',2,'router'),(3,'Arris Modem 1','Arris','SB8200',1,'modem'),(4,'Huawei Modem 2','Huawei','EchoLife HG8245H',3,'modem'),(5,'Cisco Switch 1','Cisco','Catalyst 2960',1,'switch'),(6,'TP-Link Switch 2','TP-Link','TL-SG1024',4,'switch');
/*!40000 ALTER TABLE `networkdevice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `route`
--

DROP TABLE IF EXISTS `route`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `route` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `router_id` int(11) NOT NULL,
  `destination_address` varchar(50) NOT NULL,
  `next_hop` varchar(50) NOT NULL,
  `metric` int(11) NOT NULL,
  `interface` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_route_router` (`router_id`),
  CONSTRAINT `fk_route_router` FOREIGN KEY (`router_id`) REFERENCES `router` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `route`
--

LOCK TABLES `route` WRITE;
/*!40000 ALTER TABLE `route` DISABLE KEYS */;
INSERT INTO `route` VALUES (1,1,'192.168.2.0/24','192.168.1.254',1,'eth0'),(2,1,'10.0.0.0/16','192.168.1.254',2,'eth1'),(3,2,'172.16.0.0/12','10.0.0.254',1,'g0/0');
/*!40000 ALTER TABLE `route` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `router`
--

DROP TABLE IF EXISTS `router`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `router` (
  `id` int(11) NOT NULL,
  `routing_protocol` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_router_networkdevice` FOREIGN KEY (`id`) REFERENCES `networkdevice` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `router`
--

LOCK TABLES `router` WRITE;
/*!40000 ALTER TABLE `router` DISABLE KEYS */;
INSERT INTO `router` VALUES (1,'OSPF'),(2,'RIP');
/*!40000 ALTER TABLE `router` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `switchdevice`
--

DROP TABLE IF EXISTS `switchdevice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `switchdevice` (
  `id` int(11) NOT NULL,
  `number_of_ports` int(11) NOT NULL,
  `managed` tinyint(1) NOT NULL,
  `switching_capacity_gbps` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_switch_networkdevice` FOREIGN KEY (`id`) REFERENCES `networkdevice` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `switchdevice`
--

LOCK TABLES `switchdevice` WRITE;
/*!40000 ALTER TABLE `switchdevice` DISABLE KEYS */;
INSERT INTO `switchdevice` VALUES (5,24,1,56.00),(6,24,0,48.00);
/*!40000 ALTER TABLE `switchdevice` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-13  6:39:00
