var out = 0;
var inn = 0;
var slide_built = 0;

document.addEventListener('DOMContentLoaded', function(){
  document.getElementById('first-input').addEventListener('focusout', function(){out = 1; api_caller()});
  document.getElementById('first-input').addEventListener('focus', function(){inn = 1; api_caller()});
  document.getElementById('second-input').addEventListener('focusout', function(){out = 1; api_caller()});
  document.getElementById('second-input').addEventListener('focus', function(){inn = 1; api_caller()});
});

function display_msg(text){
  var elt = document.getElementById("saved");
  var overlay = document.getElementById("overlay-back");
  elt.innerHTML = text;
  elt.style.visibility = "visible";
  elt.style.opacity = "1";
  overlay.style.visibility = "visible";
  overlay.style.opacity = "0.6";
  setTimeout(function(){
    elt.style.opacity = "0";
    overlay.style.visibility = "hidden";
    overlay.style.opacity = "0";
    elt.style.visibility = "hidden";
  },580);
}

function api_caller(){
  if (document.getElementsByName('eng')[0].value == ""){
      out = 0;
      inn = 0;
      return 0;
  }
  if (out == 1 && inn == 1 && !(slide_built)){
    slide_built = 1;
    google_api(0);
  }
}

function add_img_link(){
  for (var i=0; i!=document.getElementsByClassName("slide").length; i++){
    if (window.getComputedStyle(document.getElementsByClassName("slide")[i]).getPropertyValue('opacity') !== "0"){
      var elt = document.getElementsByClassName("slide")[i];
      image_link = elt.firstElementChild.src;
      display_msg("Flashcard image set");
    };
  }
}

function send_data(){
  var eng_data = document.getElementsByName('eng')[0].value;
  var rus_data = document.getElementsByName('rus')[0].value;
  var url_link = "image_link"; //image_link;
  $.ajax({
              url: "http://localhost:8000/cgi-bin/index.py",
              type: "POST",
              data: {eng: eng_data, rus: rus_data, url: url_link}
         });
}

// Use ajax get to include the images once the translation terms have been set
// It should build the slide here

function build_slide(array){ //slider from https://codepen.io/AMKohn/pen/EKJHf (adopted to js, loaded dynamically)
  var ul = document.createElement("ul");
  ul.setAttribute("class", "slides");
  var sender = document.getElementById("sender");
  document.getElementById("main").insertBefore(ul, sender);
  setTimeout(function(){
    document.getElementsByClassName('slides')[0].className += ' slides-visible';
  }, 0);
  for (var i=1; i!=11; i++){
    var input = document.createElement("input");
    input.setAttribute("type", "radio");
    input.setAttribute("name", "radio-btn");
    input.setAttribute("id", "img-" + String(i));
    input.setAttribute("checked", "checked");
    ul.appendChild(input); //<input type="radio" name="radio-btn" id="img-{}" checked />

    var li = document.createElement("li"); //<li class="slide-container">
    li.setAttribute("class", "slide-container");
    ul.appendChild(li);

    var div = document.createElement("div"); //<div class="slide">
    div.setAttribute("class", "slide");
    li.append(div);

    var img = document.createElement("img"); //<img src="{}" />
    img.setAttribute("src", array[i-1]);
    img.setAttribute("class", "slide_img");
    div.append(img);

    var div2 = document.createElement("div"); //<div class="nav">
    div2.setAttribute("class", "nav");
    li.append(div2);

    var lab1 = document.createElement("label"); //<label for="img-{}" class="prev">&#x2039;</label>
    lab1.setAttribute("for", "img-"+String(((i+8)%10)+1));
    lab1.setAttribute("class", "prev");
    lab1.innerHTML = "&#x2039;";
    div2.append(lab1);

    var lab2 = document.createElement("label"); //<label for="img-{}" class="next">&#x203a;</label>
    lab2.setAttribute("for", "img-"+String((i % 10) + 1));
    lab2.setAttribute("class", "next");
    lab2.innerHTML = "&#x203a;";
    div2.append(lab2);
  }

  var li2 = document.createElement("li"); //<li class="nav-dots">
  li2.setAttribute("class", "nav-dots");
  ul.appendChild(li2);

  for (var i=1; i!=11; i++){
    var labeldot = document.createElement("label"); //<label for="img-{}" class="nav-dot" id="img-dot-{}"></label>'.format(i, i)
    labeldot.setAttribute("for", "img-"+String(i));
    labeldot.setAttribute("class", "nav-dot");
    labeldot.setAttribute("id", "img-dot-"+String(i));
    li2.append(labeldot);
  }

  var but = document.createElement("button"); //<li class="nav-dots">
  but.setAttribute("class", "button");
  but.setAttribute("onclick", "add_img_link()");
  but.appendChild( document.createTextNode("Set flashcard image"));
  document.getElementById("main").insertBefore(but, sender);
  var but2 = document.createElement("button"); //<li class="nav-dots">
  but2.setAttribute("class", "button");
  but2.setAttribute("onclick", "google_api(1)");
  but2.appendChild( document.createTextNode("Search again"));
  document.getElementById("main").insertBefore(but2, sender);
  setTimeout(function(){
    x = document.getElementsByClassName('button');
    for (var i = 0; i < x.length; i++) x[i].className += ' button-visible';
  }, 0);
  //<button id="button">use?</button>
}

function replace_slide(array){
  x = document.getElementsByClassName('slide_img');
  display_msg("Images replaced");
  for (var i = 0; i < x.length; i++) x[i].src = array[i];
}

function google_api(id){
  $.ajax({
              url: "http://localhost:8000/cgi-bin/index.py",
              type: "GET",
              data: {links:document.getElementsByName('eng')[0].value},
              cache: false,
              success: function(response){
                      if (id == 0){
                        build_slide(response);
                        //build_slide(JSON.parse(response));
                        //var image_link = document.getElementsByClassName("slide")[0].firstElementChild.src;
                        //alert(response);
                      }
                      else {
                        replace_slide(response);
                      }
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
