import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "bond005/whisper-large-v3-ru-podlodka"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)
pipe.tokenizer.pad_token_id = model.config.eos_token_id


def run_voice_to_text(path):
    result = pipe(path, generate_kwargs={"language": "russian"})
    return result["chunks"]


# Пример работы
# print(run_voice_to_text('/Users/kartashoffv/Documents/hack_RZD/speech-analyser/sample_data/test_audio.mp3'))
