# pf9-object-store

Objective:

`The high level goal of this idea is to showcase the ease of setting up a reliable Object storage (similar to AWS S3) cluster alongside your K8s workloads for non-prod use cases (like storing build artifacts, private container registries etc) `


What is the work involved?

- Setting up a functional Ceph S3 cluster in the DF environment through our PF9 storage operator. - Owned by Pranav
    
    https://www.rook.io/docs/rook/v1.9/Storage-Configuration/Object-Storage-RGW/object-storage/
     
     - Final Status: Done 

- Configuring a minio gateway service to frontend the CephS3 endpoint. - Owned by Pranav
   
   This can be deployed as a service in the same K8s cluster
    Note: The gateway feature seems deprecated by Minio recently. Should not be a problem though for the hackathon.
      
     - Final Status: Done, facing intermittent issues with port-forwarding though.

- Setting up a private docker registry server and configure it to store images in Ceph S3 cluster via minio - Owned by Vedant/Gaurav
   
   This can also be deployed as a service in the same k8s cluster.
    Note: Using minio in between as there seems to be some issues directly using CephS3.
     
     - Final Status: Done
  
- Go / Python based utility to perform S3 CRD operations related to User, Buckets, Objects. - Owned by Vedant/Gaurav
   
   Boto3 library which is the SDK compatible with AWS S3.
    For bucket, creation, listing of objects, deleting objects.
    For object, upload and download (read) to the bucket.
     
     - Final Status: Done
  
- Artifactory deployment with S3 backend - Owned by Gaurav.
	  
     - Final Status: Done
