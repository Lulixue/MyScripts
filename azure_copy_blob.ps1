$SrcPath = "https://srcxxx.blob.core.windows.net/SAS_TOKEN"
$DstPath = "https://dstxxx.blob.core.windows.net/SAS_TOKEN"

./azcopy.exe copy $SrcPath $DstPath --recursive --overwrite=ifsourcenewer
