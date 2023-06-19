-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql:3131
-- Generation Time: Jun 19, 2023 at 03:03 PM
-- Server version: 8.0.32
-- PHP Version: 8.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_conference_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int NOT NULL,
  `admin_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `contact` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `reset_password_token` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `status` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `admin_name`, `contact`, `email`, `password`, `reset_password_token`, `status`, `created_at`, `updated_at`) VALUES
(1, 'Super Admin', '0245678987', 'admin@admin.com', '$2b$12$T8qdN5.zY07wpT8/GubbtuFscOJt2LuqBGjN1SUdmcihD0RMN2ztC', NULL, 'Active', '2023-05-31 12:40:57', '2023-05-31 12:40:57'),
(2, 'Emma', 'password', 'emma@test.com', NULL, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODY4MjA3MjR9.rhKj5pysGqJZ4blX7ECFSlgiDuXC-mTvWqzHqHhA5gs', 'Active', '2023-06-15 08:18:44', '2023-06-15 08:18:44');

-- --------------------------------------------------------

--
-- Table structure for table `attendances`
--

CREATE TABLE `attendances` (
  `id` int NOT NULL,
  `status` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `admin_id` int DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `participantId` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

CREATE TABLE `events` (
  `id` int NOT NULL,
  `event_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `venue` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `flyer` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `start_date` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `registration_time` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `how_to_join` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `program_outline` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `end_date` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `number_of_participants` int DEFAULT NULL,
  `description` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `admin_id` int DEFAULT NULL,
  `status` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`id`, `event_name`, `venue`, `flyer`, `start_date`, `registration_time`, `how_to_join`, `program_outline`, `end_date`, `number_of_participants`, `description`, `admin_id`, `status`, `created_at`, `updated_at`) VALUES
(1, 'EID AL-ADHA', 'GHANA CATHEDRAL', 'EID AL-ADHA.png', '2023-01-01', '9:00AM', 'Onsite', 'SMART CONFERENCING DOC_1.pdf', '2023-10-10', 56000, 'Muslims Festive Season', 1, 'Active', '2023-05-31 12:50:38', '2023-05-31 12:50:38'),
(2, 'AFRICAN UNION DAY', 'GI-KACE', 'African Union Day.jpeg', '2023-01-01', '9:00AM', 'Onsite', 'appraisalManagementSRS.pdf', '2023-10-10', 56000, 'African Day', 1, 'Active', '2023-05-31 12:52:02', '2023-05-31 12:52:02'),
(3, 'may day', 'AITI-KACE', NULL, '1111', '12', 'Virtual', NULL, '1111', 250, 'workers day', 1, 'InActive', '2023-06-15 10:22:11', '2023-06-15 10:23:56'),
(4, 'Femi-tech', 'aiti', 'Screenshot from 2023-06-14 13-29-12.png', '11-05-2023', '9:20', 'virtual ', 'Screenshot from 2023-06-14 13-29-12.png', '11-05-2023', 250, 'females in tech', 1, 'InActive', '2023-06-16 10:02:33', '2023-06-16 11:10:34');

-- --------------------------------------------------------

--
-- Table structure for table `participants`
--

CREATE TABLE `participants` (
  `id` int NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone_number` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `gender` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `organization` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `how_to_join` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `registration_time` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `location` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `event_id` int DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `participants`
--

INSERT INTO `participants` (`id`, `name`, `phone_number`, `gender`, `email`, `organization`, `status`, `how_to_join`, `registration_time`, `location`, `event_id`, `created_at`, `updated_at`) VALUES
(1, 'Nana Kwesi', '1234567890', 'Male', 'nana@gmial.com', 'AITI-KACE', 0, 'Onsite', '09:30AM', 'Bolga', 2, '2023-05-31 12:53:24', '2023-05-31 12:53:24');

-- --------------------------------------------------------

--
-- Table structure for table `participant_fields`
--

CREATE TABLE `participant_fields` (
  `id` int NOT NULL,
  `field_name` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `field_type` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `field_validation` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `field_max_length` varchar(255) DEFAULT NULL,
  `field_min_length` varchar(255) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `event_id` int DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `participant_fields`
--

INSERT INTO `participant_fields` (`id`, `field_name`, `field_type`, `field_validation`, `field_max_length`, `field_min_length`, `status`, `event_id`, `created_at`, `updated_at`) VALUES
(1, 'Full Name', 'textField', '0', '30', '3', 1, 4, '2023-06-16 14:05:28', '2023-06-16 14:05:28'),
(2, 'Gender', 'Dropdown', '0', NULL, NULL, 1, 4, '2023-06-16 14:09:06', '2023-06-16 14:09:06'),
(3, 'Email', 'textField', '1', '50', '10', 1, 4, '2023-06-16 14:09:47', '2023-06-16 14:09:47'),
(4, 'Phone Number', 'number', '1', '10', '10', 1, 4, '2023-06-16 14:10:23', '2023-06-16 14:10:23'),
(5, 'Name|Contact', 'textField|textField', '0|0', '25|10', '3|5', 1, 1, '2023-06-17 12:03:43', '2023-06-17 12:03:43');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `admin_name` (`admin_name`),
  ADD UNIQUE KEY `contact` (`contact`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `attendances`
--
ALTER TABLE `attendances`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`),
  ADD KEY `participantId` (`participantId`);

--
-- Indexes for table `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `event_name` (`event_name`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indexes for table `participants`
--
ALTER TABLE `participants`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `phone_number` (`phone_number`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `event_id` (`event_id`);

--
-- Indexes for table `participant_fields`
--
ALTER TABLE `participant_fields`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_EVENT` (`event_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `attendances`
--
ALTER TABLE `attendances`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `events`
--
ALTER TABLE `events`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `participants`
--
ALTER TABLE `participants`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `participant_fields`
--
ALTER TABLE `participant_fields`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendances`
--
ALTER TABLE `attendances`
  ADD CONSTRAINT `attendances_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`id`),
  ADD CONSTRAINT `attendances_ibfk_2` FOREIGN KEY (`participantId`) REFERENCES `participants` (`id`);

--
-- Constraints for table `events`
--
ALTER TABLE `events`
  ADD CONSTRAINT `events_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`id`);

--
-- Constraints for table `participants`
--
ALTER TABLE `participants`
  ADD CONSTRAINT `participants_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`);

--
-- Constraints for table `participant_fields`
--
ALTER TABLE `participant_fields`
  ADD CONSTRAINT `FK_EVENT` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
