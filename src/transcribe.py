import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

def transcribe(audio_file_path, model_type):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = f"openai/whisper-{model_type}"

    print("Loading model...")

    # Original Model
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True,
        attn_implementation="eager"
    )
    
    # Flash Attention
    # model = AutoModelForSpeechSeq2Seq.from_pretrained(
    #     model_id, torch_dtype=torch_dtype, 
    #     low_cpu_mem_usage=True, 
    #     use_safetensors=True, 
    #     use_flash_attention_2=True
    # )

    # Better Transformer Model
    # model = model.to_bettertransformer()

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
    
    print(f"Transcribing...")
    result = pipe(audio_file_path, generate_kwargs={"language": "english"}, return_timestamps="word")
    print(result["text"])
    # print(result["chunks"])
    
    return result["chunks"]
