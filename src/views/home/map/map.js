var WorldWind = require("@nasaworldwind/worldwind");
WorldWind.configuration.baseUrl = "img/";

var plot = function() {
  var wwd = new WorldWind.WorldWindow("map");
  wwd.addLayer(new WorldWind.BMNGOneImageLayer());
  wwd.addLayer(new WorldWind.BMNGLandsatLayer());
  wwd.addLayer(new WorldWind.CoordinatesDisplayLayer(wwd));
};

export default {
  plot: plot
};
