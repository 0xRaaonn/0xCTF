<?php
/**
 * GridSecure File Upload Handler
 * Version: 1.0.0
 */

session_start();

// Check authentication
if (!isset($_SESSION['user_id'])) {
    header('Location: ../login.php');
    exit();
}

$upload_dir = 'uploads/';
$max_file_size = 10 * 1024 * 1024; // 10MB

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $file = $_FILES['file'];
    
    // Basic file validation
    if ($file['error'] !== UPLOAD_ERR_OK) {
        $error = "Upload failed with error code: " . $file['error'];
    } elseif ($file['size'] > $max_file_size) {
        $error = "File too large. Maximum size is 10MB.";
    } else {
        // Create upload directory if it doesn't exist
        if (!is_dir($upload_dir)) {
            mkdir($upload_dir, 0755, true);
        }
        
        $filename = basename($file['name']);
        $target_path = $upload_dir . $filename;
        
        if (move_uploaded_file($file['tmp_name'], $target_path)) {
            $success = "File uploaded successfully: " . $filename;
        } else {
            $error = "Failed to move uploaded file.";
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Upload - GridSecure</title>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>File Upload</h1>
            <nav>
                <a href="../index.php">Home</a>
                <a href="../dashboard/">Dashboard</a>
            </nav>
        </header>
        
        <main>
            <?php if (isset($error)): ?>
                <div class="alert alert-error"><?= $error ?></div>
            <?php endif; ?>
            
            <?php if (isset($success)): ?>
                <div class="alert alert-success"><?= $success ?></div>
            <?php endif; ?>
            
            <form method="POST" enctype="multipart/form-data" class="upload-form">
                <div class="form-group">
                    <label for="file">Select File:</label>
                    <input type="file" id="file" name="file" required>
                </div>
                
                <button type="submit">Upload File</button>
            </form>
            
            <div class="upload-info">
                <h3>Upload Information</h3>
                <ul>
                    <li>Maximum file size: 10MB</li>
                    <li>Supported formats: All</li>
                    <li>Files are stored in: <?= $upload_dir ?></li>
                </ul>
            </div>
        </main>
    </div>
</body>
</html> 