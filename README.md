slack-pb
========

slack-pb is a simple script for pasting contents of files to the slack file
upload service.

Usage
=====

There are two ways to use the tool:

```
pb.py <filename>
```

Will send the contents of `filename` to slack. You can share it with a channel
or user with the `--channels` option.

```
pb.py <filename> --channels #my_channel,frank
```

The above will share the upload with `#my_channel` and `frank`

You can also pipe content in via stdin:

```
cat my_super_cool_file | pb.py -
```

Configuration
=============

The script requires a [slack legacy api
key](https://api.slack.com/custom-integrations/legacy-tokens). The script
expects the key to be stored in `~/.slack-token`.

The first time you specify a non-channel in the `--channels` option the script
will fetch a list of users known to you and cache the results in
`~/.slack-users.json`.
