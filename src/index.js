// index.js

const { exec } = require('child_process');

const pythonScript = 'python scraper.py';

exec(pythonScript, (error, stdout, stderr) => {
  if (error) {
    console.error(`Erro ao executar o script Python: ${error}`);
    return;
  }
  if (stderr) {
    console.error(`Erro no script Python: ${stderr}`);
    return;
  }
  console.log(`Saída do script Python:\n${stdout}`);
});
