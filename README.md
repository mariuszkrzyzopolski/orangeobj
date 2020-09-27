# orangeobj

## class - MergeOrangeData(filename,sheetname)
### __init__
Create Dataframe, normalize data and merge duplicate records

### merge_pair(firstrecord,secordrecord)
scan through numpy matrix to filter NaN values and save not Nan
return one merged record

### merge_data_frame()
r - scan to duplicate values and saves them
len(r) > 2 - duplicates, use merge_pair to filter NaNs
len(r) == 1 - uniq.only save to result dataframe
in end drop duplicates results from dataframe and return result

### generate_html(name)
add style and save to target file
