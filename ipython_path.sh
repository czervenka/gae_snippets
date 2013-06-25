#!/bin/bash
# Pathes remote_api_shell.py to use IPython instead of raw python interpreter


google_path=`readlink $(which remote_api_shell.py)`
google_path=$(dirname $google_path)

echo "Google Appengin found on: $google_path"

ras_path="$google_path/google/appengine/tools/remote_api_shell.py"

if [ -f "$ras_path" ]; then
    echo "Remote api shell script found at $ras_path."
    sed -i .original 's/code.interact.*$/\
  import IPython\
  from IPython.config.loader import Config\
  cfg = Config()\
  IPython.embed(config=cfg, banner2=BANNER)\
  /
  ' "$ras_path"
    if [ $? = 0 ]; then
        echo "Patched :)"
        echo "Original file can be found as remote_api_shell.py.original"
    else
        echo "Error while patching."
        exit 255
    fi
else
    echo "Could not find remote_api_shell.py script. Sorry."
fi
