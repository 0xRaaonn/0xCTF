<?php
// GridSecure Industries - Main Page
// This is the main entry point for the web application

session_start();

// Include configuration
require_once 'includes/config/config.php';

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    header('Location: login.php');
    exit();
}

// Get user information
$user_id = $_SESSION['user_id'];
$user_name = $_SESSION['user_name'];

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GridSecure Industries</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <header>
        <h1>GridSecure Industries</h1>
        <nav>
            <a href="index.php">Home</a>
            <a href="admin/">Admin Panel</a>
            <a href="logout.php">Logout</a>
        </nav>
    </header>
    
    <main>
        <h2>Welcome, <?php echo htmlspecialchars($user_name); ?></h2>
        <p>Your critical infrastructure control dashboard is ready.</p>
        
        <div class="dashboard">
            <div class="widget">
                <h3>System Status</h3>
                <p>Monitor power grid operations and system health.</p>
            </div>
            
            <div class="widget">
                <h3>Control Systems</h3>
                <p>Access SCADA controls and infrastructure management tools.</p>
            </div>
        </div>
    </main>
    
    <footer>
        <p>&copy; 2023 GridSecure Industries. All rights reserved.</p>
    </footer>
</body>
</html> 