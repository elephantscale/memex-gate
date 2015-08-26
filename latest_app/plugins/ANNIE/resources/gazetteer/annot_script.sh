#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do	
	echo "{Token.string == \"$line\"} |" >> output.list
done < "$1"
