const express = require("express");
const cors = require("cors");
const path = require("path");

const compileRoutes = require("./routes/compileRoutes");

const app = express();

app.use(cors());
app.use(express.json());

app.use(express.static(path.join(__dirname, "public")));

app.use("/api", compileRoutes);

app.get("/", (req,res)=>{
res.sendFile(path.join(__dirname,"public","index.html"));
});

const PORT = 5000;

app.listen(PORT,()=>{
console.log(`🚀 Server running at http://localhost:${PORT}`);
});
