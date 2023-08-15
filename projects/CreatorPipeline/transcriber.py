# from CreatorPipeline import _openai as oai
# # from pydub import AudioSegment
# from pathlib import Path
# audio_file = r"./testMovie_Audio.wav"

# file_base = str(Path(audio_file).parent / "samples")

# song = AudioSegment.from_wav(audio_file)
# minutes = 2
# sample_length = minutes * 60 * 1000

# samples = []
# start = 0
# dur = song.duration_seconds * 1000

# splitting = True
# while splitting:

#     if dur > sample_length:

#         end = start + sample_length
#         sample = song[start: end]
#         samples.append(sample)

#         start += sample_length
#         dur -= sample_length
#     else:
#         sample = song[start:]
#         samples.append(sample)
#         splitting = False


# for i, sample in enumerate(samples):
#     outfile = f"{file_base}/sample_{i:04d}.wav"
#     print(outfile, flush=True)
#     # sample = sample.strip_silence()
#     # print("\tsilence stripped", flush=True)
#     # sample = sample.normalize()
#     # print("\tnormalized", flush=True)
#     # sample = sample.compress_dynamic_range(threshold=-14.0)
#     # print("\tdynamic range compressed", flush=True)
#     sample.export(outfile, format="wav")
#     print("\texported", flush=True)

#     oai.generate_closed_captions(outfile, output=None)



# # first_10_minutes = song[:sample_length]
# # first_10_minutes.export("good_morning_10.mp3", format="mp3")


# # new split audio by silence
# # then transcode it



# # split audio into 10 minute chunks
# # read all files
# # merge end points
# # use fuzzy logic or something to find the best match


# # from pydub import AudioSegment
# # from pydub.silence import split_on_silence

# # sound = AudioSegment.from_file(audio_file, format="wav")
# # sound = sound.normalize()
# # chunks = split_on_silence(
# #     sound,

# #     # split on silences longer than 1000ms (1 sec)
# #     min_silence_len=1000,

# #     # anything under -16 dBFS is considered silence
# #     silence_thresh=-60,

# #     # keep 200 ms of leading/trailing silence
# #     keep_silence=400
# # )

# # slices = {}

# for i, sample in list(enumerate(chunks))[:3]:
#     for y in dir(sample):
#         print(y)

#     outfile = f"{file_base}/sample_{i:04d}.mp3"
#     print(outfile, flush=True)
#     sample = sample.normalize()
#     sample = sample.compress_dynamic_range(threshold=-14.0)
#     sample.export(outfile, format="mp3")
#     print("\texported", flush=True)
#     text = oai.generate_closed_captions(outfile, output=None).get("text")
#     slices[i] = [outfile, text]

# # closed caption function should recombine
# # use a ml model to cluster all sentences into similar
# # then choose most recent.



# # now recombine the chunks so that the parts are at least 90 sec long
# # target_length = 90 * 1000
# # output_chunks = [chunks[0]]
# # for chunk in chunks[1:]:
# #     if len(output_chunks[-1]) < target_length:
# #         output_chunks[-1] += chunk
# #     else:
# #         # if the last output chunk is longer than the target length,
# #         # we can start a new one
# #         output_chunks.append(chunk)

# # # now your have chunks that are bigger than 90 seconds (except, possibly the last one)


# # Maybe just use the first splitter to get the frames to cut things, and this to manually call ffmpeg @ specific frames.
