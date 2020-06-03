# pb
**Name:** pb<br>
**Description:** Solution for Pitney Bowes's recruitment test<br>
**GitHub:** https://github.com/korniichuk/pb

## Test task
Please, see [Test-readme.md](Test-readme.md) file.

## Test solution
**Step 1:** Build an image from a Dockerfile
```
$ docker build -t korniichuk/pb .
```

**Step 2:** Use `$ docker run` command
```
$ export db=<DB>
$ export s3_bucket=<S3_BUCKET>
$ docker run -v ~/.aws:/home/pb/.aws -e db -e s3_bucket korniichuk/pb
```

Example:
```
$ export db=ruslan:passwd@demo.cluster-ro-c3rno4vis1ue.eu-central-1.rds.amazonaws.com:5432/example_db
$ export s3_bucket=example_bucket
$ docker run -v ~/.aws:/home/pb/.aws -e db -e s3_bucket korniichuk/pb
```

Where:
* `ruslan` -- database username,
* `passwd` -- database password (**Note:** Quote special characters with `\`),
* `demo.cluster-ro-c3rno4vis1ue.eu-central-1.rds.amazonaws.com` -- database host,
* `5432` -- database port,
* `example_db` -- database name,
* `example_bucket` -- name of Amazon S3 bucket.

To share the host file system, credentials, and configuration to the container, mount the host system's `~/.aws` directory to the container at `/home/pb/.aws` with the `-v` flag to the docker run command. For more information about the `-v` flag and mounting, see the [Docker reference guide](https://docs.docker.com/storage/volumes/).

**Step 3:** Verify result in Amazon S3 bucket
