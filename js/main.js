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

// FIX - convert reload to ajax

function send_data(){
  var eng_data = document.getElementsByName('eng')[0].value;
  var rus_data = document.getElementsByName('rus')[0].value;
  var url_link = image_link;
  $.ajax({
              url: "http://localhost:8000/cgi-bin/index.py",
              type: "POST",
              data: {eng: eng_data, rus: rus_data, url: url_link},
              success: function(response){
                      alert(eng_data+'&'+rus_data+'&'+url_link);;
                  }
         });
}
