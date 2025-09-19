<?php
/**
 * GridSecure Admin Settings
 * Version: 1.1.0
 */

session_start();

// Check authentication and admin privileges
if (!isset($_SESSION['user_id']) || $_SESSION['role'] !== 'admin') {
    header('Location: ../login.php');
    exit();
}

// Handle form submission
if ($_POST) {
    $message = "Settings updated successfully!";
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Settings - GridSecure Admin</title>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>System Settings</h1>
            <nav>
                <a href="index.php">Dashboard</a>
                <a href="users.php">User Management</a>
                <a href="logs.php">System Logs</a>
            </nav>
        </header>
        
        <main>
            <form method="POST" class="settings-form">
                <div class="form-group">
                    <label for="site_name">Site Name</label>
                    <input type="text" id="site_name" name="site_name" value="GridSecure Industries">
                </div>
                
                <div class="form-group">
                    <label for="maintenance_mode">Maintenance Mode</label>
                    <select id="maintenance_mode" name="maintenance_mode">
                        <option value="0">Disabled</option>
                        <option value="1">Enabled</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="session_timeout">Session Timeout (minutes)</label>
                    <input type="number" id="session_timeout" name="session_timeout" value="30">
                </div>
                
                <div class="form-group">
                    <label for="backup_frequency">Backup Frequency</label>
                    <select id="backup_frequency" name="backup_frequency">
                        <option value="daily">Daily</option>
                        <option value="weekly">Weekly</option>
                        <option value="monthly">Monthly</option>
                    </select>
                </div>
                
                <button type="submit">Save Settings</button>
            </form>
        </main>
    </div>
</body>
</html> 