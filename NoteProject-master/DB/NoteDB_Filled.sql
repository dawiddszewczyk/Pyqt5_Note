-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: NoteDB
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1

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
-- Table structure for table `TaskState`
--

DROP TABLE IF EXISTS `TaskState`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TaskState` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `State` text,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TaskState`
--

LOCK TABLES `TaskState` WRITE;
/*!40000 ALTER TABLE `TaskState` DISABLE KEYS */;
INSERT INTO `TaskState` VALUES (1,'Przeznaczone do usunięcia'),(2,'Stworzone'),(3,'Przydzielone'),(4,'W realizacji'),(5,'Zakończone'),(6,'Przeznaczone do archiwizacji');
/*!40000 ALTER TABLE `TaskState` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Tasks`
--

DROP TABLE IF EXISTS `Tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Tasks` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Date` varchar(150) DEFAULT NULL,
  `Title` text,
  `Contents` text,
  `StateID` int(11) DEFAULT NULL,
  `CreatorID` int(11) DEFAULT NULL,
  `UserID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `CreatorID` (`CreatorID`),
  KEY `UserID` (`UserID`),
  KEY `StateID` (`StateID`),
  CONSTRAINT `Tasks_ibfk_1` FOREIGN KEY (`CreatorID`) REFERENCES `Users` (`ID`),
  CONSTRAINT `Tasks_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `Users` (`ID`),
  CONSTRAINT `Tasks_ibfk_3` FOREIGN KEY (`StateID`) REFERENCES `TaskState` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tasks`
--

LOCK TABLES `Tasks` WRITE;
/*!40000 ALTER TABLE `Tasks` DISABLE KEYS */;
INSERT INTO `Tasks` VALUES (1,'28.01.13','Konserwacja Danych','Skopiować i zabezpieczyć dane',2,1,3);
INSERT INTO `Tasks` VALUES (2,'15.01.2017','Analiza Malware','Przesyłam Ci paczkę malwareu do analizy. Rzuć na to okiem.',2,1,3);
INSERT INTO `Tasks` VALUES (3,'10.01.2018','Audyt Bezpieczeństwa','Jutro przeprowadzmy audyt bezpieczeństwa. Pracownicy działu bezpieczeństwa proszeni są o stawiwnie się w jutrzejszym dniu w sali konferencyjnej o gdzinie 8:00.',2,1,3);
INSERT INTO `Tasks` VALUES (4,'21.05.2018','Testy Aplikacji','Przeprowadź testy i przygotuj raport.',2,1,3);
INSERT INTO `Tasks` VALUES (5,'10.06.18','Konferencja zagraniczna','Przygotuj tekst na konferecję z TaskMiracle Company. Wymagane jest opracowanie w języku angielksim i rosyjskim!',2,1,3);
INSERT INTO `Tasks` VALUES (6,'11.11.19','Objekt 0312','Do dnia 11.02.2021 musimy przygotować prototyp narzędzia niszczącego urządzenia działające w sieci botnet.',2,1,3);
INSERT INTO `Tasks` VALUES (7,'01.05.18','Spotkanie z zarządem','Musimy przedstawić postęp naszych prac zarządowi firmy.',2,1,3);
INSERT INTO `Tasks` VALUES (8,'24.11.18','Przygotowanie projekty aplikacji','Zgodnie z otrzymanymi wytycznymi przygotuj projekt aplikacji dla klienta.',2,1,3);
INSERT INTO `Tasks` VALUES (9,'10.03.18','Podsumowanie testów bezpieczeństwa','Niniejszy raport jest podsumowaniem testów bezpieczeństwa systemu YetiForce CRM w wersji 4.0.0.',2,1,3);
INSERT INTO `Tasks` VALUES (10,'30.09.18','Wnioski z testów','W systemie YetiForce zidentyfikowano kilka sposobów na wykonywanie dowolnego kodu po stronie
serwera. Praktycznie tego typu podatność może zostać wykorzystana m.in. do: Przejęcia wszystkich danych przechodzących przez system YetiForce. Mogą to być zarówno
dane użytkowników systemu (loginy i hasła), jak i dane przetwarzane przez system, takie jak:
listy kontrahentów, dane osobowe itp.
Dalszych ataków na inne hosty znajdujące się w sieci wewnętrznej,
Wykorzystanie oprogramowania typu „ransomware”, skutkującego zaszyfrowaniem plików na
dysku.',2,1,3);
INSERT INTO `Tasks` VALUES (11,'23.02.18','Zalecenia','Większość podatności wynika z możliwości bezpośredniego dostępu do uploadowanych plików z
poziomu webroota. Zmiana architektury systemu YetiForce w taki sposób, by pliki wgrywane
użytkowników nie były umieszczone w webroocie pozwoli zniwelować te ryzyka.',2,1,3);
INSERT INTO `Tasks` VALUES (12,'14.12.18','Podsumowanie techniczne','Wiesz co robić.',2,1,3);
/*!40000 ALTER TABLE `Tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UserInfo`
--

DROP TABLE IF EXISTS `UserInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserInfo` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `UserID` int(11) DEFAULT NULL,
  `PicturePath` text,
  PRIMARY KEY (`ID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `UserInfo_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `Users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserInfo`
--

LOCK TABLES `UserInfo` WRITE;
/*!40000 ALTER TABLE `UserInfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `UserInfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Login` varchar(40) DEFAULT NULL,
  `Password` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'Jan','JanK'),(2,'Roksana','Roksana321'),(3,'Edward','Edw123');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-25 21:38:37
