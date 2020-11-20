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
        "exec_id": exec_id,
        "executedby": executedby
    },
    "data": {
        "locations": {
            "i": [list of 'i' (aka 'x' coordinates)],
            "j": [list of 'j' (aka 'y' coordinates)]
        },
        "features": {
            "TIL": [ list of feature data corresponding to i,j ],
            "Cancer": [ list of feature data corresponding to i,j ],
            "Tissue": [ list of feature data corresponding to i,j ]
        }
    }
}
```

