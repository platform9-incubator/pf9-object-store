Description:

The directory has the required yamls to setup Ceph Objectstore along with a Minio UI to manage. Source: https://www.rook.io/docs/rook/v1.9/Storage-Configuration/Object-Storage-RGW/object-storage/

Steps:

1) Deploy the object store
# kubectl apply -f objectstore.yaml
# kubectl -n pf9-storage get pod -l app=rook-ceph-rgw

2) Create storage class
# kubectl apply -f sc.yaml

3) Create user with admin privileges
# kubectl apply -f user.yaml

4) Expose objectstore endpoint using NodePort
# kubectl apply -f nodeport.yaml

5) Copy user credentials for S3 client(s3testuser is the default user. Use the name as specified in user.yaml)
# kubectl get secret rook-ceph-object-user-ceph-objectstore-s3testuser -n pf9-storage -o jsonpath='{.data.SecretKey}' | base64 --decode
# kubectl get secret rook-ceph-object-user-ceph-objectstore-s3testuser -n pf9-storage -o jsonpath='{.data.AccessKey}' | base64 --decode

6) On the client side install s5cmd and create file ~/.aws/credentials with following content

[default]
aws_access_key_id=E1RZT4C8PAFI6EWJRAXH # AccessKey
aws_secret_access_key=L6FkUZ3qX1XFlCADj1YlMDaTKMYztCxYcioODTBH # SecretKey

7) Create a test bucket using s5cmd or the checked in python client

Source: https://pkg.go.dev/github.com/SilvereGit/s5cmd#section-readme

# endpoint URL is <host_public_IP>:<nodeport_IP>
# s5cmd --endpoint-url http://10.128.243.26:31813 mb s3://testbucket
# s5cmd --endpoint-url http://10.128.243.26:31813 ls

8) Deploy GUI for Object store using Minio Gateway(Minio Gateway is currently deprecated)

# kubectl apply -f minio_deployment.yaml

9) Create port forwarding to access the console. Confirm the port on which console is running via logs command

# kubectl logs minio-569ff4bb57-dtlxd --namespace minio 
# Confirm the console port from the output of above command
# nohup kubectl port-forward pod/minio-569ff4bb57-dtlxd --address 0.0.0.0 35013:35013 --namespace minio &

10) Login into the minio console using credentials(minio/Minio123)

# Below is the URL to connect
# curl http://10.128.243.26:35013
