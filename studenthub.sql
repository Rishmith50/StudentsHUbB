

CREATE DATABASE IF NOT EXISTS `studenthub` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `studenthub`;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `attendance`;
DROP TABLE IF EXISTS `fees`;
DROP TABLE IF EXISTS `students`;
DROP TABLE IF EXISTS `courses`;
DROP TABLE IF EXISTS `users`;

SET FOREIGN_KEY_CHECKS = 1;

-- Table structure for table `users`
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(20) DEFAULT 'admin',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `courses`
CREATE TABLE `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `students`
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `course_id` int NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `enrollment_date` date DEFAULT (curdate()),
  `status` varchar(20) NOT NULL DEFAULT 'Active',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `fk_student_course` (`course_id`),
  CONSTRAINT `fk_student_course` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `attendance`
CREATE TABLE `attendance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `attendance_date` date NOT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'Present',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_student_date` (`student_id`,`attendance_date`),
  CONSTRAINT `fk_attendance_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `fees`
CREATE TABLE `fees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `total_fee` decimal(10,2) NOT NULL DEFAULT '50000.00',
  `amount_paid` decimal(10,2) NOT NULL DEFAULT '0.00',
  `last_payment_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_id` (`student_id`),
  CONSTRAINT `fk_fees_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



-- Dumping data for table `users`
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `role`, `created_at`) VALUES
(1, 'admin', 'admin@studenthub.local', 'scrypt:32768:8:1$q1paDQrywBoqVp9f$43fda6e57ec3bd4f6c8a04092b5b79240ad913262eea69b044e7bbeadaddaf77e103cc51ac51134fa7fe5b353bf00499058d7d6c285e4a73f2294bf7202efc01', 'admin', '2026-10-05 22:08:21');

-- Dumping data for table `courses`
INSERT INTO `courses` (`id`, `name`) VALUES
(5, 'BBA'),
(1, 'BCA'),
(2, 'BSc IT'),
(4, 'BTech Computer Science'),
(3, 'MCA'),
(6, 'MCom');

-- Dumping data for table `students`
INSERT INTO `students` (`id`, `name`, `email`, `phone`, `gender`, `course_id`, `date_of_birth`, `enrollment_date`, `status`) VALUES
(1, 'Rahul Sharma', 'rahul@example.com', '9876543210', 'Male', 1, '2002-04-12', '2025-06-15', 'Inactive'),
(2, 'Ayesha Khan', 'ayesha@example.com', '9123456789', 'Female', 2, '2003-08-21', '2025-06-18', 'Active'),
(3, 'Arjun Mehta', 'arjun@example.com', '9988776655', 'Male', 1, '2002-11-10', '2025-06-20', 'Active'),
(4, 'Emily Davis', 'emily@example.com', '9876501234', 'Female', 4, '2001-05-14', '2025-06-22', 'Inactive'),
(5, 'Chris Wilson', 'chris@example.com', '9765432109', 'Male', 3, '2002-01-25', '2025-06-25', 'Active'),
(6, 'Sara Patel', 'sara@example.com', '9898989898', 'Female', 5, '2003-03-17', '2025-07-01', 'Active'),
(7, 'Kabir Shah', 'kabir@example.com', '9000011111', 'Male', 2, '2002-09-09', '2025-07-03', 'Inactive'),
(8, 'Maya Thomas', 'maya@example.com', '9888877777', 'Female', 6, '2001-12-04', '2025-07-05', 'Active'),
(17, 'Neha Kapoor', 'neha@example.com', '9111122222', 'Female', 1, '2003-02-10', '2026-10-05', 'Active'),
(18, 'Rishmith', 'rishmith123@gmail.com', '8452857190', 'Male', 4, '2006-11-20', '2026-10-05', 'Active');

-- Dumping data for table `attendance`
INSERT INTO `attendance` (`id`, `student_id`, `attendance_date`, `status`) VALUES
(1, 2, '2026-10-04', 'Present'),
(2, 3, '2026-10-04', 'Present'),
(3, 5, '2026-10-04', 'Present'),
(4, 6, '2026-10-04', 'Present'),
(5, 8, '2026-10-04', 'Absent'),
(6, 17, '2026-10-04', 'Present'),
(7, 18, '2026-10-04', 'Present'),
(8, 2, '2026-10-03', 'Present'),
(9, 3, '2026-10-03', 'Absent'),
(10, 5, '2026-10-03', 'Present'),
(11, 6, '2026-10-03', 'Absent'),
(12, 8, '2026-10-03', 'Present'),
(13, 17, '2026-10-03', 'Present'),
(14, 18, '2026-10-03', 'Absent'),
(22, 2, '2026-10-05', 'Present'),
(23, 3, '2026-10-05', 'Present'),
(24, 5, '2026-10-05', 'Present'),
(25, 6, '2026-10-05', 'Present'),
(26, 8, '2026-10-05', 'Present'),
(27, 17, '2026-10-05', 'Present'),
(28, 18, '2026-10-05', 'Present');

-- Dumping data for table `fees`
INSERT INTO `fees` (`id`, `student_id`, `total_fee`, `amount_paid`, `last_payment_date`) VALUES
(1, 1, '50000.00', '50000.00', '2026-10-05'),
(2, 3, '50000.00', '50000.00', '2026-10-05'),
(3, 17, '50000.00', '0.00', NULL),
(4, 2, '50000.00', '20200.00', '2026-10-05'),
(5, 7, '50000.00', '0.00', NULL),
(6, 5, '50000.00', '20000.00', '2026-10-05'),
(7, 4, '50000.00', '0.00', NULL),
(8, 18, '50000.00', '0.00', NULL),
(9, 6, '50000.00', '0.00', NULL),
(10, 8, '50000.00', '50000.00', '2026-10-05');
