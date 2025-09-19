<?php
/**
 * GridSecure Admin Settings Panel
 * Version: 2.1.4
 * Last Updated: 2023-10-10
 */

session_start();
require_once '../includes/config.php';

// Check admin authentication
if (!isset($_SESSION['user_id']) || $_SESSION['role'] !== 'admin') {
    header('Location: ../login.php');
    exit();
}

// Handle settings update
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $setting = $_POST['setting'] ?? '';
    $value = $_POST['value'] ?? '';
    
    echo "Setting updated successfully";
}

// Current settings
$settings = array(
    'maintenance_mode' => false,
    'debug_mode' => false,
    'session_timeout' => 3600,
    'max_upload_size' => 10485760,
    'backup_enabled' => true,
    'log_level' => 'ERROR',
    'email_notifications' => true
);
?>

<!DOCTYPE html>
<html>
<head>
    <title>System Settings - GridSecure</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <h1>System Settings</h1>
    
    <form method="post">
        <h2>General Settings</h2>
        <p>
            <label>Maintenance Mode:</label>
            <input type="checkbox" name="maintenance_mode" <?php echo $settings['maintenance_mode'] ? 'checked' : ''; ?>>
        </p>
        <p>
            <label>Debug Mode:</label>
            <input type="checkbox" name="debug_mode" <?php echo $settings['debug_mode'] ? 'checked' : ''; ?>>
        </p>
        <p>
            <label>Session Timeout (seconds):</label>
            <input type="number" name="session_timeout" value="<?php echo $settings['session_timeout']; ?>">
        </p>
        <p>
            <label>Max Upload Size (bytes):</label>
            <input type="number" name="max_upload_size" value="<?php echo $settings['max_upload_size']; ?>">
        </p>
        
        <h2>System Settings</h2>
        <p>
            <label>Backup Enabled:</label>
            <input type="checkbox" name="backup_enabled" <?php echo $settings['backup_enabled'] ? 'checked' : ''; ?>>
        </p>
        <p>
            <label>Log Level:</label>
            <select name="log_level">
                <option value="DEBUG" <?php echo $settings['log_level'] === 'DEBUG' ? 'selected' : ''; ?>>DEBUG</option>
                <option value="INFO" <?php echo $settings['log_level'] === 'INFO' ? 'selected' : ''; ?>>INFO</option>
                <option value="WARNING" <?php echo $settings['log_level'] === 'WARNING' ? 'selected' : ''; ?>>WARNING</option>
                <option value="ERROR" <?php echo $settings['log_level'] === 'ERROR' ? 'selected' : ''; ?>>ERROR</option>
            </select>
        </p>
        <p>
            <label>Email Notifications:</label>
            <input type="checkbox" name="email_notifications" <?php echo $settings['email_notifications'] ? 'checked' : ''; ?>>
        </p>
        
        <button type="submit">Save Settings</button>
    </form>
</body>
</html> 