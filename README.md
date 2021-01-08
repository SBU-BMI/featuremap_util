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

- `cd` into this directory
- Modify volume mapping in docker-compose.yml (particularly `wsi` - point it to the appropriate folder under `images` on the server.
- Then run `docker-compose up -d`

Put input files in the [input](input) directory.<br>
Normal TIL/Cancer input: heatmap_txt<br>
Classified cancer input: heatmap_txt_3classes_separate_class<br>
...<br>
The program will output files to the [output](output) directory.<br>
<!-- IT'S USUALLY A GOOD IDEA TO TAG AN ABBREVIATED EXECID TO THE END OF THE FILENAMES SO YOU CAN DISTINGUISH THEM FROM OTHER FILES WITH THE SAME NAME -->


## Usage

### Prediction files to featuremap
Let's say you have a bunch of prediction files (color-\*, prediction-\*) and you want to generate featuremaps.<br>
The following command takes two arguments: execution id, and wsi type.<br>
wsi type can be svs, tif, scn, etc.

```
nohup docker exec quip-maputil pred_to_map exec_id exec_by wsi_type &
```

Traditionally, the channels are labelled as:
```
red = TIL
green = Cancer
blue = Tissue
```

**Optional 4th parameter**<br>
If it's a cancer-only prediction, add `Cancer` so that the program knows to put data in the correct channel.

```
nohup docker exec quip-maputil pred_to_map exec_id exec_by wsi_type Cancer &
```

<!-- Semi-related: Every time we add a new type (Pyradiomics, Gleason, etc.), quip admin has to add it to quip (field_map_type.map.node) -->

<br>


### Pyradiomics to featuremap
We've generated a bunch of pyradiomics csv files.  Here's how to create featuremaps:

```
docker exec quip-maputil pyrad_to_map exec_id exec_by
```
<br>

## Upload to server
Use [ImageLoader](https://github.com/SBU-BMI/ImageLoader) to load them.

Note: Because ImageLoader does not yet handle `execution id`, one could add that info to the host via HTTP `PATCH` calls.
<br>
