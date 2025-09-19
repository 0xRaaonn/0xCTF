<?php
// GridSecure Industries - Utility Functions
// Common utility functions used throughout the application

require_once 'config/config.php';

/**
 * Sanitize user input
 */
function sanitize_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

/**
 * Validate email address
 */
function is_valid_email($email) {
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}

/**
 * Generate random token
 */
function generate_token($length = 32) {
    return bin2hex(random_bytes($length));
}

/**
 * Check if user is logged in
 */
function is_logged_in() {
    return isset($_SESSION['user_id']);
}

/**
 * Redirect to specified URL
 */
function redirect($url) {
    header("Location: $url");
    exit();
}

/**
 * Log user activity
 */
function log_activity($user_id, $action, $details = '') {
    global $db;
    
    $sql = "INSERT INTO user_activity (user_id, action, details, ip_address, created_at) 
            VALUES (?, ?, ?, ?, NOW())";
    
    $params = array($user_id, $action, $details, $_SERVER['REMOTE_ADDR']);
    return $db->query($sql, $params);
}

/**
 * Format currency
 */
function format_currency($amount) {
    return '$' . number_format($amount, 2);
}

/**
 * Get current timestamp
 */
function get_current_timestamp() {
    return date('Y-m-d H:i:s');
}

/**
 * Validate file upload
 */
function validate_file_upload($file) {
    $allowed_types = ALLOWED_FILE_TYPES;
    $max_size = MAX_UPLOAD_SIZE;
    
    if ($file['size'] > $max_size) {
        return false;
    }
    
    $file_extension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    if (!in_array($file_extension, $allowed_types)) {
        return false;
    }
    
    return true;
}
?> 