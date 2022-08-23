# Setup Jfrog artifactory with CephS3 storage backend
1. Refer https://jfrog.com/artifactory/install to install the artifactory on a VM
2. Replace the `/var/opt/jfrog/artifactory/etc/artifactory/binarystore.xml` file on artifactory VM with the file <br>
   `binarystore.xml` present in this folder.
   update the ceph s3 details/creds in binarystore.xml as necessary and restart artifactory service <br>
   `systemctl restart artifactory`

