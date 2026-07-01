#HPSA Physician Opportunity Map Data
This repository stores the data files, update scripts, and documentation for the Map on the PLG website.

It stores: 
- The HPSA boundary data used to draw the polygons of the shortage area (hpsas_simplifies_tol_0p01.json)
- Physician hiring-opportunity data used to create the map pins (hrsa_physician_opportunities.csv)
- The Python script used to refresh physician opportunity data (hrsa_physician_opportunities.py)
- A backup copy of the Webflow map/navigation pill embed code (webflow_map_embed.html & webflow_navPill_embed.html)
- Documentation for maintaining the project

The public Webflow map reads the current data files from this repository, so updating those files in GitHub updates the data available to the map without having to change the Webflow embed. 
