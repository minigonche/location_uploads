CREATE TABLE `db_location_uploads`.`summary_prod` (
  `carnet` VARCHAR(25) NOT NULL,
  `id_entrevistado` VARCHAR(18) NOT NULL,
  `timestamp_json`BIGINT,
  `json_id` CHAR(32),
  `entrego_json`BOOLEAN DEFAULT FALSE,
  `exporto_json` BOOLEAN DEFAULT FALSE,
  `numero_registros` INT DEFAULT -1,
  `timestamp_encuesta` BIGINT,
  `entrego_encuesta` BOOLEAN DEFAULT FALSE,
  `grupo` VARCHAR(25) DEFAULT 'NINGUNO'
  );
