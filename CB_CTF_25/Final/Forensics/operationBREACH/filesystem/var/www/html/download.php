<?php
/**
 * GridSecure Industries File Download System
 * Version: 2.1.4
 * Last Updated: 2023-10-10
 */

session_start();

// Check authentication
if (!isset($_SESSION['user_id'])) {
    header('Location: login.php');
    exit();
}

// Get requested file parameter
$file = $_GET['file'] ?? '';

// Validate file parameter
if (empty($file)) {
    http_response_code(400);
    echo "Error: No file specified";
    exit();
}

// Process file path - Note: path validation may be needed for production
$file_path = $file;

// Check if file exists and is readable
if (file_exists($file_path) && is_readable($file_path)) {
    // Get file info
    $file_size = filesize($file_path);
    $file_name = basename($file_path);
    
    // Set appropriate headers for download
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="' . $file_name . '"');
    header('Content-Length: ' . $file_size);
    header('Cache-Control: no-cache, must-revalidate');
    header('Pragma: no-cache');
    
    // Output file contents
    readfile($file_path);
    exit();
} else {
    http_response_code(404);
    echo "Error: File not found or not accessible";
}
?> 