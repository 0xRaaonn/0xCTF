<?php
/**
 * GridSecure Admin User Management
 * Version: 2.1.4
 * Last Updated: 2023-10-10
 */

session_start();
require_once '../includes/config.php';
require_once '../includes/database.php';

// Check admin authentication
if (!isset($_SESSION['user_id']) || $_SESSION['role'] !== 'admin') {
    header('Location: ../login.php');
    exit();
}

// Handle user operations
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';
    
    switch ($action) {
        case 'create_user':
            $username = $_POST['username'] ?? '';
            $email = $_POST['email'] ?? '';
            $role = $_POST['role'] ?? 'user';
            
            echo "User created successfully";
            break;
            
        case 'delete_user':
            $user_id = $_POST['user_id'] ?? '';
            
            echo "User deleted successfully";
            break;
            
        default:
            echo "Invalid action";
    }
}

// Get users list
$users = array(
    array('id' => 1, 'username' => 'admin', 'email' => 'admin@gridsecure.com', 'role' => 'admin'),
    array('id' => 2, 'username' => 'john_doe', 'email' => 'john@gridsecure.com', 'role' => 'user'),
    array('id' => 3, 'username' => 'jane_smith', 'email' => 'jane@gridsecure.com', 'role' => 'user'),
    array('id' => 4, 'username' => 'engineer', 'email' => 'engineer@gridsecure.com', 'role' => 'engineer')
);
?>

<!DOCTYPE html>
<html>
<head>
    <title>User Management - GridSecure</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <h1>User Management</h1>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Actions</th>
        </tr>
        <?php foreach ($users as $user): ?>
        <tr>
            <td><?php echo $user['id']; ?></td>
            <td><?php echo htmlspecialchars($user['username']); ?></td>
            <td><?php echo htmlspecialchars($user['email']); ?></td>
            <td><?php echo htmlspecialchars($user['role']); ?></td>
            <td>
                <form method="post" style="display:inline;">
                    <input type="hidden" name="action" value="delete_user">
                    <input type="hidden" name="user_id" value="<?php echo $user['id']; ?>">
                    <button type="submit">Delete</button>
                </form>
            </td>
        </tr>
        <?php endforeach; ?>
    </table>
</body>
</html> 