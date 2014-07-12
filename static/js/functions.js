    // Autores: Natalia Bustacara, Nicolas Vergara y y en colaboracion de Alejandro Rojas
	
	
	//Funcion que inicializa mapa            
       function initialize() {
            // Centro aproximado en colombia
            var myLatlng = new google.maps.LatLng(4.63, -74.06);
            var myOptions = {
                zoom: 13,
                center: myLatlng,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            }
            map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);   
        }


        function adicionar_usuario(){
            console.log("Adicionando");
            var cx = parseFloat(jQuery('#cx').val());
            var cy = parseFloat(jQuery('#cy').val());
            point = new google.maps.LatLng(cy, cx);
            //Anado marcador                
            addMarker(point, "<b> Posicion </b>", "/static/imgs/walker.png");
    
        }

        function get_paraderos_cercanos(tipo){
          initialize();
           var cx = parseFloat(jQuery('#cx').val());
          var cy = parseFloat(jQuery('#cy').val());
          adicionar_usuario();
   
            jQuery.getJSON("/paraderos_cercanos/", {'cx': cx, 'cy': cy, 'tipo': tipo}, function(data) {

            for (var i=0; i<data.length; i++) {
              var nombre = data[i].name;
              var cx = parseFloat(data[i].cx);
              var cy = parseFloat(data[i].cy);
              var desc = data[i].description;
              var tipo = data[i].tipo;
              var rutas = data[i].rutas;
              var popup = "<b>Nombre: </b>"+nombre+"</br>"+"<b>Coordenada X: </b>"+cx+"</br>"+"<b>Coordenada Y: </b>"+cy+"</br>"+"<b>Descripcion</b>"+desc+"</br>";
              
              if(tipo == "sitp"){
                jQuery('#tabla_paraderos').append('<tr><td>'+ nombre + '</td><td>'+ cx + '</td><td>' + cy + '</td><td>' + "Paradero SITP" + '</td><td>' + rutas +'</td></tr>');
                point = new google.maps.LatLng(cy, cx);
                addMarker(point, popup, "/static/imgs/sitp.jpg");
              }
              else {
                jQuery('#tabla_estaciones').append('<tr><td>'+ nombre + '</td><td>'+ cx + '</td><td>' + cy + '</td><td>' + "Estacion TM" + '</td><td>' + rutas +'</td></tr>');
                point = new google.maps.LatLng(cy, cx);
               addMarker(point, popup, "/static/imgs/tm.png");
              }
              
            }

            });
        
        }

        function addMarker(location, datos, logo_url) {
            console.log("Adicionando marker");
            var infowindow = new google.maps.InfoWindow({
                  content: datos
              });
            var marker = new google.maps.Marker({
                position: location,
                map: map,
                icon: logo_url, 
            });
             google.maps.event.addListener(marker, 'click', function() {
            infowindow.open(map,marker);
          });
        }