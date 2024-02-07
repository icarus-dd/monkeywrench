# monkeywrench
Just a collection of random tools - cli, modules, whatever works

#### CLI tools
* `env_exports_to_json.py`
  * Scan shell script(s) or STDIR, and output a JSON blob of all environment variables set.
* `mw_tee.py`
  * Functions like the *NIX `tee` command - but does not write to STDOUT unless specified
* `pretty_json_file.py`
  * Read JSON from file(s) or STDIN, print human-readable format
* `timestamp_pipe.py`
  * read STDIN from pipe, output each line prepended with a timestamp. Useful when piping STDIN to a log file, or tailing non-timestamped text. 