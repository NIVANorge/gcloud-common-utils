# Changelog

All notable changes to this project should be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2021-10-27

- blob_helper_local.upload_file seeking file to position 0
    
this prevents empty files from being uploaded in cases where the file pointer/cursor is at the end

## [0.4.0] - 2021-06-02

- pubsub_helpers: generate a unique span id per message using UUID.uuid4() function

## [0.3.1] - 2021-05-05

- fixed subscriber.acknowledge to use named parameters, fixing breaking change in 2.0.0

This fixes the following error when trying to ack a message:

```
....
google/cloud/pubsub_v1/_gapic.py", line 40, in <lambda>
    fx = lambda self, *a, **kw: wrapped_fx(self.api, *a, **kw)  # noqa
TypeError: acknowledge() takes from 1 to 2 positional arguments but 3 were given
```

## [0.3.0] - 2021-05-03

- Setup logcontext with trace_id from message attributes, if present.
- updated pubsub version range to only allow version >2.0.0



## Previous changes

This is the start of changelog, changes prior to version 0.3.0 are only documented in git history.
