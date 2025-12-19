#!/bin/bash
   
if [ $# -lt 2 ]; then
   echo "Usage: $0 <file_to_watch> <command_to_run>"
   exit 1
fi

FILE="$1"
COMMAND="${@:2}"

if [ ! -f "$FILE" ]; then
   echo "Error: File '$FILE' does not exist"
   exit 1
fi

echo "Monitoring '$FILE' for changes..."
echo "Will execute: $COMMAND"
echo "Press Ctrl+C to stop"

while inotifywait --event attrib "$FILE"; do
   echo "Change detected! Executing command..."
   eval "$COMMAND"
done
