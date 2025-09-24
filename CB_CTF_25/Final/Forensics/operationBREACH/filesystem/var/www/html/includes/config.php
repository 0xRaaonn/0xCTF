<?php
/**
 * GridSecure Industries Main Configuration File
 * Version: 2.1.4
 * Last Updated: 2023-10-10
 */

// Database Configuration
define('DB_HOST', 'localhost');
define('DB_USER', 'gridsecure_admin');
define('DB_PASS', 'K8#mN9$vL2@qR7!pX4&jH5*wE3');
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

// Email Configuration
define('SMTP_HOST', 'smtp.gridsecure.com');
define('SMTP_PORT', 587);
define('SMTP_USER', 'noreply@gridsecure.com');
define('SMTP_PASS', 'email_password_2023');

// Cache Configuration
define('CACHE_ENABLED', true);
define('CACHE_TTL', 3600);
define('CACHE_PATH', '/var/cache/gridsecure/');

// Maintenance Mode
define('MAINTENANCE_MODE', false);
define('MAINTENANCE_IP_WHITELIST', '192.168.1.0/24');
?> 