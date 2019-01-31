
解决在Windows平台将本地mp3/flac/wav等格式的音乐导入iTunes进而导入iPhone时遇到的一系列问题:

### 1, 无法导入flac/wav格式. 

我的解决思路: 执行convert_flac_wav_2_mp3.py会将当前目录下的flac/wav音频转换为mp3格式的音乐(320kbps), 如果当前目录有一个子目录"some_dir"存放着部分flac/wav文件, 则会将其转换为mp3以后放入"converted_some_dir"目录.

### 2, 音乐文件tag乱码.

我的解决思路: 将音乐文件重命名为以下格式:
<pre><code>演唱者 - 歌曲名.mp3
演唱者 - 歌曲名.flac

# 如果有专辑名称, 也可以加上专辑名称, 例如下面:
演唱者 - 歌曲名 - 专辑名.mp3
演唱者 - 歌曲名 - 专辑名.flac
</code></pre>

python脚本会读取音乐文件里的tag信息, 并与'文件名'中的信息作比对, 如果不一致, 则会将'文件名中'提取出的tag写入音乐文件. 
这一步是有内险的. 有这样一种可能性, 音乐文件里的tag信息是正确的, 但是'文件名'里写的tag是错误的, 此时有可能将正确tag信息覆盖.

# 准备工作:

<pre><code>sudo apt install python3 python3-dev

\# 安装pip
wget https://bootstrap.pypa.io/get-pip.py -O - | sudo python3
</code></pre>


\# 安装pytaglib相关依赖. 否则运行pip install pytaglib会报错, centos请安装python-devel和taglib-devel
\# pytaglib这个包调用了os.fspath()方法, 但该方法从python3.6版本开始引入. 因此需要安装python3.6以上的版本. Ubuntu 18.04自带Python3.6版.
<pre><code>sudo apt install gcc g++ python3-dev libtag1-dev
sudo apt install python3-taglib    #https://pypi.org/project/pytaglib/, 用于修正mp3/flac文件的TAG信息
</code></pre>

### 安装libav 或者 ffmpeg (任选其一)
<pre><code>sudo apt-get install libav-tools libavcodec-extra
sudo apt-get install ffmpeg libavcodec-extra

sudo pip install pydub      #https://github.com/jiaaro/pydub, 用于将flac/wav等格式转换为mp3格式
</code></pre>

# 转换flac/wav文件格式:

<pre><code>./convert_flac_wav_2_mp3.py
</code></pre>

# 修正音乐文件的tag信息(演唱者)

<pre><code>./tag_repair_album.py
</code></pre>

# 修正音乐文件的tag信息(歌曲名)

<pre><code>./tag_repair_album.py
</code></pre>

# 修正音乐文件的tag信息(专辑名)

<pre><code>./tag_repair_album.py
</code></pre>

### 提示:
wav格式在Windows平台存在编码问题, 因此使用taglib修改完tag仍是乱码, 建议转换完mp3以后删除wav格式





