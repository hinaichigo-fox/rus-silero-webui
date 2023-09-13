import argparse
import time
import subprocess
import os

import gradio as gr
import torch
import torchaudio
import nltk

import tts_preprocessor

params = {
    'speaker': 'eugene',
    'language': 'ru',
    'model_id': 'v4_ru',
    'sample_rate': 48000,
    'device': 'cpu',
    'voice_pitch': 'medium',
    'voice_speed': 'medium',
    'volume': '50'
}

model = None

voices_by_gender = ['eugene', 'baya', 'kseniya', 'xenia', 'aidar']
voice_pitches = ['x-low', 'low', 'medium', 'high', 'x-high']
voice_speeds = ['x-slow', 'slow', 'medium', 'fast', 'x-fast']

def load_model():
    global model

    nltk.download('punkt', download_dir=os.path.dirname(__file__))

    model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_tts', language=params['language'], speaker=params['model_id'])
    model.to(params['device'])

def generate(text_input, progress=gr.Progress()):

    if text_input == '':
        raise gr.Error("Input is empty")

    progress(0, 'Подготовка')

    if not model:
        load_model()

    text_input = tts_preprocessor.preprocess(text_input)
    prosody = '<prosody rate="{}" pitch="{}">'.format(params['voice_speed'], params['voice_pitch'])

    audio = torch.Tensor()
    sentences = nltk.sent_tokenize(text_input)
    progress_steps = 1 / float(len(sentences))
    cur_progress = 0
    for sentence in sentences:

        silero_input = f'<speak>{prosody}{sentence}</prosody></speak>'

        sentence_audio = model.apply_tts(ssml_text=silero_input,
                                speaker=params['speaker'],
                                sample_rate=params['sample_rate'])

        audio = torch.cat((audio, sentence_audio))

        cur_progress += progress_steps
        progress(cur_progress, 'Генерация речи')

    # Adjust volume
    audio = torch.multiply(audio, float(params['volume'])/100)

    # 1 sec of silence
    silence = torch.zeros(params['sample_rate'])
    audio = torch.cat((audio, silence))
    # 2D array
    audio = audio.unsqueeze(0)

    output_file = 'output.wav'

    torchaudio.save(output_file, audio, params['sample_rate'])

    #progress(1, 'Creating waveform')
    #out = gr.make_waveform(output_file)

    return output_file


def ui(launch_kwargs):
    # Gradio elements
    with gr.Blocks() as interface:
        gr.Markdown(
            """
            # Silero TTS
            """
        )
        with gr.Row():
            text_input = gr.Textbox(max_lines=1000, lines=5, placeholder='Вставьте сюда текст', label='Текст')

        voice = gr.Dropdown(value=params['speaker'], choices=voices_by_gender, label='Голос TTS')
        with gr.Row():
            v_pitch = gr.Dropdown(value=params['voice_pitch'], choices=voice_pitches, label='Высота голоса')
            v_speed = gr.Dropdown(value=params['voice_speed'], choices=voice_speeds, label='Скорость голоса')
            volume = gr.Slider(value=params['volume'], label='Громкость')

        with gr.Row():
            gen_button = gr.Button('Сгенерировать')

        with gr.Row():
            output = gr.Audio(label="Сгенерированная речь")


        # Event functions to update the parameters in the backend
        voice.change(lambda x: params.update({"speaker": x}), voice, None)
        v_pitch.change(lambda x: params.update({"voice_pitch": x}), v_pitch, None)
        v_speed.change(lambda x: params.update({"voice_speed": x}), v_speed, None)
        volume.change(lambda x: params.update({"volume": x}), volume, None)

        gen_button.click(generate, inputs=[text_input], outputs=[output])


    interface.queue().launch(**launch_kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--listen',
        type=str,
        default='0.0.0.0' if 'SPACE_ID' in os.environ else '127.0.0.1',
        help='IP to listen on for connections to Gradio',
    )
    parser.add_argument(
        '--username', type=str, default='', help='Username for authentication'
    )
    parser.add_argument(
        '--password', type=str, default='', help='Password for authentication'
    )
    parser.add_argument(
        '--server_port',
        type=int,
        default=0,
        help='Port to run the server listener on',
    )
    parser.add_argument(
        '--inbrowser', action='store_true', help='Open in browser'
    )

    args = parser.parse_args()

    launch_kwargs = {}
    launch_kwargs['server_name'] = args.listen

    if args.username and args.password:
        launch_kwargs['auth'] = (args.username, args.password)
    if args.server_port:
        launch_kwargs['server_port'] = args.server_port
    if args.inbrowser:
        launch_kwargs['inbrowser'] = args.inbrowser

    ui(launch_kwargs)