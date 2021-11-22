function showTime(id, showSeconds=false) {
    var date = new Date();
    var h = date.getHours(); // 0 - 23
    var m = date.getMinutes(); // 0 - 59
    var s = date.getSeconds(); // 0 - 59

    h = (h < 10) ? "0" + h : h;
    m = (m < 10) ? "0" + m : m;
    s = (s < 10) ? "0" + s : s;

    var time = h + ":" + m;

    if (showSeconds){
        time += ":" + s
    }

    document.getElementById(id).innerText = time;
    document.getElementById(id).textContent = time;

    setTimeout(() => {showTime(id, showSeconds)}, 1000);

}