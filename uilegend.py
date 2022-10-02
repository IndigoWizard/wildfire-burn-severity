uilegend = """
{% macro html(this, kwargs) %}
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="robots" content="index,follow,max-image-preview:large" />
        <meta name="keywords" content="wildfire, forest fire, earth engine, google earth engine, gee, remote sensing, normalized burn ratio, burn severity,, satellite imagery, sentinel-2, proejcts, folium, github pages, github, linkedin, environmental studies, forest fire analysis, wildfire analysis">
        <meta property="og:description" content="Wildfire Burn Severity Anlasysis by Ahmed Islem Mokhtari">
        <meta property="og:title" content="Wildfire Burn Severity Anlasysis using GEE by Ahmed I. Mokhtari"/>
        <meta property="og:image" content="https://www.pixenli.com/image/X0aFtxup">
        <link rel="image_src" href="https://www.pixenli.com/image/X0aFtxup">
        <meta itemprop="image" content="https://www.pixenli.com/image/X0aFtxup">
        <meta itemprop="thumbnailUrl" content="https://www.pixenli.com/image/X0aFtxup">
        <meta name="linkedin:image" content="https://www.your-website.com/open-graph.jpg">
        <meta property="og:url" content="https://indigowizard.github.io/wildfire-burn-severity/webmap.html"/>
        <title>Wildfire Burn Severity Analysis</title>
        <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
        <link rel="stylesheet" href="src/ui.css">
        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

        <script>
            $(function() {
                $("#ui-container, #title-container, #project-container").draggable({
                    start: function(event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
            });
        </script>
    </head>

  <body>
  <div class="ui-container" id="title-container">
    <div class="map-title">
      <p>Wildfire Burn Severity Analysis</p>
    </div>
  </div>

  <div id="ui-container" class="ui-container">

        <div class="project-source">
          <div class="project-logo">
              <a href="https://github.com/IndigoWizard/wildfire-burn-severity/tree/dev" title="Go to repository" target="_blank">
                <i class="fa fa-github" aria-hidden="true" id="icons"></i>
              </a>
          </div>

          <div class="project-info">
            <a href="https://github.com/IndigoWizard/wildfire-burn-severity" title="Go to repository" target="_blank"><p  class="project-link"  id="icons">IndigoWizard/mega-port-environment</p></a>
            <div class="project-stats">
              <a href="https://github.com/IndigoWizard/wildfire-burn-severity/" target="_blank"><i class="fa fa-link" aria-hidden="true" id="icons"><span class="ghtext"> Check it!</span></i></a>
              <a href="https://github.com/IndigoWizard/wildfire-burn-severity/stargazers" target="_blank"><i class="fa fa-star" aria-hidden="true" id="icons"><span class="ghtext"> Star it!</span></i></a>
              <a href="https://github.com/IndigoWizard/wildfire-burn-severity/network/members" target="_blank"><i class="fa fa-code-fork" aria-hidden="true" id="icons"><span class="ghtext"> Fork it!</span></i></a>
            </div>
          </div>
        </div>

        <div class="leaflet-control-layers-separator"></div>

      <div class="legend-title">Legend</div>

      <div class="index-container">
        <div class="legend-scale" id="VECTOR">
          <ul class="legend-labels">
            <li><span style="background:#5555552e;opacity:0.8;border: solid 2px #87043b;"></span>Burn Scar Zone.</li>
          </ul>
        </div>
        <div class="legend-scale" id="dNBR">
            <h4>dNBR Classes - Burn Severity Levels</h4>
            <ul class="legend-labels">
              <li><span style="background:#902cd6;opacity:0.8;"></span>High Severity Burns</li>
              <li><span style="background:#e86c4e;opacity:0.8;"></span>Moderate-High Severity Burns</li>
              <li><span style="background:#f7a769;opacity:0.8;"></span>Moderate-Low Severity Burns</li>
              <li><span style="background:#f8ebb0;opacity:0.8;"></span>Low Severity Burns</li>
              <li><span style="background:#a1d574;opacity:0.8;"></span>Unburned</li>
              <li><span style="background:#2aae29;opacity:0.8;"></span>Enhanced Regrowth (Low)</li>
              <li><span style="background:#1c742c;opacity:0.8;"></span>Enhanced Regrowth (High)</li>
            </ul>
        </div>

        <div class="index-gradient">

          <div class="index-gradient-container">
            <div class="legend-scale" id="NBRGS">
              <h4>NBR Greyscale</h4>
              <ul class="legend-labels">
                <li id="greyscale">-1<span id="nbr-greyscale"></span>1</li>
              </ul>
          </div>
        </div>

      </div>
  </div>
{% endmacro %}
"""