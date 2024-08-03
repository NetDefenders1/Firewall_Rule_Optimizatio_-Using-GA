const { exec } = require('child_process');

function runPythonServer() {
    exec('python3 server.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return;
        }

        if (stderr) {
            console.error(`Python script stderr: ${stderr}`);
            return;
        }

        console.log(`Python script stdout: ${stdout}`);
    });
}

runPythonServer();
