$(document).ready(function() {
  $.getJSON('data.json', function(data){
      console.log(data)
      var card = '';
      for (var obj in data) {
          card += "<div class='card' style='float: left;width: 24%;margin: 0.5%; height: 500px; overflow: scroll;'>";
              card += "<h3 class='card-title' style='text-align:center; padding: 20px 0'>" +obj+ "</h3>";
              card += "<div class='card-img'>";
                  card += "<img style='width: 100%; height: 300px' src='"+data[obj].img[0]['src']+"'>";
              card += "</div>";
              card += "<div class='card-body'>";
                  card += "<h5 class='card-age'>Age: " +data[obj].age+ "</h5>";
                  card += "<h5 class='card-gender'>Gender: " +data[obj].gender+ "</h5>";
                  card += "<p class='card-presentation'>" +data[obj].presentation+ "</p>";
              card += "</div>";
          card += "</div>";
      }
      $(card).appendTo('.card-gallery')
  });
});
