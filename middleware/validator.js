module.exports = function(req, res, next){

    const { language, code } = req.body;

    if(!language || !code){
        return res.status(400).send("Invalid Request");
    }

    next();
}
