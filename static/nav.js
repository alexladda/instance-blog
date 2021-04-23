function hamburger() {
  var x = document.getElementById("main_nav");
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "block";
  }
}
function set_nav() {
  // mobile: #nav {display: none;}
  // desktop: #nav {display: block;}
  var w = window.outerWidth;
  var x = document.getElementById("main_nav");
  if (w > 800) {
    x.style.display = "block";
  } else {
    // this also tends to conveniently hide the nav
    x.style.display = "none";
  }
}
