<?php
/**
 * GridSecure API Configuration
 * Version: 1.0.0
 */

// Database configuration
define('DB_HOST', 'localhost');
define('DB_NAME', 'gridsecure_infrastructure');
define('DB_USER', 'gridsecure_admin');
define('DB_PASS', 'K8#mN9$vL2@qR7!pX4&jH5*wE3');

// API configuration
define('API_VERSION', 'v1');
define('API_RATE_LIMIT', 1000); // requests per hour
define('API_TIMEOUT', 30); // seconds

// Security settings
define('JWT_SECRET', 'xK9#mN2$vL8@qR4!pX7&jH1*wE6#sT3$yU5@iO9!kP2&lQ8*mW4#nX6$vY1@zA7!bB3&cC9*dD5#eE2$fF8@gG4!hH1&iI6*jJ3#kK9$lL5@mM2!nN8&oO4*pP1#qQ7$rR3@sS9!tT5&uU2*vV8#wW4$xX1@yY6!zZ3&aA9*bB5#cC2$dD8@eE4!fF1&gG7*hH3#iI9$jJ5@kK2!lL8&mM4*nN1#oO7$pP3@qQ9!rR5&sS2*tT8#uU4$vV1@wW6!xX3&yY9*zZ5');
define('CORS_ORIGIN', 'https://gridsecure.com');

// Logging configuration
define('LOG_LEVEL', 'INFO');
define('LOG_FILE', '/var/log/gridsecure/api.log');

// Feature flags
define('ENABLE_DEBUG_MODE', false);
define('ENABLE_MAINTENANCE_MODE', false);
define('ENABLE_RATE_LIMITING', true);

// External services
define('SMTP_HOST', 'smtp.gridsecure.com');
define('SMTP_PORT', 587);
define('SMTP_USER', 'noreply@gridsecure.com');
define('SMTP_PASS', 'H7#jK4$mN9@qR2!pX6&vL8*wE1#sT5$yU3@iO7!kP4&lQ1*mW9#nX3$vY6@zA2!bB8&cC4*dD7#eE1$fF5@gG9!hH3&iI8*jJ2#kK6$lL1@mM5!nN9&oO3*pP7#qQ1$rR5@sS9!tT3&uU7*vV1#wW5$xX9@yY3!zZ7&aA1*bB5#cC9$dD3@eE7!fF1&gG5*hH9#iI3$jJ7@kK1!lL5&mM9*nN3#oO7$pP1@qQ5!rR9&sS3*tT7#uU1$vV5@wW9!xX3&yY7*zZ1');

// Backup configuration
define('BACKUP_ENABLED', true);
define('BACKUP_RETENTION_DAYS', 30);
define('BACKUP_PATH', '/var/backups/gridsecure/');
?> 