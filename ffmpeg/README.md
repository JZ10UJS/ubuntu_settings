# Command
``` sh
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -strict -2 -hls_time 30 -hls_list_size 0 -f hls output.m3u8

```


# Refrences
`http://blog.csdn.net/jookers/article/details/21694957`