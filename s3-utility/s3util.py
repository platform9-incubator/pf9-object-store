import sys
import boto3
import argparse

from os import environ as env

try:
    ACCESS_KEY = env['ACCESS_KEY']
    SECRET_KEY = env['SECRET_KEY']
    S3_ENDPOINT_URL = env['S3_ENDPOINT_URL']
except KeyError as ke:
    print(f'env var {ke} is not defined')
    sys.exit(1)


def get_s3_boto_session():
    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        endpoint_url=S3_ENDPOINT_URL,
    )
    return s3_client


def list_buckets(**kwargs):
    for bucket in get_s3_boto_session().list_buckets()['Buckets']:
        print("{name}\t{created}".format(
            name=bucket['Name'],
            created=bucket['CreationDate'],
        ))


def create_bucket(bucket, **kwargs):
    s3_client = get_s3_boto_session()
    print(f'creating bucket: {bucket}')
    s3_client.create_bucket(Bucket=bucket)


def delete_bucket(bucket, **kwargs):
    s3_client = get_s3_boto_session()
    print(f'deleting bucket: {bucket}')
    s3_client.delete_bucket(Bucket=bucket)


def list_bucket_objects(bucket, **kwargs):
    s3_client = get_s3_boto_session()
    bucket_objects = s3_client.list_objects(Bucket=bucket).get('Contents', None)
    if not bucket_objects:
        print('No objects in this bucket')
        return
    for obj in bucket_objects:
        print("{key}".format(key=obj['Key']))


def delete_bucket_objects(bucket, objects, **kwargs):
    s3_client = get_s3_boto_session()
    objects = [{'Key': obj.strip()} for obj in objects.split(',')]
    response = s3_client.delete_objects(Bucket=bucket, Delete={'Objects': objects})
    if "Errors" in response and len(response["Errors"]) > 0:
        print(f'failed to delete object(s); err: {response["Errors"]}')


def upload_bucket_object(bucket, file_path, dest_obj, **kwargs):
    s3_client = get_s3_boto_session()
    s3_client.upload_file(Bucket=bucket, Filename=file_path, Key=dest_obj)


def download_bucket_object(bucket, file_path, object, **kwargs):
    s3_client = get_s3_boto_session()
    s3_client.download_file(Bucket=bucket, Filename=file_path, Key=object)


def parse_args():
    parser = argparse.ArgumentParser()
    bucket_parser = argparse.ArgumentParser(description='Parser for bucket', add_help=False)
    bucket_parser.add_argument('--bucket', required=True, dest='bucket', default=None, help='bucket name')

    object_parser = argparse.ArgumentParser(description='Parser for object', add_help=False)
    object_parser.add_argument('--objects', required=True, dest='objects', default=None, help='objects')

    file_path_parser = argparse.ArgumentParser(description='Parser for file_path', add_help=False)
    file_path_parser.add_argument('--file-path', dest='file_path', required=True, default=None, help='file path')

    sub_parsers = parser.add_subparsers(help='operation to execute', dest='operation')

    # parser for list-buckets
    parser_list_buckets = sub_parsers.add_parser('list-buckets')

    # parser for create-bucket
    parser_list_buckets = sub_parsers.add_parser('create-bucket', parents=[bucket_parser])

    # parser for list-objects
    parser_list_objects = sub_parsers.add_parser('list-objects', parents=[bucket_parser])

    # parser for delete-objects
    parser_list_objects = sub_parsers.add_parser('delete-objects', parents=[bucket_parser, object_parser])

    # parser for upload-object
    parser_upload_object = sub_parsers.add_parser('upload-object', parents=[bucket_parser, file_path_parser])
    parser_upload_object.add_argument('--dest-obj', dest='dest_obj', required=True, default=None, help='dest. object')

    # parser for download-object
    parser_download_object = sub_parsers.add_parser('download-object', parents=[bucket_parser, file_path_parser])
    parser_download_object.add_argument('--object', dest='object', required=True, default=None, help='object name')

    # parser for delete-bucket
    parser_list_buckets = sub_parsers.add_parser('delete-bucket', parents=[bucket_parser])

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    op_func_map = {
        'list-buckets': list_buckets,
        'create-bucket': create_bucket,
        'list-objects': list_bucket_objects,
        'upload-object': upload_bucket_object,
        'download-object': download_bucket_object,
        'delete-objects': delete_bucket_objects,
        'delete-bucket': delete_bucket,
    }
    try:
        op_func_map[args.operation](**args.__dict__)
    except KeyError as ex:
        raise RuntimeError('Unsupported operation {}'.format(args.operation))


if __name__ == '__main__':
    main()
