-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 22, 2021 at 04:54 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nexttrain2`
--

-- --------------------------------------------------------

--
-- Table structure for table `platforms`
--

CREATE TABLE `platforms` (
  `ID` varchar(20) NOT NULL,
  `StationID` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `rail`
--

CREATE TABLE `rail` (
  `ID` varchar(20) NOT NULL,
  `network` varchar(20) NOT NULL,
  `length` int(11) NOT NULL,
  `width` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `rail_connections`
--

CREATE TABLE `rail_connections` (
  `railID` varchar(20) NOT NULL,
  `StationID` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `route`
--

CREATE TABLE `route` (
  `ID` varchar(20) NOT NULL,
  `network` varchar(20) NOT NULL,
  `popularity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `route_station`
--

CREATE TABLE `route_station` (
  `LineID` varchar(20) NOT NULL,
  `StationID` varchar(20) NOT NULL,
  `stopNumber` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `stations`
--

CREATE TABLE `stations` (
  `ID` varchar(20) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Network` varchar(20) NOT NULL,
  `Popularity` int(11) NOT NULL,
  `isStation` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `platforms`
--
ALTER TABLE `platforms`
  ADD KEY `StationID` (`StationID`);

--
-- Indexes for table `rail`
--
ALTER TABLE `rail`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `rail_connections`
--
ALTER TABLE `rail_connections`
  ADD KEY `railID` (`railID`),
  ADD KEY `StationID` (`StationID`);

--
-- Indexes for table `route`
--
ALTER TABLE `route`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `route_station`
--
ALTER TABLE `route_station`
  ADD KEY `LineID` (`LineID`),
  ADD KEY `StationID` (`StationID`);

--
-- Indexes for table `stations`
--
ALTER TABLE `stations`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `platforms`
--
ALTER TABLE `platforms`
  ADD CONSTRAINT `platforms_ibfk_1` FOREIGN KEY (`StationID`) REFERENCES `stations` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `rail_connections`
--
ALTER TABLE `rail_connections`
  ADD CONSTRAINT `rail_connections_ibfk_1` FOREIGN KEY (`railID`) REFERENCES `rail` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `rail_connections_ibfk_2` FOREIGN KEY (`StationID`) REFERENCES `stations` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `route_station`
--
ALTER TABLE `route_station`
  ADD CONSTRAINT `route_station_ibfk_1` FOREIGN KEY (`StationID`) REFERENCES `stations` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `route_station_ibfk_2` FOREIGN KEY (`LineID`) REFERENCES `route` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
