create database if not exists app_log;
use app_log;
CREATE TABLE if not exists comm_log (
    log_id INT UNSIGNED AUTO_INCREMENT,
    conn_id int NOT NULL,
    conn_label VARCHAR(100) NOT NULL,
    `event` VARCHAR(100) NOT NULL,
    `data` TEXT,
    `type` VARCHAR(20),
    sample_no VARCHAR(100) DEFAULT '',
    `time` DATETIME NOT NULL,
    PRIMARY KEY (log_id),
    INDEX idx_time(`time`),
    INDEX idx_time_type(`time`, `type`),
    INDEX idx_time_conn_id(`time`, conn_id),
    INDEX idx_time_type_conn_id(`time`, `type`, conn_id),
    INDEX idx_time_sample_no(`time`, sample_no),
    INDEX idx_time_type_sample_no(`time`, `type`, sample_no),
    INDEX idx_time_conn_id_sample_no(`time`, conn_id, sample_no),
    INDEX idx_time_type_conn_id_sample_no(`time`, `type`, conn_id, sample_no)
) DEFAULT CHARSET = utf8mb4;