# Infrastructure Data Archive

## Overview

This directory contains archived infrastructure data that has been migrated to secure blob storage.

## Archive Structure

- `legacy_backup/` - Original unencrypted files (DEPRECATED)
- `encrypted_blobs/` - References to encrypted blob storage
- `access_logs/` - Historical access logs
- `audit_trails/` - Compliance audit records

## Security Notes

- All original files have been encrypted and moved to Azure Blob Storage
- Access requires proper authentication and encryption keys
- Legacy files are kept for compliance purposes only
- Direct access to archived files is blocked by .htaccess

## Migration Date

2023-10-01 - All infrastructure data migrated to encrypted storage

## Contact

For access to archived infrastructure data, contact:

- IT Security: security@gridsecure.com
- Engineering Team: engineering@gridsecure.com
- Compliance: compliance@gridsecure.com
