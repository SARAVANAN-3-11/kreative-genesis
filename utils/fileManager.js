const fs = require("fs");
const path = require("path");

function writeCode(filePath, code) {

    const dir = path.dirname(filePath);

    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(filePath, code);
}

module.exports = { writeCode };