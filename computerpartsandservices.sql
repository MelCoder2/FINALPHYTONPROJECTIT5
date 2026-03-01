-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 01, 2026 at 03:26 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `computerpartsandservices`
--

-- --------------------------------------------------------

--
-- Table structure for table `completed_services`
--

CREATE TABLE `completed_services` (
  `completed_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `service_type` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) DEFAULT 0.00,
  `started_at` datetime DEFAULT NULL,
  `completed_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `completed_services`
--

INSERT INTO `completed_services` (`completed_id`, `customer_id`, `full_name`, `service_type`, `description`, `price`, `started_at`, `completed_at`) VALUES
(1, 4, 'Prince Joshua Mahinay', 'Thermal Paste Repasting', '[Scheduled: 2026-02-23] none\n', 200.00, '2026-02-23 23:11:26', '2026-02-23 23:20:21'),
(2, 3, 'Prince Arvin Cabute', 'Hardware Installation', '[Scheduled: 2026-02-23] I want to install microsoft office ', 300.00, '2026-02-23 23:09:14', '2026-02-23 23:20:22'),
(3, 3, 'Prince Arvin Cabute', 'Hardware Installation', '[Scheduled: 2026-02-23] none ', 300.00, '2026-02-23 23:08:34', '2026-02-23 23:20:23'),
(4, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-23] none', 500.00, '2026-02-23 23:31:56', '2026-02-23 23:32:08');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `code` varchar(50) NOT NULL,
  `name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock_qty` int(11) NOT NULL,
  `category` varchar(50) DEFAULT 'General',
  `details` text DEFAULT NULL,
  `is_active` tinyint(4) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `code`, `name`, `price`, `stock_qty`, `category`, `details`, `is_active`) VALUES
(1, '1001', 'Ryzen 5600g', 100.00, 6, 'CPU', '', 0),
(2, '1002', 'Inplay Case', 1200.00, 4, 'CPU', '', 0),
(3, '1003', 'Ryzen 5600g', 5000.00, 11, 'CPU', '', 0),
(4, '1004', 'Inplay Case', 1200.00, 4, 'Case', '', 1),
(5, '1005', 'Razer Viper Mini', 1000.00, 8, 'Other', '', 1),
(6, '1006', 'Fantech Vx7', 500.00, 3, 'CPU', '', 1),
(7, '1007', 'G102 logitech', 800.00, 5, 'CPU', '', 1);

-- --------------------------------------------------------

--
-- Table structure for table `sales`
--

CREATE TABLE `sales` (
  `sale_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `total_price` decimal(10,2) DEFAULT NULL,
  `payment_method` varchar(50) DEFAULT 'Cash',
  `bank_name` varchar(100) DEFAULT NULL,
  `account_number` varchar(100) DEFAULT NULL,
  `sale_date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales`
--

INSERT INTO `sales` (`sale_id`, `customer_id`, `full_name`, `product_id`, `quantity`, `total_price`, `payment_method`, `bank_name`, `account_number`, `sale_date`) VALUES
(1, 2, 'Juan Dela Cruz', 3, 1, 5000.00, 'Cash on Pickup', NULL, NULL, '2026-02-23 23:15:11'),
(2, 4, 'Prince Joshua Mahinay', 3, 1, 5000.00, 'Cash on Pickup', NULL, NULL, '2026-02-23 23:15:36'),
(3, 4, 'Prince Joshua Mahinay', 4, 1, 1200.00, 'Cash on Pickup', NULL, NULL, '2026-02-23 23:15:36'),
(4, 3, 'Prince Arvin Cabute', 3, 2, 10000.00, 'Bank Transfer', 'BDO', '6767', '2026-02-23 23:16:24'),
(5, 3, 'Prince Arvin Cabute', 4, 1, 1200.00, 'Bank Transfer', 'BDO', '6767', '2026-02-23 23:16:24'),
(6, 2, 'Juan Dela Cruz', 3, 1, 5000.00, 'Cash on Pickup', NULL, NULL, '2026-02-23 23:30:04'),
(7, 2, 'Juan Dela Cruz', 4, 1, 1200.00, 'Cash on Pickup', NULL, NULL, '2026-02-23 23:30:04'),
(8, 2, 'Juan Dela Cruz', 3, 1, 5000.00, 'Bank Transfer', 'BDO (Banco de Oro)', '123', '2026-02-25 01:34:34'),
(9, 2, 'Juan Dela Cruz', 3, 1, 5000.00, 'Cash on Pickup', NULL, NULL, '2026-02-25 02:38:16'),
(10, 2, 'Juan Dela Cruz', 3, 1, 5000.00, 'Cash on Pickup', NULL, NULL, '2026-02-25 02:40:09'),
(11, 2, 'Juan Dela Cruz', 4, 1, 1200.00, 'Bank Transfer', 'Metrobank', '232', '2026-02-25 02:53:38'),
(12, 2, 'Juan Dela Cruz', 5, 1, 1000.00, 'Bank Transfer', 'Metrobank', '232', '2026-02-25 02:53:38'),
(13, 2, 'Juan Dela Cruz', 4, 1, 1200.00, 'Cash on Pickup', NULL, NULL, '2026-02-25 02:54:59'),
(14, 2, 'Juan Dela Cruz', 5, 1, 1000.00, 'Cash on Pickup', NULL, NULL, '2026-02-25 02:57:03'),
(15, 2, 'Juan Dela Cruz', 4, 1, 1200.00, 'Cash on Pickup', NULL, NULL, '2026-02-25 02:57:03'),
(16, 2, 'Juan Dela Cruz', 5, 2, 2000.00, 'Cash on Pickup', NULL, NULL, '2026-02-25 02:57:23'),
(17, 2, 'Juan Dela Cruz', 4, 2, 2400.00, 'Cash on Pickup', NULL, NULL, '2026-02-25 02:57:23'),
(18, 2, 'Juan Dela Cruz', 4, 1, 1200.00, 'Cash on Pickup', NULL, NULL, '2026-02-25 03:12:25'),
(19, 2, 'Juan Dela Cruz', 4, 1, 1200.00, 'Cash on Pickup', NULL, NULL, '2026-02-25 03:43:10'),
(20, 2, 'Juan Dela Cruz', 5, 2, 2000.00, 'Cash on Pickup', NULL, NULL, '2026-02-25 03:43:21'),
(21, 4, 'Prince Joshua Mahinay', 4, 1, 1200.00, 'Cash on Pickup', NULL, NULL, '2026-02-25 03:45:24'),
(22, 4, 'Prince Joshua Mahinay', 5, 1, 1000.00, 'Cash on Pickup', NULL, NULL, '2026-02-25 03:45:24'),
(23, 2, 'Juan Dela Cruz', 4, 1, 1200.00, 'Cash on Pickup', NULL, NULL, '2026-02-25 03:46:25'),
(24, 2, 'Juan Dela Cruz', 7, 2, 1600.00, 'Cash on Pickup', NULL, NULL, '2026-02-27 02:14:35');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `service_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `service_type` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) DEFAULT 0.00,
  `status` varchar(50) DEFAULT 'Pending',
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`service_id`, `customer_id`, `full_name`, `service_type`, `description`, `price`, `status`, `created_at`) VALUES
(5, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-23] none', 500.00, 'Completed', '2026-02-23 23:40:58'),
(6, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-23] none', 500.00, 'Completed', '2026-02-23 23:41:13'),
(7, 4, 'Prince Joshua Mahinay', 'System Reformat', '[Scheduled: 2026-02-23] ikaw na bahala\n', 500.00, 'Completed', '2026-02-23 23:48:36'),
(8, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-25] none', 500.00, 'Completed', '2026-02-25 02:38:03'),
(9, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-25] none', 500.00, 'Completed', '2026-02-25 02:38:06'),
(10, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-25] none', 500.00, 'Completed', '2026-02-25 02:38:53'),
(11, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-25] none', 500.00, 'Completed', '2026-02-25 02:40:15'),
(12, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-25] none', 500.00, 'Completed', '2026-02-25 02:53:17'),
(13, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-25] none', 500.00, 'Completed', '2026-02-25 02:53:20'),
(14, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-25] test', 500.00, 'Completed', '2026-02-25 02:57:39'),
(15, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-25] test', 500.00, 'Completed', '2026-02-25 02:57:41'),
(16, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-25] test', 500.00, 'Completed', '2026-02-25 02:57:43'),
(17, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-25] test', 500.00, 'Completed', '2026-02-25 02:57:45'),
(18, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-25] test', 500.00, 'Completed', '2026-02-25 03:40:57'),
(19, 2, 'Juan Dela Cruz', 'Troubleshooting / Diagnostics', '[Scheduled: 2026-02-25] test', 250.00, 'Completed', '2026-02-25 03:43:30'),
(20, 4, 'Prince Joshua Mahinay', 'System Reformat', '[Scheduled: 2026-02-25] test\n', 500.00, 'Completed', '2026-02-25 03:45:33'),
(21, 4, 'Prince Joshua Mahinay', 'System Reformat', '[Scheduled: 2026-02-25] test', 500.00, 'Completed', '2026-02-25 03:45:35'),
(22, 2, 'Juan Dela Cruz', 'System Reformat', '[Scheduled: 2026-02-27] test', 500.00, 'Completed', '2026-02-27 02:14:58');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(20) DEFAULT 'customer',
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `role`, `full_name`, `email`, `phone`) VALUES
(1, 'manager', '$2b$12$1.3LzwMDau0N3Ai11NGSP.oW3L9lCxPkoB2wbo1gXRlqBuuOTBIrS', 'manager', 'Store Manager', 'admin@melcom.com', '09123456789'),
(2, 'user', '$2b$12$ktRjnF4FSz5M00uz1PoFsOBf9hbJUWnLxHzT/1uUC0ZgCqBBsPed.', 'customer', 'Juan Dela Cruz', 'juan@email.com', '09187654321'),
(3, 'prince', '$2b$12$HF6iAK60AwYyF8ggpjTPu.qH20BfX2px6cFQ2pENtPs5RHZd.BviW', 'customer', 'Prince Arvin Cabute', 'cabuteprince@gmail.com', '09952126535'),
(4, 'pj123', '$2b$12$Mq5rTnHDWCmWkEMvZOrZluDP6f7loPjmjD2zUYjq8OF3h55v0yscK', 'customer', 'Prince Joshua Mahinay', 'princejoshua@gmail.com', '09329399329');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `completed_services`
--
ALTER TABLE `completed_services`
  ADD PRIMARY KEY (`completed_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `sales`
--
ALTER TABLE `sales`
  ADD PRIMARY KEY (`sale_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`service_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `completed_services`
--
ALTER TABLE `completed_services`
  MODIFY `completed_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `sales`
--
ALTER TABLE `sales`
  MODIFY `sale_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `completed_services`
--
ALTER TABLE `completed_services`
  ADD CONSTRAINT `completed_services_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `sales`
--
ALTER TABLE `sales`
  ADD CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `sales_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);

--
-- Constraints for table `services`
--
ALTER TABLE `services`
  ADD CONSTRAINT `services_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
