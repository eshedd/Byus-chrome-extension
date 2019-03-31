//
//function hello() {
//    function contentScript(text){
//        document.write(" i am here . . .");
//        var hr = new XMLHttpRequest();
//        var url = "http://127.0.0.1:5000/";
//        var vars = "text="+text;
//        hr.open("POST", url, true);
//        hr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//        hr.send(vars);
//    }
//
//    var text = document.getElementById("text").value;
//    chrome.tabs.executeScript({
//        code: (contentScript.toString() + "\ncontentScript('" + text + "');")
//    }); 
//}
//document.getElementById('clickme').addEventListener('click', hello);