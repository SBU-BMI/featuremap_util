# Featuremap Utility
Generate featuremaps.  Most of the time you'll be converting prediction files to featuremap files.
Or, you may want to generate a featuremap from a spreadsheet containing pyradiomics data.

## Build and run

```
./build.sh /path/to/input/dir /path/to/output/dir /path/to/wsi/dir
```

Input files go in input directory!<br>
Program will output files to the output folder you specified!
<br>


## Usage

### Prediction files to featuremap
Let's say you have a bunch of prediction files (color-\*, prediction-\*) and you want to generate featuremaps.<br>
The following command takes two arguments: execution id, and wsi type.<br>
wsi type can be svs, tif, scn, etc.

```
nohup docker exec quip-maputil pred_to_map exec_id wsi_type &
```
<br>


### Prediction file merge
**Merge TIL & Cancer prediction**

We've got TIL predictions and cancer predictions.<br>
The following command takes two arguments: execution id, and wsi type.<br>
wsi type can be svs, tif, scn, etc.

```
cd input; mkdir til cancer
# put input files in input/til and input/cancer
# then run
nohup docker exec quip-maputil merge_cancer_til exec_id wsi_type &
```
<br>


### Pyradiomics to featuremap
We've generated a bunch of pyradiomics csv files.  Here's how to create featuremaps:

```
docker exec quip-maputil pyrad_to_map exec_id
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


## Output data format
The output data format is in JSON.

```
{
    "metadata": {
        "img_width": number,
        "img_height": number,
        "png_w": number,
        "png_h": number,
        "patch_w": number,
        "patch_h": number,
        "exec_id": exec_id
    },
    "data": {
        "locations": {
            "i": [list of 'i' (aka 'x' coordinates)],
            "j": [list of 'j' (aka 'y' coordinates)]
        },
        "features": {
            "TIL": [ list of feature data corresponding to i,j (see above) ],
            "Cancer": [ list of feature data corresponding to i,j (see above) ],
            "Tissue": [ list of feature data corresponding to i,j (see above) ]
        }
    }
}
```


<!--
### Build

```
docker build -t featuremap_util .
```

### Run
```
docker run --name quip-maputil -v $(pwd)/input:/data/input -v $(pwd)/output:/data/output -itd featuremap_util

./build.sh $(pwd)/input $(pwd)/output $(pwd)/wsi

```
-->
