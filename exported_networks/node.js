let JS = require("./SimpsonsFacebookJIT.json");
const fs = require("fs");

JS = JSON.parse(JS);

fs.writeFile("./test", JSON.stringify(JS), e => {
  console.error(e);
});
