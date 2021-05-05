# Changelog

All notable changes to this project should be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
