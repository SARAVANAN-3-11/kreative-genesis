const languageSelect = document.getElementById("language");
const fileNameBox = document.getElementById("filename");
const outputBox = document.getElementById("output");
const inputBox = document.getElementById("input");
const runBtn = document.getElementById("runBtn");

let editor;

/* =========================
CODE TEMPLATES
========================= */

const templates = {

java:`public class Main {

    public static void main(String[] args){

        System.out.println("Hello World");

    }

}`,

python:`print("Hello World")`,

c:`#include<stdio.h>

int main(){

    printf("Hello World");

    return 0;

}`,

cpp:`#include<iostream>
using namespace std;

int main(){

    cout<<"Hello World";

    return 0;

}`
};

/* =========================
MONACO EDITOR
========================= */

require.config({
paths:{vs:"https://unpkg.com/monaco-editor@0.45.0/min/vs"}
});

require(["vs/editor/editor.main"],function(){

editor = monaco.editor.create(document.getElementById("editor"),{

value:templates.java,
language:"java",
theme:"vs-dark",
automaticLayout:true,
minimap:{enabled:false},
fontSize:14

});

/* set initial filename */

updateFileName();

/* language switch */

languageSelect.addEventListener("change",changeLanguage);

/* detect typing */

editor.onDidChangeModelContent(function(){

updateFileName();

});

/* CTRL + ENTER RUN */

editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, function () {
runCode();
});

});

/* =========================
LANGUAGE CHANGE
========================= */

function changeLanguage(){

const lang = languageSelect.value;

monaco.editor.setModelLanguage(editor.getModel(),lang);

editor.setValue(templates[lang]);

updateFileName();

}

/* =========================
FILE NAME LOGIC
========================= */

function updateFileName(){

if(!editor) return;

const lang = languageSelect.value;

const code = editor.getValue();

/* JAVA dynamic */

if(lang==="java"){

const match = code.match(/public\s+class\s+([A-Za-z0-9_]+)/);

if(match){

fileNameBox.textContent = match[1] + ".java";

}else{

fileNameBox.textContent = "Main.java";

}

}

/* STATIC FILES */

if(lang==="python"){
fileNameBox.textContent="main.py";
}

if(lang==="c"){
fileNameBox.textContent="main.c";
}

if(lang==="cpp"){
fileNameBox.textContent="main.cpp";
}

}

/* =========================
RUN CODE
========================= */

runBtn.addEventListener("click",runCode);

async function runCode(){

outputBox.textContent="⚡ Running...";

try{

const res = await fetch("/api/compile",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

language:languageSelect.value,
code:editor.getValue(),
input:inputBox.value

})

});

const result = await res.json();

outputBox.textContent = result.output || "";

outputBox.scrollTop = outputBox.scrollHeight;

}catch(err){

outputBox.textContent="❌ Server Error";

}

}
