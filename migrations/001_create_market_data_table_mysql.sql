-- Migration: Create market_data table (MySQL/MariaDB)
-- Description: Table untuk menyimpan data hasil scraping harga saham dari Katadata
-- Created: 2025-01-22
-- Database: myorbit_market_data

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

-- Create market_data table
DROP TABLE IF EXISTS `market_data`;
CREATE TABLE `market_data` (
  -- Primary key
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

  -- Informasi emiten
  `emiten` VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `url` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,

  -- Timestamp
  `date_time_scraping` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update_text` DATETIME NULL DEFAULT NULL,

  -- Data harga
  `price` DECIMAL(18, 2) NULL DEFAULT NULL,
  `high_price` DECIMAL(18, 2) NULL DEFAULT NULL,
  `low_price` DECIMAL(18, 2) NULL DEFAULT NULL,
  `last_price` DECIMAL(18, 2) NULL DEFAULT NULL,
  `open_price` DECIMAL(18, 2) NULL DEFAULT NULL,

  -- Metadata
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` DATETIME NULL DEFAULT NULL,

  PRIMARY KEY (`id`),
  INDEX `idx_emiten` (`emiten`),
  INDEX `idx_date_time_scraping` (`date_time_scraping`),
  INDEX `idx_emiten_date` (`emiten`, `date_time_scraping`),
  INDEX `idx_last_update` (`last_update_text`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Create view untuk get latest data per emiten
DROP VIEW IF EXISTS `v_latest_market_data`;
CREATE VIEW `v_latest_market_data` AS
SELECT
    t1.id,
    t1.emiten,
    t1.url,
    t1.date_time_scraping,
    t1.last_update_text,
    t1.price,
    t1.high_price,
    t1.low_price,
    t1.last_price,
    t1.open_price,
    t1.created_at,
    t1.updated_at
FROM market_data t1
INNER JOIN (
    SELECT emiten, MAX(date_time_scraping) as max_date
    FROM market_data
    WHERE deleted_at IS NULL
    GROUP BY emiten
) t2 ON t1.emiten = t2.emiten AND t1.date_time_scraping = t2.max_date
WHERE t1.deleted_at IS NULL
ORDER BY t1.emiten;

SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
