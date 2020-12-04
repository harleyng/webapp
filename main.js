  function renderImage(page_name) {
    if (page_name == 'radiopaedia') {
      $.getJSON('data.json', function(data){
        var card = '';
        for (var obj in data) {
            card += "<div class='card' style='float: left;width: 24%;margin: 0.5%; height: 500px; overflow: scroll;'>";
                card += "<h3 class='card-title' style='text-align:center; padding: 20px 0'>" +obj+ "</h3>";
                card += "<div class='card-img'>";
                    card += "<img style='width: 100%; height: 300px' src='"+data[obj].img[0]['src']+"'>";
                card += "</div>";
                card += "<div class='card-body'>";
                    card += "<div> <h5 class='card-age' style='display: inline-block'>Age: </h5>" +data[obj].age+"</div>";
                    card += "<div> <h5 class='card-gender' style='display: inline-block'>Gender: </h5>" +data[obj].gender+"</div>";
                    card += "<div> <h5 class='card-presentation' style='display: inline-block'>Condition:</h5>"+" "+data[obj].presentation+ "</div>";
                card += "</div>";
            card += "</div>";
        }
        $("#news").innerHTML = '';
        $(card).appendTo('.card-gallery'); 
      })
    } else {
      $.getJSON('simp.json', function(data){
        var img = '';
        $.each(data.img, function(key, value){
          img += '<tr>';
          img += '<td>'+value.title+'</td>';
          img += '<td><img src="'+value.src+'"></td>';
          img += '</tr>';
      });
      $('.card-gallery').empty();
      $(img).appendTo("#news tbody");
      });
    }
  }

  $(document).ready(function() {
    $.getJSON('simp.json', function(data){
        console.log(data)
        var img = '';
        $.each(data.img, function(key, value){
            img += '<thead>';
            img += '<th>Case</th>';
            img += '<th>Image</th>';
            img += '</thead>';
            img += '<tbody>';
            img += '<tr>';
            img += '<td>'+value.title+'</td>';
            img += '<td><img src="'+value.src+'"></td>';
            img += '</tr>';
            img += '</tbody>';
        });
        $(img).appendTo("#news");
    });
});
