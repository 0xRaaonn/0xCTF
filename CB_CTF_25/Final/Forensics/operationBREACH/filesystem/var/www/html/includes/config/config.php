<?php
// GridSecure Industries - Main Configuration
// Database and application configuration

// Database configuration
define('DB_HOST', 'localhost');
define('DB_NAME', 'gridsecure_infrastructure');
define('DB_USER', 'gridsecure_admin');
define('DB_PASS', 'K8#mN9$vL2@qR7!pX4&jH5*wE3');

// Application configuration
define('APP_NAME', 'GridSecure Industries');
define('APP_VERSION', '1.0.0');
define('APP_URL', 'https://gridsecure.com');

// Security settings
define('SESSION_TIMEOUT', 3600); // 1 hour
define('MAX_LOGIN_ATTEMPTS', 5);
define('PASSWORD_MIN_LENGTH', 8);

// File upload settings
define('MAX_UPLOAD_SIZE', 5242880); // 5MB
define('ALLOWED_FILE_TYPES', ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx']);

// Error reporting
error_reporting(E_ALL);
ini_set('display_errors', 0);
ini_set('log_errors', 1);
ini_set('error_log', '/var/log/php/error.log');

// Timezone
date_default_timezone_set('UTC');

// Start session if not already started
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?> 