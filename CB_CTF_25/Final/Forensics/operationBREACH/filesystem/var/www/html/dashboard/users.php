<?php
/**
 * GridSecure User Management
 * Version: 1.0.0
 */

session_start();

// Check authentication and admin privileges
if (!isset($_SESSION['user_id']) || $_SESSION['role'] !== 'admin') {
    header('Location: ../login.php');
    exit();
}

// Mock user data
$users = [
    ['id' => 1, 'username' => 'admin', 'email' => 'admin@gridsecure.com', 'role' => 'admin', 'status' => 'active'],
    ['id' => 2, 'username' => 'john_doe', 'email' => 'john@gridsecure.com', 'role' => 'user', 'status' => 'active'],
    ['id' => 3, 'username' => 'jane_smith', 'email' => 'jane@gridsecure.com', 'role' => 'user', 'status' => 'inactive'],
    ['id' => 4, 'username' => 'engineer', 'email' => 'engineer@gridsecure.com', 'role' => 'engineer', 'status' => 'active']
];
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Management - GridSecure Admin</title>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>User Management</h1>
            <nav>
                <a href="index.php">Dashboard</a>
                <a href="settings.php">System Settings</a>
                <a href="logs.php">System Logs</a>
            </nav>
        </header>
        
        <main>
            <div class="user-actions">
                <button class="btn-primary">Add New User</button>
                <button class="btn-secondary">Export Users</button>
            </div>
            
            <table class="user-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($users as $user): ?>
                    <tr>
                        <td><?= $user['id'] ?></td>
                        <td><?= $user['username'] ?></td>
                        <td><?= $user['email'] ?></td>
                        <td><?= $user['role'] ?></td>
                        <td><span class="status-<?= $user['status'] ?>"><?= $user['status'] ?></span></td>
                        <td>
                            <button class="btn-small">Edit</button>
                            <button class="btn-small btn-danger">Delete</button>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </main>
    </div>
</body>
</html> 