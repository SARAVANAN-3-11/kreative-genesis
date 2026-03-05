const { spawn } = require("child_process");
const fs = require("fs");

const CODE_FOLDER = "./temp";

if(!fs.existsSync(CODE_FOLDER)){
fs.mkdirSync(CODE_FOLDER);
}

function writeCode(file,code){
fs.writeFileSync(file,code);
}

function runProgram(cmd,args,input){

return new Promise((resolve)=>{

let output="";

const process = spawn(cmd,args);

if(input){
process.stdin.write(input);
process.stdin.end();
}

process.stdout.on("data",(data)=>{
output+=data.toString();
});

process.stderr.on("data",(data)=>{
output+=data.toString();
});

process.on("close",()=>{
resolve(output);
});

});

}

/* ======================
PYTHON
====================== */

exports.runPython = async(code,input)=>{

const file=`${CODE_FOLDER}/main.py`;

writeCode(file,code);

return await runProgram("python",[file],input);

};

/* ======================
C
====================== */

exports.runC = async(code,input)=>{

const file=`${CODE_FOLDER}/main.c`;
const exe=`${CODE_FOLDER}/main_c`;

writeCode(file,code);

return new Promise((resolve)=>{

const compile = spawn("gcc",[file,"-o",exe]);

let error="";

compile.stderr.on("data",(d)=>{
error+=d.toString();
});

compile.on("close",(status)=>{

if(status!==0){
resolve(error);
return;
}

runProgram(exe,[],input).then(resolve);

});

});

};

/* ======================
CPP
====================== */

exports.runCPP = async(code,input)=>{

const file=`${CODE_FOLDER}/main.cpp`;
const exe=`${CODE_FOLDER}/main_cpp`;

writeCode(file,code);

return new Promise((resolve)=>{

const compile = spawn("g++",[file,"-o",exe]);

let error="";

compile.stderr.on("data",(d)=>{
error+=d.toString();
});

compile.on("close",(status)=>{

if(status!==0){
resolve(error);
return;
}

runProgram(exe,[],input).then(resolve);

});

});

};

/* ======================
JAVA
====================== */

exports.runJava = async(code,input)=>{

const match = code.match(/public\s+class\s+([A-Za-z0-9_]+)/);

if(!match){
return "Public class not found";
}

const className = match[1];

const file = `${CODE_FOLDER}/${className}.java`;

writeCode(file,code);

return new Promise((resolve)=>{

const compile = spawn("javac",[file]);

let error="";

compile.stderr.on("data",(d)=>{
error+=d.toString();
});

compile.on("close",(status)=>{

if(status!==0){
resolve(error);
return;
}

runProgram("java",["-cp",CODE_FOLDER,className],input)
.then(resolve);

});

});

};
