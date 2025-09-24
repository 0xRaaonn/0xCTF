<?php
/**
 * GridSecure Industries System Configuration Backup
 * Generated: 2023-10-10 06:14:00
 * Version: 2.1.4
 * Backup ID: GS-BKP-2023-10-10-001
 */

// Database Configuration
define('DB_HOST', 'localhost');
define('DB_USER', 'gridsecure_admin');
define('DB_PASS', 'GridSecure2024!');
define('DB_NAME', 'gridsecure_infrastructure');
define('DB_PORT', 3306);

// Application Settings
define('APP_NAME', 'GridSecure Industries Infrastructure Portal');
define('APP_VERSION', '2.1.4');
define('APP_ENV', 'production');
define('DEBUG_MODE', false);

// Security Configuration
define('SESSION_TIMEOUT', 3600);
define('MAX_LOGIN_ATTEMPTS', 5);
define('PASSWORD_MIN_LENGTH', 8);

// File Upload Settings
define('MAX_UPLOAD_SIZE', 10485760); // 10MB
define('ALLOWED_EXTENSIONS', 'pdf,doc,docx,xlsx,xls');

// API Configuration
define('API_VERSION', 'v1');
define('API_RATE_LIMIT', 100);
define('API_KEY_EXPIRY', 86400);

// Logging Configuration
define('LOG_LEVEL', 'ERROR');
define('LOG_FILE', '/var/log/gridsecure/app.log');
define('LOG_MAX_SIZE', 52428800); // 50MB

// Backup Configuration
define('BACKUP_ENABLED', true);
define('BACKUP_RETENTION_DAYS', 30);
define('BACKUP_PATH', '/var/backups/gridsecure/');

// Email Configuration
define('SMTP_HOST', 'smtp.gridsecure.com');
define('SMTP_PORT', 587);
define('SMTP_USER', 'noreply@gridsecure.com');
define('SMTP_PASS', 'H7#jK4$mN9@qR2!pX6&vL8*wE1#sT5$yU3@iO7!kP4&lQ1*mW9#nX3$vY6@zA2!bB8&cC4*dD7#eE1$fF5@gG9!hH3&iI8*jJ2#kK6$lL1@mM5!nN9&oO3*pP7#qQ1$rR5@sS9!tT3&uU7*vV1#wW5$xX9@yY3!zZ7&aA1*bB5#cC9$dD3@eE7!fF1&gG5*hH9#iI3$jJ7@kK1!lL5&mM9*nN3#oO7$pP1@qQ5!rR9&sS3*tT7#uU1$vV5@wW9!xX3&yY7*zZ1');

// Cache Configuration
define('CACHE_ENABLED', true);
define('CACHE_TTL', 3600);
define('CACHE_PATH', '/var/cache/gridsecure/');

// Maintenance Mode
define('MAINTENANCE_MODE', false);
define('MAINTENANCE_IP_WHITELIST', '192.168.1.0/24');
?> 