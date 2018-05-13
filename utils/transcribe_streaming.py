#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.

Example usage:
	python transcribe_streaming.py resources/audio.raw
"""

# [START import_libraries]
import argparse
import io
import os
import sys
# [END import_libraries]

google_json_key_path = '/home/pi/MyMic-b737a86ac104.json'

def transcribe_streaming(audio_file):
	"""Streams transcription of the given audio file."""
	from google.cloud import speech
	from google.cloud.speech import enums
	from google.cloud.speech import types
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_json_key_path
	client = speech.SpeechClient()

	content = audio_file.read()
	stream = [content]
	requests = (types.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream)

	config = types.RecognitionConfig(
			encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
			sample_rate_hertz=44100,
			language_code='ko-KR')
	streaming_config = types.StreamingRecognitionConfig(config=config)

	responses = client.streaming_recognize(streaming_config, requests)

	for response in responses:
		for result in response.results:
			alternatives = result.alternatives
			for alternative in alternatives:
				return alternative.transcript

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('stream', help='File to stream to the API')
	args = parser.parse_args()
	transcribe_streaming(args.stream)
