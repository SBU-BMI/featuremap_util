## Other utilities

### Prediction file merge
**Merge TIL & Cancer prediction**

We've got TIL predictions and cancer predictions.<br>
The following command takes two arguments: execution id, and wsi type.<br>
wsi type can be svs, tif, scn, etc.

```
cd input; mkdir til cancer
# put input files in input/til and input/cancer
# then run
nohup docker exec quip-maputil merge_cancer_til exec_id exec_by wsi_type &
```
<br>


### PNG to featuremap
Let's say we don't have the prediction files, but we have a bunch of PNGs.  Here's how to generate featuremaps.

```
docker exec quip-maputil png_to_map wsi_type
```


<br>

### CSV to featuremap
The FeatureMap application accepts data in JSON format.  Let's say we have a "legacy" map, i.e. one with a JSON "header", and then columns `i, j, R, G, B`.  And we want to convert them to proper featuremaps.  Here's how:

```
docker exec quip-maputil csv_to_json
```
<br>

