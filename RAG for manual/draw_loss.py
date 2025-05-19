from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import matplotlib.pyplot as plt
import os

def plot_tensorboard_loss(log_dir="./logs"):
    # 自動找到 logs 中的 event 檔案
    event_files = [
        os.path.join(log_dir, f)
        for f in os.listdir(log_dir)
        if f.startswith("events.out.tfevents")
    ]
    if not event_files:
        print("❌ 找不到 tensorboard event 檔案")
        return

    event_file = event_files[0]  # 用第一個 event 檔案
    event_acc = EventAccumulator(event_file)
    event_acc.Reload()

    # 獲取 loss scalar
    if "loss" not in event_acc.Tags()["scalars"]:
        print("❌ logs 中沒有 loss 記錄")
        return

    scalars = event_acc.Scalars("loss")
    steps = [s.step for s in scalars]
    values = [s.value for s in scalars]

    # 繪圖
    plt.figure(figsize=(10, 5))
    plt.plot(steps, values, label="Training Loss")
    plt.xlabel("Step")
    plt.ylabel("Loss")
    plt.title("Training Loss Curve")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_tensorboard_loss("./logs")
