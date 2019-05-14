This folder contains scripts that can generate necessary road data. Location,
output filenames, and bounding box specifications can be changed in bBoxConfig.txt.

/generated_map_data/
  This directory is where all generated data is saved to. Some data was generated
  using old versions of scripts and thus are not formatted correctly. These should be
  re-generated.

/map_data_images/
  This directory contains images of generated data displayed using
  displayGeneratedDatasets.py

roadSegmentGen.py
  This file gets all the road segments within the bounding box specified in
  bBoxConfig.txt and writes it to a .CSV file.

  The CSV will be of form
    startNodeId, endNodeID, startLat, startLon, endLat, endLon, distance, street name

  The output filename of the CSV will be of form
    roadSegmentsXXX.csv
    XXX = name specified in bBoxConfig.txt

intersectionGen.py
  This file gets all intersections within the bounding box specified in
  bBoxConfig.txt and writes it to a .CSV file.

  The CSV will be of form
    intersection name, lat, lon, NodeID

  The output filename of the CSV will be of form
    intersectionsXXX.csv
    XXX = name specified in bBoxConfig.txt

poiGenYelp.py
  This file gets all POI's around the location specified in
  bBoxConfig.txt and writes it to a .CSV file.

  The CSV will be of form
    address, lat, lon, rating, startNodeID, endNodeID

  The output filename of the CSV will be of form
    poiYelpXXX.csv
    XXX = name specified in bBoxConfig.txt
