
import subprocess
from app.log.MyLog import log

xfadeStr="[0:v][1:v]xfade=duration={}:offset={}:easing={}:transition={}"
glTransiton="[0:v][1:v]gltransition=duration={}:offset={}:source={}[1:v]"
tmpCmd="ffmpeg -i {} -i {} -filter_complex_threads {} -filter_complex \"{}\" -y {}"

xfadeStr=xfadeStr.format(3,2,"cubic-in-out","wipedown")
# glTransiton=glTransiton.format(3,4,"./app/filters/GridFlip.glsl")

# filters=f"{xfadeStr};{glTransiton}"
# command=tmpCmd.format("./app/upload/v1.mp4","./app/upload/v2.mp4",4,filters,"./out2.mp4")
print("glTransiton="+glTransiton)
print("xfadeStr="+xfadeStr)
# print("command="+command)


def printStdout(pro:subprocess.CompletedProcess[str]):
    new_var = pro.stdout.replace("\n","")    
    log(f"pro.returncode={pro.returncode} pro.stdout={pro.stdout.replace("\n","")} erro={pro.stderr}")
    return new_var
    



def runCmd(cmd,cwd="."):
    result = subprocess.run(cmd,capture_output=True,text=True,cwd=cwd)
    str=""
    for i in cmd:
        str+=" "+i
    log("======>cmd:"+str)
    var=printStdout(result)
    return  var

new_var=runCmd("pwd")
glTransiton=glTransiton.format(3,4,f"{new_var}/app/filters/GridFlip.glsl")
filters=f"{xfadeStr};{glTransiton}"
# command=tmpCmd.format(f"{new_var}/app/upload/v1.mp4",f"{new_var}/app/upload/v2.mp4",4,filters,f"{new_var}/out2.mp4")
# command = [
#     "ffmpeg",
#     "-i", "upload/v1.mp4",
#     "-i", "upload/v2.mp4",
#     "-filter_complex", "[0:v][1:v]xfade=duration=3:offset=1:easing=cubic-in-out:transition=wipedown",
#     "-y", "out2.mp4"
# ]
# runCmd("sudo ffmpeg -i v2.mp4 -i v1.mp4 -filter_complex_threads 4 -filter_complex [0:v][1:v]xfade=duration=3:offset=3:easing=cubic-in-out:transition=wipedown;[0:v][1:v]gltransition=duration=3:offset=0:source=GridFlip.glsl[1:v] -y output.mp4".split(" "))


password = "lin"
command = ["sudo", "-S", "apt", "update"]

# 使用 subprocess.run，并通过 stdin 传递密码
result = subprocess.run(command, input=f"{password}\n", text=True, capture_output=True)

# 检查命令执行的结果
if result.returncode != 0:
    print("Command failed with error:", result.stderr)
else:
    print("Command executed successfully.")