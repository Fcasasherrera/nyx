// reloj-arcade.js
import readline from 'readline';
import chalk from 'chalk';

const numbers = {
  "0": [
    " ███ ",
    "█   █",
    "█   █",
    "█   █",
    " ███ "
  ],
  "1": [
    "  █  ",
    " ██  ",
    "  █  ",
    "  █  ",
    " ███ "
  ],
  "2": [
    " ███ ",
    "    █",
    " ███ ",
    "█    ",
    "█████"
  ],
  "3": [
    " ███ ",
    "    █",
    " ███ ",
    "    █",
    " ███ "
  ],
  "4": [
    "█   █",
    "█   █",
    "█████",
    "    █",
    "    █"
  ],
  "5": [
    "█████",
    "█    ",
    "████ ",
    "    █",
    "████ "
  ],
  "6": [
    " ███ ",
    "█    ",
    "████ ",
    "█   █",
    " ███ "
  ],
  "7": [
    "█████",
    "    █",
    "   █ ",
    "  █  ",
    "  █  "
  ],
  "8": [
    " ███ ",
    "█   █",
    " ███ ",
    "█   █",
    " ███ "
  ],
  "9": [
    " ███ ",
    "█   █",
    " ████",
    "    █",
    " ███ "
  ],
  ":": [
    "     ",
    "  █  ",
    "     ",
    "  █  ",
    "     "
  ]
};

let showColon = true;

function drawTime() {
  readline.cursorTo(process.stdout, 0, 0);
  readline.clearScreenDown(process.stdout);

  const now = new Date();
  const timeStr = now.toLocaleTimeString("es-MX", { hour12: false });

  const lines = ["", "", "", "", ""];
  for (const char of timeStr) {
    const digitLines = numbers[char];
    digitLines.forEach((line, i) => {
      if (char === ":" && !showColon) {
        lines[i] += "     " + "  "; // espacio cuando parpadea
      } else {
        // Verde retro estilo arcade
        lines[i] += chalk.greenBright(line) + "  ";
      }
    });
  }

  console.log(lines.join("\n"));
  showColon = !showColon; // alterna el parpadeo
}

setInterval(drawTime, 1000);
