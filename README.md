# Featuremap Utility
Generate featuremaps.  Most of the time you'll be converting prediction files to featuremap files.
Or, you may want to generate a featuremap from a spreadsheet containing pyradiomics data.

## Need to know
* Who's algorithm is it (who ran it)?
* What is the execution id?
* And sometimes – where are the color files?

You can usually answer the question "who's algorithm" and "execution id" by looking at `heatmap_json` output.

If there are no color files, run this script in the input folder:

```
for i in $(ls prediction-*); do
  a=$(echo "$i" | awk -F 'prediction-' '{print $2}')
  awk '{ if ($3>0.0) { print $1" "$2" 100.0 50.0 0.0" } else { print $1" "$2" 1.0 50.0 0.0" } }' "$i" >color-"$a"
done
```

## Build and run

- `cd` into the directory
- Modify volume mapping in docker-compose.yml
- Then run `docker-compose up -d`

Put input files in the [input](input) directory.<br>
Put output files in the [output](output) directory.<br>


## Usage

### Prediction files to featuremap
Let's say you have a bunch of prediction files (color-\*, prediction-\*) and you want to generate featuremaps.<br>
The following command takes two arguments: execution id, and wsi type.<br>
wsi type can be svs, tif, scn, etc.

```
nohup docker exec quip-maputil pred_to_map exec_id exec_by wsi_type &
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
nohup docker exec quip-maputil merge_cancer_til exec_id exec_by wsi_type &
```
<br>


### Pyradiomics to featuremap
We've generated a bunch of pyradiomics csv files.  Here's how to create featuremaps:

```
docker exec quip-maputil pyrad_to_map exec_id exec_by
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
