from django.db import models
from transformers import T5ForConditionalGeneration, T5Tokenizer

class TextSummarizer:
    def __init__(self):
        self.model_name = 't5-large'  # estab t5-small  Modelo T5 específico para español# Puedes cambiar a 't5-base', 't5-large', etc.
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)

    def summarize(self, text):
        # Preprocesar el texto de entrada
        preprocess_text = text.strip().replace("\n", "")
        t5_input_text = "summarize: " + preprocess_text

        # Tokenizar el texto de entrada
        tokenized_text = self.tokenizer.encode(t5_input_text, return_tensors="pt", max_length=512, truncation=True)

        # Generar el resumen
        summary_ids = self.model.generate(
            tokenized_text, 
            max_length=350,  # Longitud máxima del resumen en tokens
            min_length=20,  # Longitud mínima del resumen (al menos 50% de max_length o 50 tokens)
            length_penalty=1.5,  # Penalización de longitud ajustada
            num_beams=4,  # Número de haces para búsqueda
            early_stopping=True  # Detener la generación temprano si se alcanza una secuencia válida
        )        
        
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)


        return summary

