# 🎧 Deezer RPC | v2

**Deezer RPC** is a lightweight Python application that updates your Discord Rich Presence with the song you're currently playing on **Deezer**. It works by detecting the active **Deezer window** and syncing the track title in real-time, enhancing your Discord status with detailed song info.

This project was created as an alternative to [Yuuto's project](https://github.com/JustYuuto/deezer-discord-rpc), which inspired the method of capturing song details via the window title.

---

## 📚 Table of Contents  

1. [✨ Features](#-features)  
2. [⚙️ Installation](#️-installation)  
   - [Prerequisites](#prerequisites)  
   - [Clone the Repository](#clone-the-repository)  
   - [Run the Application](#run-the-application)  
3. [🖼️ Screenshots](#️-screenshots)   
4. [🤝 Contributing](#-contributing)  
5. [📄 License](#-license)  

---

## ✨ Features  

- **Discord Rich Presence** integration for **Deezer** 🎶  
- **Auto-detects** active Deezer window or lets you manually select from multiple windows 🔍  
- **Real-time track and artist updates** with album cover and artist image ⏳  
- **Error logging** for better debugging 🛠️  
- **Improved window detection** that matches variations of Deezer window titles  
- **Lightweight & fast** performance ⚡  

---

## ⚙️ Installation  

### Prerequisites  

Ensure you have the following installed:  

- **Python 3.10** or later  
- Required Python modules:  
  ```bash
  pip install pygetwindow pypresence requests
  ```
- **Deezer application** must be open with a song playing  

### Clone the Repository  

```bash
git clone https://github.com/nildontsleep/deezer-rpc.git
cd deezer-rpc
```

### Run the Application  

```bash
python deezer_rpc.py
```

---

## 🖼️ Screenshots  

Here’s a quick look at **Deezer RPC** in action!  

### 🎧 Discord Rich Presence  

![inDiscord](https://github.com/user-attachments/assets/5caaf4af-5955-46d9-b047-41195b5c0adc)

### 🖥️ Running in Terminal  

![term prev](https://github.com/user-attachments/assets/9c448013-3be9-4373-8c2b-d6367d7f8e69)

---

## 🤝 Contributing  

Contributions are welcome!  

- 🛠️ **Fork** this repository.  
- 🌟 Create a new **branch** for your feature or bug fix.  
- 📨 Submit a **pull request** with detailed notes on your changes.  

---

## 📄 License  

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

--- 

### Key Updates in v2:
- **Mode Selection:** Users can now choose between **auto-detect** and **manual window selection** for greater flexibility in detecting Deezer windows.
- **Improved Logging and Error Handling:** Detailed logs are now recorded for troubleshooting and monitoring.
