const {
  runPython,
  runC,
  runCPP,
  runJava
} = require("../services/compileService");

exports.compileCode = async (req, res) => {

  try {

    const { language, code, input } = req.body;

    if (!language || !code) {
      return res.json({
        status: "RE",
        output: "Invalid Request"
      });
    }

    let result;

    switch(language){

      case "python":
        result = await runPython(code,input);
      break;

      case "c":
        result = await runC(code,input);
      break;

      case "cpp":
        result = await runCPP(code,input);
      break;

      case "java":
        result = await runJava(code,input);
      break;

      default:
        return res.json({
          status:"RE",
          output:"Unsupported Language"
        });

    }

    res.json({
      status:"OK",
      output:result
    });

  } catch(err){

    res.json({
      status:"RE",
      output:err.toString()
    });

  }

};
