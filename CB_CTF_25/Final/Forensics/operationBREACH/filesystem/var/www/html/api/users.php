<?php
/**
 * GridSecure Users API
 * Version: 1.0.0
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

require_once 'config.php';

// Simple authentication check
$headers = getallheaders();
$auth_token = $headers['Authorization'] ?? '';

if (empty($auth_token) || $auth_token !== 'Bearer valid-token-123') {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
    exit();
}

$method = $_SERVER['REQUEST_METHOD'];
$path = $_SERVER['REQUEST_URI'];

switch ($method) {
    case 'GET':
        if (strpos($path, '/api/users') !== false) {
            // Return list of users
            $users = [
                ['id' => 1, 'username' => 'admin', 'email' => 'admin@gridsecure.com', 'role' => 'admin'],
                ['id' => 2, 'username' => 'john_doe', 'email' => 'john@gridsecure.com', 'role' => 'user'],
                ['id' => 3, 'username' => 'jane_smith', 'email' => 'jane@gridsecure.com', 'role' => 'user']
            ];
            echo json_encode(['users' => $users]);
        } else {
            http_response_code(404);
            echo json_encode(['error' => 'Endpoint not found']);
        }
        break;
        
    case 'POST':
        // Create new user
        $data = json_decode(file_get_contents('php://input'), true);
        echo json_encode(['message' => 'User created successfully', 'id' => 5]);
        break;
        
    default:
        http_response_code(405);
        echo json_encode(['error' => 'Method not allowed']);
        break;
}
?> 