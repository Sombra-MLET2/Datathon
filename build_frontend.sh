#!/bin/bash

cd frontend

echo "Installing frontend dependencies..."
npm install

echo "Building React app..."
npm run build

echo "Frontend build complete!"
