"""Select the local or Gemini inference backend without loading models at import time."""

import os


def get_inference_backend(backend=None):
    backend = backend or os.getenv("INFERENCE_BACKEND", "local")
    if backend == "api":
        from model.api_inference_service import get_gemini_service
        return get_gemini_service()
    if backend == "local":
        from model import inference_service
        if inference_service._model_config is None:
            model_type = os.getenv("MODEL_TYPE", "qwen")
            if model_type == "qwen":
                from model.model_config_qwen import MODEL_CONFIG
            elif model_type in ("7b", "deepseek"):
                from model.model_config_7b import MODEL_CONFIG
            else:
                raise ValueError("MODEL_TYPE must be qwen, deepseek, or 7b")
            inference_service.set_model_config(MODEL_CONFIG)
        return inference_service.get_inference_service()
    raise ValueError("INFERENCE_BACKEND must be local or api")


__all__ = ["get_inference_backend"]

