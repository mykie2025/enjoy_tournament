#!/usr/bin/env node
/**
 * Script to run the frontend server using configuration from config.yml
 */

const fs = require('fs');
const yaml = require('js-yaml');
const { spawn } = require('child_process');
const path = require('path');

// Read configuration from config.yml
try {
  const configPath = path.resolve(__dirname, 'config.yml');
  const configYaml = fs.readFileSync(configPath, 'utf8');
  const config = yaml.load(configYaml);
  
  // Get frontend configuration
  const frontendConfig = config.server.frontend;
  const host = frontendConfig.host || 'localhost';
  const port = frontendConfig.port || 3000;
  
  console.log(`Starting frontend server on http://${host}:${port}`);
  
  // Set environment variables for Next.js
  const env = {
    ...process.env,
    PORT: port.toString(),
    HOST: host,
    NEXT_PUBLIC_API_HOST: config.server.api.host || 'localhost',
    NEXT_PUBLIC_API_PORT: config.server.api.port || 9000
  };
  
  // Start Next.js development server with explicit port
  const nextProcess = spawn('npm', ['run', 'dev', '--', '-p', port.toString()], {
    cwd: path.resolve(__dirname, 'frontend'),
    env,
    stdio: 'inherit'
  });
  
  nextProcess.on('error', (error) => {
    console.error(`Error starting frontend server: ${error.message}`);
    process.exit(1);
  });
  
  // Handle process termination
  process.on('SIGINT', () => {
    console.log('Stopping frontend server...');
    nextProcess.kill('SIGINT');
    process.exit(0);
  });
  
} catch (error) {
  console.error(`Error reading configuration: ${error.message}`);
  process.exit(1);
}
