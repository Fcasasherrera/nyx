const readline = require("readline");

const SIZE = 4;
let board = Array.from({ length: SIZE }, () => Array(SIZE).fill(0));

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

function printBoard() {
  console.clear();
  board.forEach(row => {
    console.log(row.map(v => (v === 0 ? "." : v)).join("\t"));
  });
}

function slide(row) {
  row = row.filter(v => v !== 0);
  for (let i = 0; i < row.length - 1; i++) {
    if (row[i] === row[i + 1]) {
      row[i] *= 2;
      row[i + 1] = 0;
    }
  }
  row = row.filter(v => v !== 0);
  while (row.length < SIZE) row.push(0);
  return row;
}

function moveLeft() {
  for (let i = 0; i < SIZE; i++) {
    board[i] = slide(board[i]);
  }
}

function moveRight() {
  for (let i = 0; i < SIZE; i++) {
    board[i] = slide(board[i].reverse()).reverse();
  }
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

// Inicializar
addRandomTile();
addRandomTile();
printBoard();

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.on("line", (input) => {
  if (input === "a") moveLeft();
  if (input === "d") moveRight();
  if (input === "w") moveUp();
  if (input === "s") moveDown();
  addRandomTile();
  printBoard();
});
