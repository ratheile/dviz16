$(document).ready(function(){

	$("#button1").click(function(e){
		e.preventDefault();
		load('/test',{}, '#plot1');
	});

	$("#button2").click(function(e){
		e.preventDefault();
		load('/test',{}, '#plot2');
	});

	$("#button3").click(function(e){
		e.preventDefault();
		load('/test',{}, '#plot3');
	});

	$("#button4").click(function(e){
		e.preventDefault();
		$.getJSON("static/genreavgs.json", function(json) {

   			var keys = [];
   			var values = []
			for (var key in json) {
			  if (json.hasOwnProperty(key)) {
			    keys.push(key);
				values.push(json[key]);
			  }
			}

			var min = Math.min.apply(null, values); 
			var max = Math.max.apply(null, values); 
			var count = keys.length;
			var pi = Math.PI;

			var plot_size = 600;
			var radius = 100

			var min_font_px = 15;
			var max_font_px = 60;

			var svg = d3.select("#plot4").append("svg")
			                             .attr("width", plot_size)
			                             .attr("height", plot_size);


			for(var i = 0; i < count; i++){

				var delta = max_font_px - min_font_px;
				var scale = (json[keys[i]] - min) / (max - min) ;
				var font_size = min_font_px + delta * scale; 

				 svg.append("text")
				.text(keys[i])
				.style("font-size", font_size + "px"   )
				.style('fill', getRandomColor())
				.attr("width", 10)
				.attr("height", 10)
				.attr("x", plot_size/2 + radius)
				.attr("y", plot_size/2)
				.attr("transform","rotate(" + (360/count) * i + "," 
					+ plot_size/2 + ","
					+ plot_size/2 + ")");

			}

	

		});
	});


	function getRandomColor() {
	    var letters = '0123456789ABCDEF';
	    var color = '#';
	    for (var i = 0; i < 6; i++ ) {
	        color += letters[Math.floor(Math.random() * 16)];
	    }
	    return color;
	}

	function load(url, data, parent){
		$.ajax({type: "GET",
		  url: url,
		  data: data,
		  success:function(result){
				$(parent).html(result);
		  },
		  error: function (xhr, ajaxOptions, thrownError) {
				$(parent).html('Error, check parameters!: ' + xhr.status + ' ' + thrownError);
			}
		});
	}



});



