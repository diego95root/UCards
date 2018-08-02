var image_link = "hi";

document.addEventListener("DOMContentLoaded", function(event) {
  //var image_link = document.getElementsByClassName("slide")[0].firstElementChild.src;
  console.log(image_link);
});

function add_img_link(){
  for (var i=0; i!=document.getElementsByClassName("slide").length; i++){
    if (window.getComputedStyle(document.getElementsByClassName("slide")[i]).getPropertyValue('opacity') !== "0"){
      var elt = document.getElementsByClassName("slide")[i];
      image_link = elt.firstElementChild.src;
    };
  }
}

function send_data(){
  var eng_data = document.getElementsByName('eng')[0].value;
  var rus_data = document.getElementsByName('rus')[0].value;
  var url_link = image_link;
  $.ajax({
              url: "http://localhost:8000/cgi-bin/index.py",
              type: "POST",
              data: {eng: eng_data, rus: rus_data, url: url_link}
         });
}

// Use ajax get to include the images once the translation terms have been set
// It should build the slide here

function google_api(){
  $.ajax({
              url: "http://localhost:8000/cgi-bin/index.py",
              type: "GET",
              data: {links:'a'},
              cache: false,
              success: function(response){ // HOW THE HELL DO I DO THIS SHIT MAN
                      alert(response);
                  }
         });
}


// Try to use native js to implement ajax calls - FIX

function send_data2(){
  var eng_data = document.getElementsByName('eng')[0].value;
  var rus_data = document.getElementsByName('rus')[0].value;
  var url_link = image_link;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200){
        alert(eng_data+'&'+rus_data+'&'+url_link);
    }
  };
  xhttp.open('POST', 'http://localhost:8000/cgi-bin/index.py', true);
  xhttp.send(JSON.stringify({eng: eng_data, rus: rus_data, url: url_link}));
}
