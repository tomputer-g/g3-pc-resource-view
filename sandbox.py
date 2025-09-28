# import nvidia_smi

# def get_gpu_stats():
#     nvidia_smi.nvmlInit()
#     handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)  # First GPU
#     mem_info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
#     utilization = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)

#     stats = {
#         "gpu_memory_GB": mem_info.used / (1024 ** 3),  # Bytes to GB
#         "gpu_util_percent": utilization.gpu  # percentage
#     }
    
#     nvidia_smi.nvmlShutdown()
#     return stats

# # Example usage
# if __name__ == "__main__":
#     gpu_stats = get_gpu_stats()
#     print(gpu_stats)

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import time
import nvidia_smi

app = FastAPI()

# Mount your existing folder containing index.html as root static files
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

def get_gpu_stats():
    nvidia_smi.nvmlInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
    mem_info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
    utilization = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
    stats = {
        "metrics": {
            "gpumem": round(mem_info.used / (1024 ** 3), 2),  # memory in GB
            "gpuutil": utilization.gpu
        },
        "units": {
            "gpumem": "MB",
            "gpuutil": "s"
        }
    }
    nvidia_smi.nvmlShutdown()
    return stats

@app.get("/")
def root():
    # Redirect root to static index.html
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")


@app.get("/stream", response_class=JSONResponse)
def stream():
    stats = get_gpu_stats()
    return JSONResponse(content=stats)