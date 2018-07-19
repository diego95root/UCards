document.addEventListener("DOMContentLoaded", function(event) {
  var image_link = document.getElementsByClassName("slide")[0].firstElementChild.src;
});

function add_img_link(){
  for (var i=0; i!=document.getElementsByClassName("slide").length; i++){
    if (window.getComputedStyle(document.getElementsByClassName("slide")[i]).getPropertyValue('opacity') !== "0"){
      var elt = document.getElementsByClassName("slide")[i];
      image_link = elt.firstElementChild.src;
    };
  }
}

// FIX - convert reload to ajax

function send_data(){
  var eng = document.getElementsByName('eng')[0].value;
  var rus = document.getElementsByName('rus')[0].value;
  var url = image_link;
  var xhttp = new XMLHttpRequest();
  var params = 'eng='+eng+'&rus='+rus+'&url='+url;
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      alert(eng+'&'+rus+'&'+url);
    }
  };
  xhttp.open("POST", "/cgi-bin/index.py", true);
  xhttp.send(params);
}
