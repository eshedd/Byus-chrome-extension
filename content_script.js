//console.log("Got this far!")
//request({
//    method: 'GET',
//    url: 'http://textfiles.com/news/092793.txt'
//}, (err, res, body) => {
//    
//    if (err) throw err;
//
//    if (err) return console.error(err);
//
//    let $ = cheerio.load(body);
//
//    let h1El = $('h1');
//
//    let parentEl = h1El.parent();
//
//    console.log(parentEl.get(0).tagName)
//});