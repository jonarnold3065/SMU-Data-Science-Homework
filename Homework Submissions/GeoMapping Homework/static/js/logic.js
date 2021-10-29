// Store the API query variables.
var baseURL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/";
// Add the timeframe
var timeframe = "all_week.geojson";

// build URL
var url = baseURL + timeframe;

// geojson
var tectonic_boundary_url = "./static/data/PB2002_boundaries.json";

$(document).ready(function() {
 // add filter option for time frame????



    // AJAX
    $.ajax({
        type: "GET",
        url: url,
        contentType: "application/json",
        dataType: "json",
        success: function(data) {

            $.ajax({
                type: "GET",
                url: tectonic_boundary_url,
                contentType: "application/json",
                dataType: "json",
                success: function(tect_data) {
                    // console.log(data);
                    // console.log(tect_data);
                    makeMap(data, tect_data);

                },
                error: function(data) {
                    console.log("YOU BROKE IT!!");
                },
                complete: function(data) {
                    console.log("Request finished");
                }
            });
        },
        error: function(data) {
            console.log("YOU BROKE IT!!");
        },
        complete: function(data) {
            console.log("Request finished");
        }
    });
});




function makeMap(data, tect_data) {
    // Create the base layers.
    var dark_layer = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/dark-v10',
        accessToken: API_KEY
    });

    var light_layer = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/light-v10',
        accessToken: API_KEY
    });


    // Basemaps 
    var baseMaps = {
        "Dark": dark_layer,
        "Light": light_layer
    };

    //  MARKERS
    let features = data.features;
    let geoLayer = L.geoJSON(features, {
        onEachFeature: onEachFeature
    });

    // plates 
    let tectLayer = L.geoJson(tect_data, {
        style: function(feature) {
            return {
                color: "red",
                weight: 1,
        
            };
        }
    });


    // heatmaps and markers
    var heatArray = [];
    var quakeMarkers = L.markerClusterGroup();
    var circleMarkers = [];


    for (var i = 0; i < features.length; i++) {
        var location = features[i].geometry;

        

        if (location) {
            heatArray.push([location.coordinates[1], location.coordinates[0]]);

            // marker info for quake marker cluster group 
            let marker = L.marker([location.coordinates[1], location.coordinates[0]]);
            marker.bindPopup(`<h3>Location: ${data.features[i].properties.place}</h3>
            <hr>
            <p>Time: ${new Date(data.features[i].properties.time)}</p>
            <p>Magnitude: ${data.features[i].properties.mag}</p>
            <p>Depth: ${data.features[i].geometry.coordinates[2]}</p>`);
            quakeMarkers.addLayer(marker);

                // add facney circles that vary by color based on magnitude 
            let circle = L.circle([location.coordinates[1], location.coordinates[0]], {
                fillOpacity: 0.75,
                color: makeColor(data.features[i].geometry.coordinates[2]),
                fillColor: makeColor(data.features[i].geometry.coordinates[2]),
                
            
                // marker's size proportionate to its mag/depth.

                radius: makeRadius(data.features[i].properties.mag)
            }).bindPopup(`<h3>Location: ${data.features[i].properties.place}</h3>
            <hr>
            <p>Time: ${new Date(data.features[i].properties.time)}</p>
            <p>Magnitude: ${data.features[i].properties.mag}</p>
            <p>Depth: ${data.features[i].geometry.coordinates[2]}</p>`);
    

            circleMarkers.push(circle);
        
        }
    }

    
    var circleLayer = L.layerGroup(circleMarkers)

    var heatLayer = L.heatLayer(heatArray, {
        radius: 50,
        blur:1
    });


    // overlays to include heat, circls, plates, etc. 
    var overlayMaps = {
        "Quake Info Markers": quakeMarkers,
        // "Earthquakes": geoLayer,
        "Heatmap": heatLayer,
        "Circles": circleLayer,
        "Tectonic Plates": tectLayer
    };

    // map defualt and what we want the page to load with 
    var myMap = L.map("map", {
        center: [37.09, -95.71],
        zoom: 3,
        layers: [dark_layer, heatLayer, circleLayer, tectLayer ]
    });


    
    // CControls for the map
    L.control.layers(baseMaps, overlayMaps).addTo(myMap);
    

    // legend stuff 

    var legend = L.control({ position: 'bottomright' });
    legend.onAdd = function() {
        var div = L.DomUtil.create('div', 'info legend');

        let legend_html = `<span>Depth Legend</span><br>
        <br>
        <i class="circle" style='background: #98ee00'></i><span> &nbsp&nbsp>10</span><br>
        <i class="circle" style='background: purple'></i><span>10-30</span><br>
        <i class="circle" style='background: blue'></i><span>30-50</span><br>
        <i class="circle" style='background: yellow'></i><span>50-70</span><br>
        <i class="circle" style='background: orange'></i><span>70-90</span><br>
        <i class="circle" style='background: red'></i><span>90+</span>`;

        div.innerHTML = legend_html;
        return div;
    }
    legend.addTo(myMap);
}

// popup info for quake marker cluster group 
function onEachFeature(feature, layer) {
    layer.bindPopup(`<h3>Location: ${feature.properties.place}</h3>
    <hr>
    <p>Time: ${new Date(feature.properties.time)}</p>
    <p>Magnitude: ${feature.properties.mag}</p>`);
}


// marker stylings 
function makeRadius(magnitude) {
    // Adjust the radius
    return magnitude * 15000;
}


  



// colors for cirlces, based on magnitude strength. 
// function makeColor(magnitude) {
//     let rtnColor = "red";

//     // Conditionals for magnitude levels
//     if (magnitude > 5) {
//         rtnColor = "red";
//     } else if (magnitude > 4) {
//         rtnColor = "orange";
//     } else if (magnitude > 3) {
//         rtnColor = "yellow";
//     } else if (magnitude > 2) {
//         rtnColor = "blue";
//     } else if (magnitude > 1) {
//         rtnColor = "purple";
//     } else {
//         rtnColor = "red";
//     }

//     return rtnColor;
// }

function makeColor(depth) {
    let rtnColor = "green";

    // Conditionals for country points
    if (depth > 90) {
        rtnColor = "red";
    } else if (depth > 70) {
        rtnColor = "orange";
    } else if (depth > 50) {
        rtnColor = "yellow";
    } else if (depth > 30) {
        rtnColor = "blue";
    } else if (depth > 10) {
        rtnColor = "purple"
    } else {
        rtnColor = "green"
    }

    return rtnColor;
}
