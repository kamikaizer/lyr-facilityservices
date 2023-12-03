-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: prueba
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.28-MariaDB

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
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dv` varchar(1) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `rut` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20120209 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (20120207,'k','asda',20120206),(20120208,'1','MAIPU2',195656653);
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cotizacion`
--

DROP TABLE IF EXISTS `cotizacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cotizacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date DEFAULT NULL,
  `tipo` int(11) DEFAULT NULL,
  `detalle` text DEFAULT NULL,
  `estado` int(11) DEFAULT NULL,
  `rut_empresa` int(11) DEFAULT NULL,
  `solicitante` varchar(100) DEFAULT NULL,
  `orden_compra` int(11) DEFAULT NULL,
  `factura` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tipo` (`tipo`),
  KEY `cotizacion_FK` (`rut_empresa`),
  CONSTRAINT `cotizacion_ibfk_2` FOREIGN KEY (`tipo`) REFERENCES `tipo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cotizacion`
--

LOCK TABLES `cotizacion` WRITE;
/*!40000 ALTER TABLE `cotizacion` DISABLE KEYS */;
INSERT INTO `cotizacion` VALUES (1,NULL,NULL,'<p>este es el detalle:</p><ul><li>1</li><li>2</li><li>3</li><li>45</li><li>5 asdas</li></ul>',1,20120206,NULL,-1,758),(4,'2023-11-15',NULL,'',1,20120206,NULL,-1,NULL),(8,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL),(10,'2023-10-28',NULL,'',1,20120206,'Cristian Navarro',-1,123),(11,'2023-11-09',NULL,'<p>Este es el detalle de la cotización:</p><ul><li>cosa1</li><li>cosa2</li></ul>',1,20120206,'yo soy el solicitante',123,123),(12,'2023-11-10',NULL,'<p>Presupuesto incluye:</p><ul><li>Despacho</li></ul>',1,20120206,'Prueba 1',-1,NULL),(13,'2023-11-16',NULL,'<p>asdasdasdasd</p>',1,20120206,'yo soy el solicitante',523,NULL),(14,'2023-12-03',NULL,'',1,20120206,'Cristian Navarroasdasd',-1,123),(15,'2023-12-03',NULL,'',1,20120206,'soy yo',NULL,NULL);
/*!40000 ALTER TABLE `cotizacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mano_obra`
--

DROP TABLE IF EXISTS `mano_obra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mano_obra` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_cotizacion` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio` int(11) DEFAULT NULL,
  `dias` int(11) DEFAULT NULL,
  `valor_neto` float DEFAULT NULL,
  `glosa` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_cotizacion` (`id_cotizacion`),
  CONSTRAINT `mano_obra_ibfk_1` FOREIGN KEY (`id_cotizacion`) REFERENCES `cotizacion` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mano_obra`
--

LOCK TABLES `mano_obra` WRITE;
/*!40000 ALTER TABLE `mano_obra` DISABLE KEYS */;
INSERT INTO `mano_obra` VALUES (5,1,2,1000,4,8000,'coasas'),(7,1,5,3000,1,15000,'cosas'),(12,1,5,12,15,900,'cosas'),(13,11,5,355,1,1775,'Lamparas 220V'),(14,11,5,355,1,1775,'Lamparas 220V'),(16,4,5,1000,2,10000,'cosas'),(17,4,3,3000,1,9000,'asda'),(18,12,5,50000,1,250000,'despacho'),(19,13,5,25000,6,750000,'personas');
/*!40000 ALTER TABLE `mano_obra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `material`
--

DROP TABLE IF EXISTS `material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `material` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_cotizacion` int(11) DEFAULT NULL,
  `proveedor` varchar(50) DEFAULT NULL,
  `valor_neto` int(11) DEFAULT NULL,
  `glosa` varchar(50) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_cotizacion` (`id_cotizacion`),
  CONSTRAINT `material_ibfk_1` FOREIGN KEY (`id_cotizacion`) REFERENCES `cotizacion` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `material`
--

LOCK TABLES `material` WRITE;
/*!40000 ALTER TABLE `material` DISABLE KEYS */;
INSERT INTO `material` VALUES (14,1,NULL,1000,'cosas',5),(15,1,NULL,6000,'cosas',2),(17,11,NULL,2100,'Ampolleta 7W',5),(18,11,NULL,2100,'Ampolleta 7W',5),(21,4,NULL,3500,'Ampolleta 7W',5),(23,12,NULL,1000,'Ampolleta 5W',5),(24,13,NULL,5000,'Ampolleta 7W',5);
/*!40000 ALTER TABLE `material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `origen`
--

DROP TABLE IF EXISTS `origen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `origen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `origen`
--

LOCK TABLES `origen` WRITE;
/*!40000 ALTER TABLE `origen` DISABLE KEYS */;
/*!40000 ALTER TABLE `origen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sol_vacaciones`
--

DROP TABLE IF EXISTS `sol_vacaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sol_vacaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fechainicio` date DEFAULT NULL,
  `fechafin` date DEFAULT NULL,
  `detalle` text DEFAULT NULL,
  `estado` int(11) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sol_vacaciones`
--

LOCK TABLES `sol_vacaciones` WRITE;
/*!40000 ALTER TABLE `sol_vacaciones` DISABLE KEYS */;
INSERT INTO `sol_vacaciones` VALUES (1,'2023-07-15','2023-07-22','adsfg',0,'qfas.asdv'),(2,'2023-07-15','2023-07-28','dfgxchgxds',0,'qfas.asdv');
/*!40000 ALTER TABLE `sol_vacaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo`
--

DROP TABLE IF EXISTS `tipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo`
--

LOCK TABLES `tipo` WRITE;
/*!40000 ALTER TABLE `tipo` DISABLE KEYS */;
/*!40000 ALTER TABLE `tipo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'root','4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2','2'),(7,'cristian_navaro','b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79','3'),(8,'hola','b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79','1'),(9,'rrhh','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','3');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'prueba'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-03 13:33:10
