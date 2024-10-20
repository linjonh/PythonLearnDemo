import asyncio.subprocess
import subprocess
import os
from flask import Flask, Response, render_template, request, send_from_directory

from log.MyLog import log

app = Flask(__name__)
app.debug = True

input_path = "upload/"
RESULT_FOLDER="result"
app.config["UPLOAD_FOLDER"] = f"{input_path}"
upload_path = os.path.join(app.config["UPLOAD_FOLDER"])
filters_path = "filters/"
pwd="lin"

@app.route("/")
def showMainPage():
    return render_template("index.html")


def ensureDir(file):
    parent = os.path.dirname(file)
    log(f"path={file} parent={parent}")
    if not os.path.exists(parent):
        os.makedirs(parent)
        log(f"Created directory: {parent}")
    else:
        log(f"Directory already exists: {parent}")
    return


@app.route("/request/fileSeclectInput", methods=["POST"])
def selectInputFile():
    formData = request.form
    files = request.files.getlist("files")
    list = []
    log(f"curdir={os.path.curdir}")
    for f in files:
        log(f"name={f.name} fileName={f.filename}")
        path = os.path.join(upload_path, f.filename)
        ensureDir(path)
        log(path)
        f.save(path)
        # outFile=open(path,"wb")
        # # f.stream.read
        # while buf:=f.stream.read(16384):
        #     # log(buf.hex(":"))
        #     outFile.write(buf)

        # input = os.path.join(input_path, f.filename)
        list.append(path)

    log(f"formdata={formData} files={files}")

    out = asyncio.run(addTransion(list))

    return out


def getFilterCommand(files, outFile):
    xfadeStr = "[0:v][1:v]xfade=duration={duration}:offset={offset}:easing={easing}:transition={trans}"
    glTransiton = (
        "[0:v][1:v]gltransition=duration={duration}:offset={offset}:source={trans}[1:v]"
    )
    tmpCmd = "sudo -S ffmpeg -i {video1} -i {video2} -filter_complex_threads {threadCount} -filter_complex {xfade} -y {out}"

    xfadeStr = xfadeStr.format(
        duration=3, offset=2, easing="cubic-in-out", trans="wipedown"
    )
    glTransiton = glTransiton.format(
        duration=3, offset=1, trans=f"{filters_path}GridFlip.glsl"
    )

    filters = f"{xfadeStr};{glTransiton}"
    filterCommand = tmpCmd.format(
        video1=files[0], video2=files[1], threadCount=4, xfade=filters, out=outFile
    )
    print("glTransiton=" + glTransiton)
    print("xfadeStr=" + xfadeStr)
    print("command=" + filterCommand)
    return filterCommand


def printStdout(pro: subprocess.CompletedProcess[str]):
    log(f"pro.returncode={pro.returncode} pro.stdout={pro.stdout.replace("\n","")} erro={pro.stderr}",frameIndex=2)


async def addTransion(files):
    outFile = f"{RESULT_FOLDER}/out2.mp4"
    cmd = getFilterCommand(files, outFile)
    cwd = prindCWD()
    # subprocess 传入的cmd为列表数组
    hit=cwd.stdout.find("app")
    log(f"hit={hit}")
    if(hit>=0):
        pro = subprocess.run(cmd.split(" "),input=f"{pwd}\n",capture_output=True, text=True)
    else:
        cwd = subprocess.run("pwd",cwd="./app",input=f"{pwd}\n", capture_output=True, text=True)
        printStdout(cwd)
        pro = subprocess.run(cmd.split(" "),cwd="./app",input=f"{pwd}\n",capture_output=True, text=True)
        
    printStdout(pro)
    # readStr = pro.stdout.find(":")
    # log(f"readStr={readStr}")
    # if readStr > 0:
    #     pro = subprocess.run("lin")
    #     printStdout(pro)
    if(pro.returncode!=0):
        prindCWD()
        msg="转场滤镜处理失败"
        log(msg)
        return msg, 500
    return f'/result/{os.path.basename(outFile)}',200

def prindCWD():
    cwd = subprocess.run("pwd", capture_output=True, text=True)
    printStdout(cwd)
    return cwd

@app.route("/result/<fileName>")
def showResult(fileName):
    log(f"fileName={fileName}")
    return send_from_directory(RESULT_FOLDER,fileName)

if __name__ == "__main__":
    app.run(debug=True)
