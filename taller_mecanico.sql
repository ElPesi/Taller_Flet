CREATE DATABASE  IF NOT EXISTS `taller_mecanico` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `taller_mecanico`;
-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: taller_mecanico
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `cod_cliente` varchar(20) NOT NULL,
  `dni` varchar(20) NOT NULL,
  PRIMARY KEY (`cod_cliente`),
  KEY `FK_dni_cliente` (`dni`),
  CONSTRAINT `FK_dni_cliente` FOREIGN KEY (`dni`) REFERENCES `persona` (`dni`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES ('A105','17890452'),('C130','17896456');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_detalle`
--

DROP TABLE IF EXISTS `customer_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_detalle` (
  `id_detalle_customer` int NOT NULL,
  `id_customer` int NOT NULL,
  `cod_cliente` varchar(20) NOT NULL,
  `patente` varchar(10) NOT NULL,
  `cod_tipo_vehiculo` varchar(5) NOT NULL,
  `cod_marca` int DEFAULT NULL,
  PRIMARY KEY (`id_detalle_customer`),
  KEY `FK_cod_tipo_vehiculo` (`cod_tipo_vehiculo`),
  KEY `FK_cod_cliente` (`cod_cliente`),
  KEY `FK_cod_marca` (`cod_marca`),
  KEY `FK_idCustomer` (`id_customer`) /*!80000 INVISIBLE */,
  CONSTRAINT `FK_cod_cliente` FOREIGN KEY (`cod_cliente`) REFERENCES `cliente` (`cod_cliente`) ON UPDATE CASCADE,
  CONSTRAINT `FK_cod_marca` FOREIGN KEY (`cod_marca`) REFERENCES `marca` (`cod_marca`) ON UPDATE CASCADE,
  CONSTRAINT `FK_cod_tipo_vehiculo` FOREIGN KEY (`cod_tipo_vehiculo`) REFERENCES `tipo_vehiculo` (`cod_tipo_vehiculo`) ON UPDATE CASCADE,
  CONSTRAINT `FK_idCustomer` FOREIGN KEY (`id_customer`) REFERENCES `customer_vehiculo` (`id_customer`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_detalle`
--

LOCK TABLES `customer_detalle` WRITE;
/*!40000 ALTER TABLE `customer_detalle` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_vehiculo`
--

DROP TABLE IF EXISTS `customer_vehiculo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_vehiculo` (
  `id_customer` int NOT NULL AUTO_INCREMENT,
  `cod_cliente` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_customer`),
  KEY `Fk_Customer_cliente` (`cod_cliente`),
  CONSTRAINT `Fk_Customer_cliente` FOREIGN KEY (`cod_cliente`) REFERENCES `cliente` (`cod_cliente`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_vehiculo`
--

LOCK TABLES `customer_vehiculo` WRITE;
/*!40000 ALTER TABLE `customer_vehiculo` DISABLE KEYS */;
INSERT INTO `customer_vehiculo` VALUES (2,'A105');
/*!40000 ALTER TABLE `customer_vehiculo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_empleado_fechatec`
--

DROP TABLE IF EXISTS `detalle_empleado_fechatec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_empleado_fechatec` (
  `id_detalle_empleado_FT` int NOT NULL AUTO_INCREMENT,
  `nro_ficha` int NOT NULL,
  `legajo` int NOT NULL,
  `horas_trabajadas` float DEFAULT NULL,
  PRIMARY KEY (`id_detalle_empleado_FT`),
  KEY `FKnro_ficha` (`nro_ficha`),
  KEY `FK_codLegajo` (`legajo`),
  CONSTRAINT `FK_codLegajo` FOREIGN KEY (`legajo`) REFERENCES `empleado` (`legajo`) ON UPDATE CASCADE,
  CONSTRAINT `FKnro_ficha` FOREIGN KEY (`nro_ficha`) REFERENCES `ficha_tecnica` (`nro_ficha`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_empleado_fechatec`
--

LOCK TABLES `detalle_empleado_fechatec` WRITE;
/*!40000 ALTER TABLE `detalle_empleado_fechatec` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalle_empleado_fechatec` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_ficha`
--

DROP TABLE IF EXISTS `detalle_ficha`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_ficha` (
  `id_detalle_ficha` int NOT NULL AUTO_INCREMENT,
  `nro_ficha` int NOT NULL,
  `fecha` date NOT NULL,
  `cod_respuesto` varchar(30) NOT NULL,
  `descripcion` varchar(50) DEFAULT NULL,
  `cantidad` float NOT NULL,
  `precio` float NOT NULL,
  `importe` float NOT NULL,
  PRIMARY KEY (`id_detalle_ficha`),
  KEY `FK_nro_ficha` (`nro_ficha`),
  KEY `FKcod_respuesto` (`cod_respuesto`),
  CONSTRAINT `FK_nro_ficha` FOREIGN KEY (`nro_ficha`) REFERENCES `ficha_tecnica` (`nro_ficha`) ON UPDATE CASCADE,
  CONSTRAINT `FKcod_respuesto` FOREIGN KEY (`cod_respuesto`) REFERENCES `repuestos` (`cod_repuesto`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_ficha`
--

LOCK TABLES `detalle_ficha` WRITE;
/*!40000 ALTER TABLE `detalle_ficha` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalle_ficha` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleado`
--

DROP TABLE IF EXISTS `empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleado` (
  `legajo` int NOT NULL,
  `dni` varchar(20) NOT NULL,
  PRIMARY KEY (`legajo`),
  KEY `FK_dni_empleado` (`dni`),
  CONSTRAINT `FK_dni_empleado` FOREIGN KEY (`dni`) REFERENCES `persona` (`dni`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleado`
--

LOCK TABLES `empleado` WRITE;
/*!40000 ALTER TABLE `empleado` DISABLE KEYS */;
/*!40000 ALTER TABLE `empleado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ficha_tecnica`
--

DROP TABLE IF EXISTS `ficha_tecnica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ficha_tecnica` (
  `nro_ficha` int NOT NULL,
  `cod_cliente` varchar(20) DEFAULT NULL,
  `vehiculo` varchar(12) NOT NULL,
  `subtotal` float DEFAULT NULL,
  `mano_obra` float DEFAULT NULL,
  `total_general` float DEFAULT NULL,
  PRIMARY KEY (`nro_ficha`),
  KEY `FK_CodCliente` (`cod_cliente`),
  CONSTRAINT `FK_CodCliente` FOREIGN KEY (`cod_cliente`) REFERENCES `cliente` (`cod_cliente`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ficha_tecnica`
--

LOCK TABLES `ficha_tecnica` WRITE;
/*!40000 ALTER TABLE `ficha_tecnica` DISABLE KEYS */;
/*!40000 ALTER TABLE `ficha_tecnica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marca`
--

DROP TABLE IF EXISTS `marca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marca` (
  `cod_marca` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`cod_marca`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marca`
--

LOCK TABLES `marca` WRITE;
/*!40000 ALTER TABLE `marca` DISABLE KEYS */;
INSERT INTO `marca` VALUES (1,'RENAULT'),(2,'FORD'),(3,'FIAT'),(4,'VOLKSWAGEN'),(5,'CHEVROLET'),(6,'TOYOTA'),(7,'HONDA');
/*!40000 ALTER TABLE `marca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona`
--

DROP TABLE IF EXISTS `persona`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `persona` (
  `dni` varchar(20) NOT NULL,
  `apellido` varchar(40) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `direccion` varchar(50) DEFAULT NULL,
  `tele_contac` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`dni`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona`
--

LOCK TABLES `persona` WRITE;
/*!40000 ALTER TABLE `persona` DISABLE KEYS */;
INSERT INTO `persona` VALUES ('17890452','POSTAI','FABIAN','AYACUCHO 969','3515504584'),('17896456','PEREZ','RODOLFO','BSFBGFG 7896','351789654');
/*!40000 ALTER TABLE `persona` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `presupuesto`
--

DROP TABLE IF EXISTS `presupuesto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presupuesto` (
  `nro_presupuesto` INT NOT NULL,
  `cod_cliente` VARCHAR(20) DEFAULT NULL,
  `descripcion` VARCHAR(255) DEFAULT NULL,
  `total_presupuesto` FLOAT DEFAULT NULL,
  `total_gastado` FLOAT DEFAULT NULL,
  PRIMARY KEY (`nro_presupuesto`),
  KEY `FK_CodCliente_Presupuesto` (`cod_cliente`),
  CONSTRAINT `FK_CodCliente_Presupuesto` FOREIGN KEY (`cod_cliente`) REFERENCES `cliente` (`cod_cliente`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presupuesto`
--

LOCK TABLES `presupuesto` WRITE;
/*!40000 ALTER TABLE `presupuesto` DISABLE KEYS */;
/*!40000 ALTER TABLE `presupuesto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_vehiculo`
--

DROP TABLE IF EXISTS `tipo_vehiculo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_vehiculo` (
  `cod_tipo_vehiculo` varchar(5) NOT NULL,
  `descripcion` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`cod_tipo_vehiculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_vehiculo`
--

LOCK TABLES `tipo_vehiculo` WRITE;
/*!40000 ALTER TABLE `tipo_vehiculo` DISABLE KEYS */;
INSERT INTO `tipo_vehiculo` VALUES ('1','AUTO'),('2','PIKUP'),('3','CAMIÓN'),('4','MOTO'),('5','LANCHA');
/*!40000 ALTER TABLE `tipo_vehiculo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'taller_mecanico'
--

--
-- Dumping routines for database 'taller_mecanico'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-23 13:23:25
