-- Infrastructure Data Database Schema
-- GridSecure Secure Infrastructure System
-- Version: 2.0.0

-- Encrypted file metadata table
CREATE TABLE encrypted_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    encrypted_blob_id VARCHAR(64) UNIQUE NOT NULL,
    file_hash VARCHAR(64) NOT NULL,
    file_size_encrypted INT NOT NULL,
    encryption_algorithm VARCHAR(32) DEFAULT 'AES-256-GCM',
    access_level ENUM('ADMIN_ONLY', 'ENGINEER_ONLY', 'OPERATOR_ONLY', 'AUDIT') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP NULL,
    status ENUM('ACTIVE', 'ARCHIVED', 'DELETED') DEFAULT 'ACTIVE'
);

-- Access control table
CREATE TABLE infrastructure_access_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    file_id INT NOT NULL,
    access_type ENUM('READ', 'WRITE', 'DELETE', 'DENIED') NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result ENUM('SUCCESS', 'DENIED', 'ERROR') NOT NULL,
    FOREIGN KEY (file_id) REFERENCES encrypted_files(id)
);

-- Sample data for encrypted files
INSERT INTO encrypted_files (file_name, encrypted_blob_id, file_hash, file_size_encrypted, access_level) VALUES
('scada_configs.zip', 'enc_scada_7f8e9d2a1b3c4e5f', 'sha256:a1b2c3d4e5f6789012345678', 156789, 'ENGINEER_ONLY'),
('grid_topology.rar', 'enc_grid_9a8b7c6d5e4f3210', 'sha256:f6e5d4c3b2a190876543210', 89543, 'OPERATOR_ONLY'),
('operator_access.txt', 'enc_op_1f2e3d4c5b6a7890', 'sha256:9876543210abcdef', 4567, 'ADMIN_ONLY');

-- Access control view
CREATE VIEW infrastructure_access_summary AS
SELECT 
    ef.file_name,
    ef.access_level,
    ef.last_accessed,
    COUNT(ial.id) as access_attempts,
    COUNT(CASE WHEN ial.result = 'SUCCESS' THEN 1 END) as successful_access
FROM encrypted_files ef
LEFT JOIN infrastructure_access_log ial ON ef.id = ial.file_id
WHERE ef.status = 'ACTIVE'
GROUP BY ef.id, ef.file_name, ef.access_level, ef.last_accessed; 