#!/bin/bash

# Start the server in the background
echo "Starting the server..."
honcho start &
SERVER_PID=$!

# Wait for the server to start
echo "Waiting for the server to start..."
sleep 5

# Run the behave tests
echo "Running behave tests..."
behave

# Capture the exit code
BEHAVE_EXIT_CODE=$?

# Kill the server
echo "Stopping the server..."
kill $SERVER_PID

# Exit with the behave exit code
exit $BEHAVE_EXIT_CODE
