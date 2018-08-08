CREATE TABLE `db_location_uploads`.`locations_dev` (
  `carnet` VARCHAR(25) NOT NULL,
  `id_entrevistado` VARCHAR(25) NOT NULL,
  `timestamp` INT UNSIGNED NULL,
  `latitude` INT NULL,
  `longitude` INT NULL,
  `accuracy` MEDIUMINT UNSIGNED NULL,
  `velocity` SMALLINT UNSIGNED NULL,
  `altitude` SMALLINT UNSIGNED NULL,
  `vertical_accuracy` MEDIUMINT UNSIGNED NULL,
  `activity_timestamp` INT UNSIGNED NULL,
  `activity` VARCHAR(3) NULL,
  `activity_confidence` TINYINT UNSIGNED NULL);
