-- Migration Rollback: Drop market_data table (MySQL/MariaDB)
-- Description: Rollback migration untuk menghapus market_data table
-- Created: 2025-01-22

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

-- Drop view
DROP VIEW IF EXISTS `v_latest_market_data`;

-- Drop table
DROP TABLE IF EXISTS `market_data`;

SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
