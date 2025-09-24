<?php
/**
 * GridSecure Admin Dashboard
 * Version: 1.2.0
 */

session_start();

// Check authentication
if (!isset($_SESSION['user_id'])) {
    header('Location: ../login.php');
    exit();
}

// Check admin privileges
if ($_SESSION['role'] !== 'admin') {
    header('Location: ../index.php');
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GridSecure Admin Dashboard</title>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>GridSecure Admin Dashboard</h1>
            <nav>
                <a href="users.php">User Management</a>
                <a href="settings.php">System Settings</a>
                <a href="logs.php">System Logs</a>
                <a href="../logout.php">Logout</a>
            </nav>
        </header>
        
        <main>
            <div class="dashboard-stats">
                <div class="stat-card">
                    <h3>Active Users</h3>
                    <p>1,247</p>
                </div>
                <div class="stat-card">
                    <h3>System Status</h3>
                    <p class="status-ok">Online</p>
                </div>
                <div class="stat-card">
                    <h3>Last Backup</h3>
                    <p>2024-01-15 02:00:00</p>
                </div>
            </div>
        </main>
    </div>
</body>
</html> 