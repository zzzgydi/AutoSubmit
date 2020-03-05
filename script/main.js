let des = require("./des.js");
let args = process.argv.splice(2);
// console.log(args);

if (args.length > 0) {
  let rsa = args[0];
  rsa = des.strEnc(rsa, "1", "2", "3");
  console.log(rsa);
}
