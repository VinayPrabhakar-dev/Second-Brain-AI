import click

from second_brain_offline.infrastructure.aws.s3 import S3Client

@click.group()
def cli() -> None:
    """CLI too for uploading and downloading folders to/from S3."""
    pass

@cli.command()
@click.argument("local_path")
@click.argument("bucket_name")
@click.option("--s3-prefix", default="", help="Optional S3 prefix (folder path)")
def upload(local_path: str, bucket_name: str, s3_prefix: str) -> None:
    try:
        s3_client = S3Client(bucket_name)
        s3_client.upload_folder(local_path, s3_prefix)
        click.echo(
            f"Successfully uploaded '{local_path}' to 's3://{bucket_name}/{s3_prefix}'"
        )

    except Exception as e:
        click.echo(f"Error: {str(e)}", err = True)
        raise click.Abort()
    

@cli.command()
@click.argument("bucket_name")
@click.argument("s3_path")
@click.argument("local_path")
@click.option(
    "--no-sign-request",
    is_flag=True,
    help="If True will access S3 un-authenticated for public buckets",
)
def download(
    bucket_name: str, s3_path: str, local_path: str, no_sign_request: bool
) -> None:
    try:
        s3_client = S3Client(bucket_name, no_sign_request=no_sign_request)
        s3_client.download_folder(s3_path, local_path)
        click.echo(
            f"Successfully downloaded 's3://{bucket_name}/{s3_path}' to '{local_path}'"
        )
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()
    
if __name__ == "__main__":
    cli()