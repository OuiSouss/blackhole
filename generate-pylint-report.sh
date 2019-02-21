#!/bin/sh

pylint --rcfile=project/.pylintrc $(find project/backend project/frontend -iname "*.py" -print) -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint-report.txt || exit 0