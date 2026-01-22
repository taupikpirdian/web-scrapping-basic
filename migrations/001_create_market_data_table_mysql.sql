CREATE TABLE market_data (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `emiten` VARCHAR(10) NOT NULL,
  `url` TEXT NOT NULL,
  `date_time_scraping` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update_text` DATETIME NULL,
  `price` DECIMAL(18,2) NULL,
  `high_price` DECIMAL(18,2) NULL,
  `low_price` DECIMAL(18,2) NULL,
  `last_price` DECIMAL(18,2) NULL,
  `open_price` DECIMAL(18,2) NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_emiten_date` (`emiten`, `date_time_scraping`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE VIEW v_latest_market_data AS
SELECT md.*
FROM market_data md
INNER JOIN (
    SELECT emiten, MAX(id) AS max_id
    FROM market_data
    WHERE deleted_at IS NULL
    GROUP BY emiten
) latest
ON md.id = latest.max_id
WHERE md.deleted_at IS NULL;
