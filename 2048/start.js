const Table = require("cli-table3");
const chalk = require("chalk");

const SIZE = 4;
let board;
let score;
let scoreHistory = [];

function initGame() {
  board = Array.from({ length: SIZE }, () => Array(SIZE).fill(0));
  score = 0;
  addRandomTile();
  addRandomTile();
  printBoard();
}

function addRandomTile() {
  let empty = [];
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      if (board[i][j] === 0) empty.push([i, j]);
    }
  }
  if (empty.length) {
    let [x, y] = empty[Math.floor(Math.random() * empty.length)];
    board[x][y] = Math.random() < 0.9 ? 2 : 4;
  }
}

function colorize(value) {
  if (value === 0) return chalk.gray(".");
  if (value === 2) return chalk.cyan(String(value));
  if (value === 4) return chalk.green(String(value));
  if (value === 8) return chalk.yellow(String(value));
  if (value === 16) return chalk.magenta(String(value));
  if (value === 32) return chalk.blue(String(value));
  if (value === 64) return chalk.red(String(value));
  if (value === 128) return chalk.bgCyan.black(String(value));
  if (value === 256) return chalk.bgGreen.black(String(value));
  if (value === 512) return chalk.bgYellow.black(String(value));
  if (value === 1024) return chalk.bgMagenta.black(String(value));
  if (value === 2048) return chalk.bgRed.white.bold(String(value));
  return chalk.white(String(value));
}


function printBoard() {
  console.clear();
  console.log("====================================");
  console.log("           2048 CLI GAME            ");
  console.log("          Hecho por Deph ⚡          ");
  console.log("====================================");
  console.log(`Puntaje: ${score}\n`);

  const table = new Table({
    colWidths: [8, 8, 8, 8],
    style: { head: [], border: [] }
  });

  for (let i = 0; i < SIZE; i++) {
    table.push(board[i].map(v => colorize(v)));
  }

  console.log(table.toString());

  if (scoreHistory.length) {
    console.log("\nHistorial de puntajes:");
    scoreHistory.forEach((s, i) => console.log(`Partida ${i + 1}: ${s}`));
  }
}

function slide(row) {
  row = row.filter(v => v !== 0);
  for (let i = 0; i < row.length - 1; i++) {
    if (row[i] === row[i + 1]) {
      row[i] *= 2;
      score += row[i];
      row[i + 1] = 0;
    }
  }
  row = row.filter(v => v !== 0);
  while (row.length < SIZE) row.push(0);
  return row;
}

function moveLeft() {
  for (let i = 0; i < SIZE; i++) board[i] = slide(board[i]);
}
function moveRight() {
  for (let i = 0; i < SIZE; i++) board[i] = slide(board[i].reverse()).reverse();
}
function transpose(matrix) {
  return matrix[0].map((_, i) => matrix.map(row => row[i]));
}
function moveUp() {
  board = transpose(board);
  moveLeft();
  board = transpose(board);
}
function moveDown() {
  board = transpose(board);
  moveRight();
  board = transpose(board);
}

function hasMoves() {
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      if (board[i][j] === 0) return true;
      if (j < SIZE - 1 && board[i][j] === board[i][j + 1]) return true;
      if (i < SIZE - 1 && board[i][j] === board[i + 1][j]) return true;
    }
  }
  return false;
}

function checkGameOver() {
  if (!hasMoves()) {
    console.log("\n💀 GAME OVER 💀");
    scoreHistory.push(score);
    console.log("Tu puntaje final fue:", score);
    console.log("Presiona cualquier tecla para reiniciar...");
    initGame();
  }
}

function checkWin() {
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      if (board[i][j] === 2048) {
        console.log("\n🏆 ¡GANASTE! 🏆");
        scoreHistory.push(score);
        console.log("Tu puntaje final fue:", score);
        console.log("Presiona cualquier tecla para reiniciar...");
        initGame();
      }
    }
  }
}


// Inicializar
initGame();

// Captura de teclas en tiempo real
process.stdin.setRawMode(true);
process.stdin.resume();
process.stdin.setEncoding("utf8");

process.stdin.on("data", (key) => {
  if (key === "\u0003") process.exit(); // Ctrl+C para salir

  if (key === "\u001B\u005B\u0044") moveLeft();   // ←
  if (key === "\u001B\u005B\u0043") moveRight();  // →
  if (key === "\u001B\u005B\u0041") moveUp();     // ↑
  if (key === "\u001B\u005B\u0042") moveDown();   // ↓

  addRandomTile();
  printBoard();
  checkGameOver();
  checkWin();
});
