function toggleDarkLight() {
    var body = document.getElementById("body");
    var currentClass = body.className;
    body.className = currentClass == "dark-mode" ? "light-mode" : "dark-mode";
    var symbol = document.getElementsByName("dark_light")[0];
    if (body.className == "dark-mode") {
        symbol.innerText = "☀";
    } else {
        symbol.innerText = "🌙";
    }
}