#!/usr/bin/env python
from pydub import AudioSegment
import os

def detect_start_end(sound):
    chunk_size = 20
    ms = 0
    songs = []
    last_was_silent = True
    start = end = False
    while chunk_size + ms < (sound.duration_seconds * 1000):
        # print sound[ms:ms+chunk_size].dBFS
        if sound[ms:ms+chunk_size].dBFS > -35:
            # this chunk is not silent
            if last_was_silent:
                # we have a first non-silent chunk
                start = ms
                last_was_silent = False
        else:
            if not last_was_silent:
                # if the track is more than six seconds
                if ms - start > 6000:
                    # if the next secs are silent too.
                    # import ipdb; ipdb.set_trace()
                    if sound[ms:ms + 10000].dBFS < -20:
                        # end of song
                        end = ms
                        last_was_silent = True
                    # else continue after some secs
                    else:
                        ms += 10000
        ms += chunk_size
        if end and start:
            # if not too silent
            if sound[start:end].dBFS > -20:
                # it's a keeper
                songs.append((start, end))
                # we have to track last end
                start = False
    return songs

def export(sound, output, start, end):
    print 'exporting from %s to %s (%s secs) ' % (start, end, (end-start)/1000)
    chunk_to_export = sound[start:end]
    if not os.path.exists(os.path.join(os.getcwd(), 'export')):
        os.mkdir(os.path.join(os.getcwd(), 'export'))
    chunk_to_export.export('export/%s.mp3' % song_no, format='mp3')

here = os.getcwd()
sound = AudioSegment.from_file(os.path.join(here, 'sample.mp3'), format='mp3')
songs = detect_start_end(sound)
for song_no, (start, end) in enumerate(songs, 1):
    export(sound, song_no, start, end)
